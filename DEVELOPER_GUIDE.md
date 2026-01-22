# Developer Guide

Welcome to the `template-conformance` project! This guide will help you set up your development environment and understand the codebase.

## Prerequisites

- Python 3.8+
- pip

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd template-conformance
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Spacy Model**:
    The project uses the `en_core_web_sm` model.
    ```bash
    python -m spacy download en_core_web_sm
    ```

## Project Structure

-   `template_conformance_core.py`: The main entry point for conformance checking logic. It aggregates the different parsers.
-   `api_engine.py`: A Flask application exposing the conformance checking as a REST API.
-   `ears_template_conformance.py`: Logic for parsing and checking EARS template conformance.
-   `rupp_template_conformance.py`: Logic for parsing and checking Rupp template conformance.
-   `agile_user_story_conformance.py`: Logic for Agile User Story conformance.

## Running the API

```bash
python api_engine.py
```

The API will run on `http://localhost:5000`.

## JSON Input Format

The API expects a JSON payload:

```json
{
    "conformance": "ears",  // "ears", "rupp", or "agile"
    "requirements": "The system shall..."
}
```

## Running Tests

A verification script is provided:

```bash
python test_functionality.py
```
