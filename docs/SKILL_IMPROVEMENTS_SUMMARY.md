# Skills Reference Improvements - 2025-10-12

## Gap Analysis Results

### Skills Mentioned but NOT Extracted
**Issue**: Job descriptions mention these skills but the extractor doesn't capture them.

| Skill | Mentions | Status |
|-------|----------|--------|
| ChatGPT | 5 times | ✅ NEED TO ADD |
| Claude Code | 2 times | ✅ Improve patterns |
| GitHub Copilot | 2 times | ✅ NEED TO ADD |

### Industry False Positives (NOT Skills)
**Issue**: These are industries/domains, not technical skills. They pollute extraction results.

| False Positive | Extractions | Action |
|----------------|-------------|--------|
| Legal | 40 times | ✅ REMOVED |
| Insurance | 30 times | ✅ REMOVED |
| Supply Chain | 8 times | ✅ REMOVED |
| Agriculture | 2 times | ✅ REMOVED |
| Automotive | 1 time | ⚠️ KEPT (borderline) |

## Changes Made

### 1. Enhanced Anthropic Claude Patterns
```json
"patterns": [
  "claude",
  "anthropic",
  "anthropic claude",
  "claude code",  // NEW
  "claude ai"     // NEW
]
```

### 2. Added ChatGPT
```json
{
  "name": "ChatGPT",
  "patterns": [
    "chatgpt",
    "chat gpt",
    "chat-gpt",
    "openai chatgpt",
    "customgpt",
    "customgpts"
  ]
}
```

### 3. Added GitHub Copilot
```json
{
  "name": "GitHub Copilot",
  "patterns": [
    "github copilot",
    "copilot",
    "gh copilot"
  ]
}
```

### 4. Removed Industry False Positives
- Removed "Insurance" from domain_expertise
- Removed "Legal" from domain_expertise
- Removed "Supply Chain" from domain_expertise  
- Removed "Agriculture" from domain_expertise

## Impact

**Before**: 549 skills (with false positives)
**After**: 547 skills (cleaner, more accurate)

**New Skills Added**: ChatGPT, GitHub Copilot
**Improved Patterns**: Anthropic Claude (now catches "Claude Code")
**Removed**: 4 industry false positives

## Next Steps

1. Re-run skill extraction on database to validate improvements
2. Monitor extraction accuracy on new job descriptions
3. Continue iterative improvements based on real-world usage
