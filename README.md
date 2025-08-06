# Template Conformance Checker

[![Built with spaCy](https://img.shields.io/badge/built%20with-spaCy-09a3d5.svg)](https://spacy.io)

## About the Project

This project provides a REST API for checking the conformance of requirement statements against predefined templates. It is a Python implementation based on the research paper: **"Automated Checking of Conformance to Requirements Templates Using Natural Language Processing"** by C. Arora, M. Sabetzadeh, L. C. Briand, and F. Zimmer (IEEE Trans. Software Eng. 2015).

You can read the full paper [here](https://people.svv.lu/sabetzadeh/pub/TSE15.pdf).

The goal of this tool is to help software engineers and requirement analysts write high-quality requirements by ensuring they adhere to proven structures.

### Features

-   **REST API:** Easily integrate conformance checking into your own tools and workflows.
-   **Multiple Templates:** Supports three popular requirement templates:
    -   Rupp
    -   EARS (Easy Approach to Requirements Syntax)
    -   Agile User Stories
-   **NLP-Powered:** Uses [spaCy](httpss://spacy.io) for natural language processing to parse and analyze requirement text.

## Getting Started

Follow these instructions to get a local copy up and running.

### Prerequisites

-   Python 3.6+

### Installation

1.  **Clone the repository:**
    ```sh
    git clone <repo-url>
    cd template-conformance
    ```

2.  **Install the dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Download the spaCy language model:**
    ```sh
    python -m spacy download en_core_web_sm
    ```

## Usage

To start the API server, run the following command from the root of the project directory:

```sh
python api_engine.py
```

The server will start on `http://localhost:5000`.

You can then send POST requests to the `/conformance` endpoint to check your requirements.

### Examples

Here are some examples using `curl`.

#### Rupp Template

**Compliant Example:**

```sh
curl -X POST -H "Content-Type: application/json" \
-d '{
    "conformance": "rupp",
    "requirements": "The Surveillance and Tracking module shall provide the system administrator with the ability to monitor system configuration changes posted to the database."
}' \
http://localhost:5000/conformance
```

**Expected Response:**

```json
[
    "<True>The Surveillance and Tracking module shall provide the system administrator with the ability to monitor system configuration changes posted to the database.</True>"
]
```

**Non-Compliant Example:**

```sh
curl -X POST -H "Content-Type: application/json" \
-d '{
    "conformance": "rupp",
    "requirements": "The information technology tools used in the design of systems performing safety functions shall be assessed for safety implications on the end-product."
}' \
http://localhost:5000/conformance
```

**Expected Response:**

```json
[
    "<False>The information technology tools used in the design of systems performing safety functions shall be assessed for safety implications on the end-product.</False>"
]
```

#### EARS Template

*(You can add an EARS example here if you have one)*

#### Agile Story Template

*(You can add an Agile Story example here if you have one)*

## API Reference

### `POST /conformance`

Checks a requirement string for conformance against a specified template.

**Request Body:**

-   `conformance` (string, required): The template to check against. Must be one of `rupp`, `ears`, or `agile`.
-   `requirements` (string, required): The requirement text to check. The text can contain multiple sentences, which will be checked individually.

**Success Response (200 OK):**

Returns a JSON array of strings. Each string is the original requirement sentence wrapped in a tag indicating its conformance status (`<True>` or `<False>`).

**Error Responses:**

-   `400 Bad Request`: If the request JSON is invalid or missing required fields.
-   `400 Bad Request`: If the `conformance` value is not one of the valid options.
-   `400 Bad Request`: If the `requirements` string is empty.

## Disclaimer

Use at your own peril. This is a quick and dirty implementation and may not be suitable for production use.

## License

Just make sure to attribute me/my work.