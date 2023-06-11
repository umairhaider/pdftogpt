# PDF-to-GPT FastAPI App (Backend)

PDF-to-GPT is a FastAPI application that leverages OpenAI's GPT model to generate summaries and answer questions based on uploaded PDF documents. This application also generates PowerPoint Presentation for the PDF you uploaded. This is the Backend part of the application.

## Features

- Upload a PDF document and get a summary generated by ChatGPT.
- Ask questions about the uploaded PDF and get answers generated by GPT-3.
- Get a PowerPoint Presentation for the PDF you uploaded in seconds.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/umairhaider/pdftogpt.git
   
2. Install the dependencies
   ```bash
   pip install -r requirements.txt


## Usage

1. Rename .env-temp to .env and put your OpenAI API keys and other relevant environment variables. These are only used for development environment. The actual Production CI secrets and variables are stored in Github Actions.

2. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload

3. Open your browser and navigate to http://localhost:8000 to access the application.

4. Running the tests:

   ```bash
   pytest -m order

## API Endpoints

1. POST api/v1/signin/: Get JWT tokens to access the other endpoints.
2. POST api/v1/upload_pdf/: Upload a PDF file to generate a summary.
3. POST api/v1/ask_question/: Ask a question about the uploaded PDF and get an answer.
2. POST api/v1/get_presentation/: Generates PowerPoint Presention for the PDF you uploaded.

## Technologies Used

1. FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
2. PDFPlumber: A library for extracting text from PDF files.
3. OpenAI: GPT language model for generating text.

## Contributing

Contributions are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request.

## Code Contribution rules

Git commit message should follow the following rules:

Add the following approved tags while pushing the commits:

feat – a new feature is introduced with the changes
fix – a bug fix has occurred
chore – changes that do not relate to a fix or feature and don't modify src or test files (for example updating dependencies)
refactor – refactored code that neither fixes a bug nor adds a feature
docs – updates to documentation such as a the README or other markdown files
style – changes that do not affect the meaning of the code, likely related to code formatting such as white-space, missing semi-colons, and so on.
test – including new or correcting previous tests
perf – performance improvements
ci – continuous integration related
build – changes that affect the build system or external dependencies
revert – reverts a previous commit
example: feat: add JWT headers to login API fix: bug preventing Firefox users to login

Merge and PR: Before creating a PR squash all the commits into one.

## License

This project is licensed under the MIT License.

