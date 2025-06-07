# Verba Vita (Translation Service)

- Author: Thmsbgfrv
- Date: 27.12.2023

## Description

This service provides a JSON API to retrieve and manage word definitions/translations. It integrates with Google Translate to fetch the required data.

## Requirements

- Python 3.12.1
- FastAPI (async mode)
- Docker and docker compose
- NoSQL database , MongoDB

# Installation and Setup

### Docker

1.  Navigate to the project directory.
2.  Build and run the Docker container using the provided `Dockerfile` and `docker-compose.yml`:

```bash
docker compose up --build
```

## API Endpoints

### 1. Get Word Details

- **Endpoint**: `/word/{word}`
- **Description**: Retrieve details about a specific word including definitions, synonyms, translations, and examples.
- **Parameters**:
  - `word`: The word to fetch details for.
  - `source`: source language code (ex: en, tr, fr, es)
  - `to`: target language code (ex: en, tr, fr, es).
- example response

```json
{
  "word": "day",
  "sl": "en",
  "langs": {
    "es": {
      "translation": "día",
      "details": {
        "noun": {
          "0": {
            "explanation": "a period of twenty-four hours as a unit of time, reckoned from one midnight to the next, corresponding to a rotation of the earth on its axis.",
            "example": "they only met a few days ago",
            "synonym": ["solar day", "sidereal day"]
          },
          "1": {
            "explanation": "a particular period of the past; an era.",
            "example": "the laws were very strict in those days",
            "synonym": [
              "twenty-four-hour period",
              "full day",
              "twenty-four hours",
              "working day"
            ]
          }
        }
      }
    }
  },
  "definitions": {
    "noun": [
      "a period of twenty-four hours as a unit of time, reckoned from one midnight to the next, corresponding to a rotation of the earth on its axis.",
      "a particular period of the past; an era."
    ]
  },
  "examples": {
    "noun": [
      "they only met a few days ago",
      "the laws were very strict in those days"
    ]
  },
  "synonyms": {
    "noun": [
      "solar day",
      "sidereal day",
      "twenty-four-hour period",
      "full day",
      "twenty-four hours",
      "working day"
    ]
  }
}
```

### 2. List Stored Words

- **Endpoint**: `/words`
- **Description**: Retrieve a paginated list of words stored in the database.
- **Optional Query Parameters**:
  - `page`: Page number for pagination.
  - `limit`: Number of words per page.
  - `word_filter`: keyword for partial match.
  - `definitions`: true/false as value for show/hide data.
  - `examples`: true/false as value for show/hide data.
  - `synonyms`: true/false as value for show/hide data.
- example request

```bash
curl -X 'GET' \
  'http://localhost:8000/words?page=1&limit=10&word_filter=ay&definitions=true&examples=true&synonyms=true' \
  -H 'accept: application/json'
```

- example response

```json
{
  "total_count": 1,
  "words": [
    {
      "word": "day",
      "sl": "en",
      "definitions": {
        "noun": [
          "a period of twenty-four hours as a unit of time, reckoned from one midnight to the next, corresponding to a rotation of the earth on its axis.",
          "a particular period of the past; an era."
        ]
      },
      "synonyms": {
        "noun": [
          "solar day",
          "sidereal day",
          "twenty-four-hour period",
          "full day",
          "twenty-four hours",
          "working day"
        ]
      },
      "examples": {
        "noun": [
          "they only met a few days ago",
          "the laws were very strict in those days"
        ]
      }
    }
  ]
}
```

### 3. Delete Word

- **Endpoint**: `/word/{word}`
- **Description**: Delete a word and its associated details from the database.
- **Parameters**:
  - `word`: The word to delete.
- example response

```json
{
  "message": "Word 'claim' deleted successfully."
}
```

## Database

Data fetched from Google Translate is saved in a MongoDB database. When a request arrives, the handler first looks for the word in the database and falls back to Google Translate only if it is not found.

## Authentication

Authentication is not required for accessing the API.

## GoogleTranslator Library

This library is writen by me for providing needed data like definitions, synonyms so on. It's open to develeopment. It can optimize more, and it can provide more data than current ones. But nevertheless I am writing this in short amount of period it works perfect.

## Known Flaws and Improvements

1.  **Data Consistency**: There might be discrepancies between Google Translate and the saved data in the database due to caching or outdated translations.
2.  **Error Handling**: Enhanced error handling can be implemented to provide more descriptive error messages and handle various edge cases.
3.  **Caching**: Implement caching mechanisms to reduce the number of requests to Google Translate and improve performance.
4.  **Rate Limiting**: Consider implementing rate limiting to prevent abuse and ensure fair usage of the service.
5.  **Security**: Implement security best practises, authentication and autherization can make project more safe.
6.  **Tests**: It must be added tests for endpoint tests, unit tests for custom libraries are crucial for that project and for development.
