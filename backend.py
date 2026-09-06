"""
backend.py
==========

Core logic for the Continuity Checker.

This module will be responsible for:
    - Loading and chunking manuscript text (e.g. by chapter or scene).
    - Extracting entities and attributes worth tracking for continuity
      (character names, physical descriptions, locations, dates/timeline
      markers, relationships, etc.).
    - Comparing extracted attributes across the manuscript to detect
      contradictions (e.g. a character's eye colour, age, or name changing
      partway through).
    - Calling out to an external API (via `requests`, using the API key
      loaded from `.env` through `python-dotenv`) to perform analysis that
      benefits from a language model, such as semantic contradiction
      detection that goes beyond simple string matching.
    - Returning structured results (e.g. a list of flagged issues with
      location, description, and confidence) that `app.py` can render.

Currently a placeholder — no logic has been implemented yet. Functions
and classes will be added in subsequent development phases.
"""
