# Database Module

## Purpose
Manages all interactions with the SQLite database for safe and reliable data storage.

## What It Does
- **Stores Job Data**: Saves complete job information (title, company, description, skills)
- **Tracks Progress**: Maintains URL processing status (pending/completed)
- **Prevents Duplicates**: Checks existing records before adding new ones
- **Atomic Transactions**: Ensures data consistency—both save job AND mark URL as processed, or neither

## Why It Matters
Database integrity is critical. A failed save could lose job data or mark unprocessed URLs as complete. This module guarantees data reliability through transactional operations.

## Key Feature
**Resume Capability** - If the system stops, the database remembers exactly where to continue, preventing duplicate work or lost progress.
