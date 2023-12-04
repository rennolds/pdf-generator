import os
import json
from pypdf import PdfReader, PdfWriter
from pypdf.generic import IndirectObject


def log_message(message, log_file):
    with open(log_file, 'a') as log:
        log.write(message + '\n')


def convert_to_serializable(obj):
    """Convert non-serializable objects to a serializable form."""
    if isinstance(obj, IndirectObject):
        # Extract relevant information or convert to a basic type
        return str(obj)
    # Add more conditions as needed for other non-serializable types

    # For other types, use the default JSON serialization
    return json.JSONEncoder.default(obj)


def get_filename(extension: str):
    while True:
        filename = input(f"What is name of the {extension} file?\n")

        if '.' in filename:
            if filename.endswith(f".{extension}"):
                print("Valid filename provided: " + filename + " thank you!")
                break
            else:
                print(f"Invalid extension. Please enter a file name ending with '.{extension}'.")
        else:
            print(f"No file extension found. Please enter a valid file name with a .{extension} extension.")
        
    return filename

pdf_list = []

while True:
    filename = get_filename("pdf")

    if os.path.isfile(filename):
        pdf_list.append(filename)
        print(f"{filename} added to the list.")
    else:
        print(f"Error: {filename} does not exist. Please enter a valid PDF filename.")

    another_file = input("Do you want to add another PDF? (yes/no): ").lower()
    if another_file != 'yes':
        break

for pdf in pdf_list:
    reader = PdfReader(pdf)
    fields = reader.get_fields()

    log_message(json.dumps(fields, default=convert_to_serializable), log_file=f"{pdf}.txt")
