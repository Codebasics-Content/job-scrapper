# LinkedIn Skill Extraction Refinement - Iteration Log

## **ITERATION 1**: Initial Analysis
- False Positives: 82 unique
- False Negatives: 58 unique
- **Issue**: Raw extractions not normalized to canonical names

## **ITERATION 2**: Pattern→Name Normalization  
- Created `refine_linkedin_skills.py` with pattern mapping
- Filtered 300 invalid skills (truncated phrases, noise)
- **Result**: False Positives: 0 ✅ | False Negatives: 84

## **ITERATION 3**: Re-extraction with AdvancedSkillExtractor
- Used `re_extract_skills.py` to re-run 3-layer extraction
- Re-extracted 363 jobs from job_description field
- **Result**: False Positives: 0 ✅ | False Negatives: 84 (unchanged)

## **ROOT CAUSE IDENTIFIED**:
Skills like Docker, Scala, Java, Git, AWS exist in:
1. ✅ Job descriptions (confirmed)
2. ✅ skills_reference_2025.json (need to verify patterns)
3. ❌ Extracted skills list (NOT being detected)

**Hypothesis**: Patterns in skills_reference_2025.json aren't matching OR extractor layers filtering them.

## **NEXT ACTIONS**:
1. Verify Docker/Scala/Java/Git patterns exist in reference
2. If missing → add patterns
3. If present but not matching → fix regex patterns
4. Re-extract → Re-analyze → Iterate until FN=0
