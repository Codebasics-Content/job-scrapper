# AegisIDE Framework - Quick Reference
## Job Scraper Project

### 🎯 Autonomy Level: 99.5
**Execute immediately + Document**

### ⚡ Key Commands (Auto-Approved)
```bash
# Code Analysis
python -m pytest tests/ -v
python -m black --check src/
python -m pyright src/

# Database
python check_db.py
sqlite3 jobs.db "SELECT DISTINCT platform FROM jobs;"

# Git
git status && git diff
git add . && git commit -m "message"

# Development
streamlit run streamlit_app.py
python scripts/validate_skills.py
```

### 📂 Memory Bank Files
```
.warp/aegiside/memory-bank/
├── activeContext.json   # Current task state
├── scratchpad.json      # Working notes
├── kanban.json          # Task board
├── mistakes.json        # Error log
├── systemPatterns.json  # Design patterns
├── progress.json        # Metrics
├── roadmap.json         # Planning
└── memory.json          # Knowledge base
```

### 📜 Constitutional Articles
```
.warp/rules/constitution/
├── article_1_foundation.md       # Mission & principles
├── article_2_command_safety.md   # Execution protocol
├── article_3_memory_bank.md      # Knowledge governance
└── article_4_quality_validation.md # Quality standards
```

### ✅ Validation Loop
```
1. Implement → 2. Test → 3. Validate → 4. Document
```

### 🚫 Never Do
- ❌ Ask permission for safe commands
- ❌ Ask "Should I continue?"
- ❌ Skip validation steps
- ❌ Delete memory bank files

### 📊 Project Stats
- **Languages**: Python 3.13+
- **Framework**: Streamlit
- **Database**: SQLite with indexes
- **Skills DB**: 20,000+ technical skills
- **Test Coverage**: 75%
- **Autonomy**: Level 99.5

### 🔄 Update Protocol
```
After task completion:
1. Update activeContext.json
2. Clear scratchpad.json completed items
3. Update progress.json metrics
4. Log in mistakes.json if errors
5. Document patterns in systemPatterns.json
```

### 📖 Key Files
- `WARP.md` - Main guidance
- `.warp/IMPLEMENTATION_SUMMARY.md` - Complete setup
- `.warp/aegiside/README.md` - Memory bank docs
- `DATABASE_FIXES.md` - Historical fixes
- `README.md` - Project overview