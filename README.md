# Portfolio Metrics Assistant

A small tool I built to automate the annoying part of financial analysis: pulling the same metrics out of long, messy PDF reports.

This started as a personal experiment after noticing how much time goes into manually reading financial reports and extracting numbers that are often reported inconsistently across companies. I wanted to see how far I could push a lightweight, LLM-assisted pipeline before it stopped being useful.

## What This Is

The app takes one or more financial reports (PDFs) and extracts selected financial metrics into a structured format that’s easy to analyze.

You upload reports, pick the metrics you care about (or add your own), and get a clean table back. That’s it.

It’s not meant to be production-ready. It _is_ meant to explore how AI can help turn unstructured documents into something usable without pretending the problem is trivial.

## Why I Built It

Two reasons:

1. Financial PDFs are painful to work with. Even simple questions like “what was revenue last quarter?” often require manual digging.
2. Most AI demos ignore the hard parts: inconsistent formats, missing data, and the risk of confidently wrong outputs.

This project was my way of exploring those edges instead of avoiding them.

## How It Works (High Level)

- PDFs are parsed using `pdfplumber`
- Text is cleaned and chunked to preserve financial context
- An LLM is used to extract only the metrics requested
- Results are returned as structured JSON and displayed in a table
- Multiple PDFs are processed in parallel to keep things reasonably fast

The UI is built with Streamlit because it’s quick to iterate and good enough for this use case.

## Features

- Upload one or multiple PDFs
- Select common financial metrics (revenue, gross margin, headcount, ARR)
- Add custom metrics on the fly
- Parallel processing for multiple documents
- Clear success/error reporting per file
- Export results as CSV

## Project Structure

portfolio-metrics-assistant/
├── app.py # Streamlit UI
├── extractor.py # PDF parsing + LLM extraction logic
├── requirements.txt
├── .env.example
└── README.md

## Running It Locally

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your OpenAI API key:
.env
OPENAI_API_KEY=

Then run the app:

```bash
streamlit run app.py
```

Notes on Accuracy and Tradeoffs

- This tool makes tradeoffs intentionally.

- LLMs can be wrong. I added basic validation and failure visibility, but this does not guarantee correctness.

- Different companies report metrics differently. Sometimes the data just isn’t there.

- The system prefers failing clearly over silently returning garbage.

If you’re using this for anything important, you should always validate the outputs against the source documents.

## Limitations

- No OCR for scanned PDFs

- No caching or retries

- No authentication

- Single model, no fallback

- Local use only

## What I Learned

This project reinforced something I already suspected: using AI responsibly is mostly about everything around the model. Input quality, constraints, validation, and knowing when not to trust the output matter more than model choice.

It also reminded me how much I enjoy building small, practical tools that sit between messy real-world inputs and structured data people can actually use.
