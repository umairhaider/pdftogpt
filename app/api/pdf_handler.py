import logging
import pdfplumber
from fastapi import HTTPException
from app.utils.openai_utils import generate_chatgpt_response, clean_text
from app.api.context_handler import set_context

async def upload_pdf(file):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a PDF file.")

    try:
        with pdfplumber.open(file.file) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                else:
                    logging.warning("A page could not be processed and was skipped.")

            text = clean_text(text)
            text = "Give me a summary of this PDF document only in English. Here is the text from a PDF document: " + text
            if len(text) > 4096:
                batch_size = 4000  # Adjust the batch size as needed
                batches = [text[i:i + batch_size] for i in range(0, len(text), batch_size)]
                generated_text = ""
                for batch in batches:
                    generated_text += generate_chatgpt_response(batch)
            else:
                generated_text = generate_chatgpt_response(text)

            set_context(clean_text(generated_text))  # Store the generated text as the PDF context

            return {"text": text, "generated_text": generated_text}
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))