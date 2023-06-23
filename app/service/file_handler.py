import os
import random
import string
from fastapi import UploadFile, File
from app.service.auth import get_current_user


async def upload_file(file: UploadFile = File(...)):
    # Generate a random string to append to the filename
    random_string = generate_random_string(5)
    
    # Get the file extension
    original_filename = os.path.splitext(file.filename)[0].replace(" ", "_")
    file_extension = os.path.splitext(file.filename)[1]

    # Construct the new filename
    new_filename = f"{original_filename}_{random_string}{file_extension}"

    # Create folder if it doesn't exist
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    
    # Save the file to the "uploads" folder
    save_path = os.path.join("uploads", new_filename)
    with open(save_path, "wb") as f:
        contents = await file.read()
        f.write(contents)
    return {file.filename}

def generate_random_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))