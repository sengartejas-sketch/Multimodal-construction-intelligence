# Multimodal Construction Intelligence Platform

A student capstone prototype built with Python and Streamlit.

## Features
- Site Safety & PPE Audit using an image-capable Gemini model
- Preliminary Crack Diagnostics using an uploaded image
- Illustrative construction budget and valuation calculations
- Weather-aware general site safety guidance
- Optional AI construction Q&A
- Downloadable JSON analysis reports

## Requirements
- Python 3.9 or newer (Python 3.11 or 3.12 recommended)
- Internet connection for installing packages and using Gemini
- Gemini API key for AI-powered image analysis and AI Q&A

## Run locally (Windows)
1. Extract this project folder.
2. Open Command Prompt in the extracted folder.
3. Create a virtual environment:
   `python -m venv .venv`
4. Activate it:
   `.venv\\Scripts\\activate`
5. Install packages:
   `python -m pip install -r requirements.txt`
6. Run:
   `streamlit run app.py`
7. Open the local URL printed in the terminal (usually http://localhost:8501).
8. Paste your Gemini API key into the password field in the sidebar when you want to use AI features.

## Deploy to Streamlit Community Cloud
1. Create a GitHub repository and upload `app.py`, `ai_analyzer.py`, `requirements.txt`, and this README.
2. On Streamlit Community Cloud, create an app from that repository and select `app.py`.
3. Deploy and test the app.
4. Do not commit API keys or secrets to GitHub.

## Limitations
- AI analysis is preliminary and may be wrong.
- Crack width cannot be reliably measured from a photo without a known scale.
- Cost estimates use user-provided assumptions and are not professional valuations.
- This prototype is not a substitute for qualified safety or structural engineering advice.
- Verify model availability and current Google Gen AI SDK guidance if the configured model is unavailable.
