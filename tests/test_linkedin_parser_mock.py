"""LinkedIn parser validation with mock HTML - bypass browser dependency"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraper.unified.linkedin.parser import extract_description
from bs4 import BeautifulSoup


def test_linkedin_description_extraction():
    """Test LinkedIn job description extraction with mock HTML"""
    # Mock LinkedIn job card HTML with description
    mock_html = """
    <div class="base-card">
        <div class="base-search-card__info">
            <div class="show-more-less-html__markup">
                <p>We are seeking a Data Analyst with 3+ years of experience in Python, SQL, and Tableau.
                The ideal candidate will have strong analytical skills and experience with data visualization.
                Key responsibilities include building dashboards, analyzing datasets, and presenting insights to stakeholders.
                Must have Bachelor's degree in Computer Science or related field.</p>
            </div>
        </div>
    </div>
    """
    
    soup = BeautifulSoup(mock_html, 'html.parser')
    description = extract_description(soup)
    
    # Validate description was extracted
    assert description, "Description should not be empty"
    assert len(description) > 50, f"Description too short: {len(description)} chars"
    assert "Data Analyst" in description
    assert "Python" in description
    
    print(f"✅ Description extracted: {len(description)} characters")
    print(f"   Preview: {description[:100]}...")


if __name__ == "__main__":
    test_linkedin_description_extraction()
    print("\n🎉 LinkedIn parser test passed!")
