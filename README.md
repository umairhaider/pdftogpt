# PDF-to-GPT FastAPI App (Backend)

PDF-to-GPT is a FastAPI application that leverages OpenAI's GPT model to generate summaries and answer questions based on uploaded PDF documents. This is the Backend part of the application.

## Features

- Upload a PDF document and get a summary generated by ChatGPT.
- Ask questions about the uploaded PDF and get answers generated by GPT-3.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/umairhaider/pdftogpt.git
   
2. Install the dependencies

   ```bash
   pip install -r requirements.txt

## Usage

1. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload

2. Open your browser and navigate to http://localhost:8000 to access the application.

## API Endpoints

1. POST /upload_pdf/: Upload a PDF file to generate a summary.
3. POST /ask_question/: Ask a question about the uploaded PDF and get an answer.

## Technologies Used

1. FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
2. PDFPlumber: A library for extracting text from PDF files.
3. OpenAI: GPT language model for generating text.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.

