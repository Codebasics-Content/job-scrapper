# Deprecated UI Components

**⚠️ DO NOT USE - LEGACY CODE**

This directory contains deprecated Streamlit UI components that have been replaced by inline UI logic in the main `streamlit_app.py`.

## Deprecated Components

- `components/` - Modular UI components (scraper forms, analytics widgets, etc.)
- `utils/` - UI helper functions

## Current Architecture (Use Instead)

**Location**: `streamlit_app.py` (root)

**Rationale**: Streamlit apps work best as single-file applications for simplicity and maintainability. The modular component approach added unnecessary complexity without significant benefit.

## Migration Date

2025-10-11
