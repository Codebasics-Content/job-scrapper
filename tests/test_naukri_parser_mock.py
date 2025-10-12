"""Naukri parser validation with mock HTML"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.naukri.parser import extract_description
from bs4 import BeautifulSoup


def test_naukri_description_extraction():
    """Test Naukri job description extraction with mock HTML"""
    mock_html = """
    <div class="jd-content">
        <p>Job Description: We are hiring a Data Analyst with strong analytical skills.
        Required: Python, SQL, Excel, Power BI, Tableau.
        Experience: 2-4 years in data analysis and reporting.
        Education: B.Tech/M.Tech in Computer Science or related field.</p>
    </div>
    <div class="key-skill">
        <span>Python</span><span>SQL</span><span>Tableau</span><span>Power BI</span>
    </div>
    """
    
    soup = BeautifulSoup(mock_html, 'html.parser')
    description = extract_description(soup)
    
    assert description, "Description should not be empty"
    assert len(description) > 50, f"Description too short: {len(description)} chars"
    assert "Data Analyst" in description
    assert "Python" in description
    
    print(f"✅ Description extracted: {len(description)} characters")
    print(f"   Preview: {description[:100]}...")


if __name__ == "__main__":
    test_naukri_description_extraction()
    print("\n🎉 Naukri parser test passed!")
