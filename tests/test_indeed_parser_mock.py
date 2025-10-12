"""Indeed parser validation with mock HTML"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.indeed.parser import extract_description
from bs4 import BeautifulSoup


def test_indeed_description_extraction():
    """Test Indeed job description extraction with mock HTML"""
    mock_html = """
    <div id="jobDescriptionText">
        <p>We're looking for a Senior Data Analyst to join our analytics team.
        Required skills: Python, SQL, Tableau, Power BI, Excel.
        Experience with statistical analysis and machine learning is a plus.
        3-5 years of experience in data analysis required.
        Bachelor's degree in Statistics, Mathematics, or Computer Science.</p>
    </div>
    """
    
    soup = BeautifulSoup(mock_html, 'html.parser')
    description = extract_description(soup)
    
    assert description, "Description should not be empty"
    assert len(description) > 50, f"Description too short: {len(description)} chars"
    assert "Data Analyst" in description
    assert "Python" in description
    assert "SQL" in description
    
    print(f"✅ Description extracted: {len(description)} characters")
    print(f"   Preview: {description[:100]}...")


if __name__ == "__main__":
    test_indeed_description_extraction()
    print("\n🎉 Indeed parser test passed!")
