"""Run complete integration test pipeline with reporting"""
import subprocess
import sys
import json
from pathlib import Path
from datetime import datetime


def check_docker_services():
    """Check if Docker services are running"""
    print("Checking Docker services...")
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        containers = result.stdout.strip().split("\n")
        
        print(f"Running containers: {containers}")
        
        required = ["headlessx", "proxy"]
        running = [c for c in containers if any(r in c.lower() for r in required)]
        
        if len(running) < 2:
            print(f"⚠ Missing services. Found: {running}")
            print("Please start Docker services:")
            print("  ./start_proxy_docker.sh")
            return False
        
        print(f"✓ Docker services running: {running}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Docker check failed: {e}")
        print("Please start Docker daemon")
        return False


def run_tests():
    """Execute pytest with reporting"""
    print(f"\n{'='*70}")
    print("INTEGRATION TEST PIPELINE")
    print(f"{'='*70}\n")
    
    test_dir = Path(__file__).parent / "integration"
    
    # Run pytest with verbose output
    result = subprocess.run(
        [
            "pytest",
            str(test_dir),
            "-v",
            "--tb=short",
            "-s",
            "--maxfail=1"
        ],
        cwd=Path(__file__).parent.parent
    )
    
    return result.returncode


def main():
    """Main test pipeline"""
    start_time = datetime.now()
    
    # Step 1: Check Docker
    if not check_docker_services():
        sys.exit(1)
    
    # Step 2: Run tests
    exit_code = run_tests()
    
    # Step 3: Report
    duration = (datetime.now() - start_time).total_seconds()
    
    print(f"\n{'='*70}")
    print(f"Pipeline completed in {duration:.1f}s")
    print(f"Exit code: {exit_code}")
    print(f"{'='*70}\n")
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
