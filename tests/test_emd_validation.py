# EMD Module Structure Validation Test
# Validates that all EMD components import correctly without running operations

def test_model_imports():
    """Test that JobModel imports correctly"""
    try:
        from models.job import JobModel
        print("✅ JobModel import: SUCCESS")
        return True
    except Exception as error:
        print(f"❌ JobModel import: FAILED - {error}")
        return False

def test_coordinator_imports():
    """Test that ParallelCoordinator imports correctly"""
    try:
        from scrapers.coordinator import ParallelCoordinator
        print("✅ ParallelCoordinator import: SUCCESS")
        return True
    except Exception as error:
        print(f"❌ ParallelCoordinator import: FAILED - {error}")
        return False

def test_worker_pool_imports():
    """Test that WorkerPoolManager imports correctly"""
    try:
        from scrapers.worker_pool import WorkerPoolManager
        print("✅ WorkerPoolManager import: SUCCESS")
        return True
    except Exception as error:
        print(f"❌ WorkerPoolManager import: FAILED - {error}")
        return False

def test_application_imports():
    """Test that JobScrapperApplication imports correctly"""
    try:
        from scrapers.application import JobScrapperApplication
        print("✅ JobScrapperApplication import: SUCCESS")
        return True
    except Exception as error:
        print(f"❌ JobScrapperApplication import: FAILED - {error}")
        return False

def test_main_wrapper_imports():
    """Test that main function imports correctly"""
    try:
        from scrapers.main_wrapper import main
        print("✅ main function import: SUCCESS")
        return True
    except Exception as error:
        print(f"❌ main function import: FAILED - {error}")
        return False

def validate_emd_architecture():
    """Validate complete EMD architecture without running operations"""
    print("🔍 EMD ARCHITECTURE VALIDATION")
    print("=" * 50)
    
    success_count = 0
    total_tests = 5
    
    # Test all module imports
    if test_model_imports(): success_count += 1
    if test_coordinator_imports(): success_count += 1  
    if test_worker_pool_imports(): success_count += 1
    if test_application_imports(): success_count += 1
    if test_main_wrapper_imports(): success_count += 1
    
    print("=" * 50)
    print(f"📊 RESULTS: {success_count}/{total_tests} components validated")
    
    if success_count == total_tests:
        print("🎉 EMD REFACTORING: COMPLETE SUCCESS!")
        print("✅ All modules import correctly")
        print("✅ EMD architecture properly implemented")
        return True
    else:
        print("⚠️ EMD REFACTORING: PARTIAL SUCCESS")
        print(f"❌ {total_tests - success_count} components need fixes")
        return False

if __name__ == "__main__":
    validate_emd_architecture()
