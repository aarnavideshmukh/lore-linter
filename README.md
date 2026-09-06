# Continuity Checker

A tool for scanning manuscripts to catch continuity errors — contradictory
physical descriptions, timeline inconsistencies, name/detail drift, and
similar slips that are easy for a human editor to miss across a long
document.

## Project Structure

```
continuity-checker/
├── backend.py          # Core logic (analysis, API calls, contradiction detection)
├── app.py              # Streamlit frontend
├── demo_output.json    # Pre-run cache of a sample analysis (for fast demos)
├── requirements.txt    # Python dependencies
├── data/
│   └── sample.txt       # Sample manuscript excerpt with a known planted error
└── README.md
```

## Setup

1. **Clone / copy the project** into a local directory named `continuity-checker/`.

2. **Create a virtual environment** (recommended):

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API key:**

   Copy `.env.example` (or edit the existing `.env`) and set your key:

   ```
   API_KEY=your_key_here
   ```

   `.env` is loaded automatically at runtime via `python-dotenv`. Do not
   commit your real API key — keep `.env` out of version control.

5. **Run the app:**

   ```bash
   streamlit run app.py
   ```

   This opens the frontend in your browser (default: http://localhost:8501).

## Sample Data

`data/sample.txt` contains a short excerpt from *Pride and Prejudice*
(public domain) with one intentional continuity error planted in it —
Elizabeth Bennet's eye colour is described inconsistently (dark eyes in
Chapter 2, blue eyes in Chapter 3). This is included so the checker's
output can be verified against a known, deliberate mistake.

## Status

This is an early scaffold (Phase 0). `backend.py` and `app.py` are
currently empty stubs to be filled in during subsequent development
phases.

## Roadmap

- [ ] Implement core contradiction-detection logic in `backend.py`
- [ ] Build the Streamlit UI in `app.py` (upload manuscript, run check, view results)
- [ ] Wire up API calls for text analysis
- [ ] Expand sample data with more contradiction types (names, dates, locations)
- [ ] Add tests
