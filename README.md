# template-conformance

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

A Python implementation for checking conformance to Requirements Templates (EARS, Rupp, Agile User Stories) using NLP (Spacy).

Based on the research paper:

> C. Arora, M. Sabetzadeh, L. C. Briand, F. Zimmer, “Automated Checking of Conformance to Requirements Templates Using Natural Language Processing”, IEEE Trans. Software Eng.41(10): 944-968 (2015)

## Features

- **EARS Compliance**: Checks if requirements follow the Easy Approach to Requirements Syntax.
- **Rupp Compliance**: Checks compliance with Rupp's templates.
- **Agile User Stories**: Validates standard user story formats.
- **REST API**: Exposes conformance checking via a Flask API.

## Quick Start

1.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    python -m spacy download en_core_web_sm
    ```

2.  **Run the API**:
    ```bash
    python api_engine.py
    ```

3.  **Check Conformance**:
    Send a POST request to `/conformance`:
    ```bash
    curl -X POST http://localhost:5000/conformance -d '{"conformance": "ears", "requirements": "The system shall do X when Y."}'
    ```

For more details, see the [Developer Guide](DEVELOPER_GUIDE.md).

## License

Please attribute the original work.