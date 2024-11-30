# Flask PDF Processing Application

Welcome to the Flask PDF Processing Application repository! This project provides a set of APIs to process PDF documents, extract text, and answer questions based on the extracted content. The application is built using Python and Flask and integrates tools like TensorFlow for machine learning functionalities.

## Features

- **PDF Upload and Management**: Upload PDFs via URL and manage them.
- **Text Extraction**: Extract text content from uploaded PDFs.
- **Question-Answering**: Ask questions related to the content of PDFs and receive accurate answers.
- **Health Check**: Ensure the application is running smoothly with a simple ping endpoint.
- **Advanced AI Models**: Uses **BERT** for generating answers and ranking pages, and **ELMo** and **TF-IDF** for text processing and page ranking.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or later
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the configuration file:
   Create a `config.ini` file in the root directory with the following structure:
   ```ini
   [session]
   file_dir = ./text
   start_page = 1

   [admin]
   host = 127.0.0.1
   port = 5000
   ```

## Configuration

Ensure your `config.ini` file is properly configured. Update the `host` and `port` values as needed.

## API Documentation

### 1. **Health Check**
- **Endpoint**: `/quans/ping`
- **Method**: `GET`
- **Description**: Verifies that the application is running.
- **Response**: `successsss!!`

### 2. **Upload PDF**
- **Endpoint**: `/quans/upload_files`
- **Method**: `GET`
- **Query Parameters**:
  - `file`: URL of the PDF to upload.
- **Description**: Uploads a PDF file from the given URL.

### 3. **Get PDF Metadata**
- **Endpoint**: `/quans/pdf_files`
- **Method**: `GET`
- **Description**: Lists uploaded PDF files with their metadata.

### 4. **Ask Questions**
- **Endpoint**: `/quans/question_list/`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
      "question": "Your question here"
  }
  ```
- **Query Parameters**:
  - `pdf_list`: List of PDF IDs to query.
- **Response**:
  ```json
  {
      "res": ["Answer1", "Answer2"]
  }
  ```

## Usage

1. Start the Flask server:
   ```bash
   python app.py
   ```

2. Access the application using the specified host and port in your `config.ini`. By default, it runs at `http://127.0.0.1:5000`.

3. Use a tool like [Postman](https://www.postman.com/) or `curl` to test the APIs.

## Project Structure

```plaintext
.
├── app.py                    # Main Flask application
├── config.ini                # Configuration file
├── requirements.txt          # Dependencies
├── text/                     # Directory for text files
├── utils/                    # Utility functions
├── log/                      # Logs directory
└── README.md                 # Project README
```

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch-name`).
3. Make your changes and commit them (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch-name`).
5. Open a pull request.

 
 
---

Thank you for using this application! If you encounter any issues or have suggestions, feel free to open an issue or submit a pull request.
