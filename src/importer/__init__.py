# BrightData Import Module
# Handles pre-scraped data import with skills extraction

from .brightdata.linkedin_importer import import_linkedin_jobs

__all__ = ["import_linkedin_jobs"]
