import os
from datetime import datetime

from pypdf import PdfReader, PdfWriter
import pandas as pd


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


current_time = datetime.now().strftime("%Y%m%d%H%M%S")

if not os.path.exists(f"output_{current_time}"):
    # If not, create it
    os.makedirs(f"output_{current_time}")


def log_message(message, log_file=f"log_{current_time}.txt"):
    with open(log_file, 'a') as log:
        log.write(message + '\n')

print("-------------------------")
print("Provide a valid CSV mapping file from which PDF field names will be generated.")
csv_mapping_file = get_filename("csv")

try:
    # Attempt to read the CSV file into a DataFrame
    df = pd.read_csv(csv_mapping_file)
    # If successful, print the first few rows of the DataFrame
    print("CSV file successfully loaded into DataFrame:")
    print(df.head())

except FileNotFoundError:
    print(f"Error: The file '{csv_mapping_file}' was not found. Please check the file path.")
except pd.errors.EmptyDataError:
    print(f"Error: The file '{csv_mapping_file}' is empty. Please provide a non-empty CSV file.")
except pd.errors.ParserError:
    print(f"Error: There was an issue parsing the CSV file '{csv_mapping_file}'. Please check the file format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

csv_columns = list(df.columns)
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

print("List of PDFs:", pdf_list)

for pdf in pdf_list:
    reader = PdfReader(pdf)
    fields = reader.get_fields()
    writer = PdfWriter()
    writer.append(reader)

    for field in fields:
        if field not in csv_columns:
            message = f"Warning: {field} not found in CSV columns for pdf {pdf}."
            print(message)
            log_message(message)

    for column in csv_columns:
        if column not in fields:
            message = f"Warning: {column} in CSV but not found in PDF fields for pdf {pdf}."
            print(message)
            log_message(message)

    for index, row in df.iterrows():
        for field in fields:
            if field in row:
                for page in writer.pages:
                    writer.update_page_form_field_values(
                        page, {field: row[field]}
                    )
            with open(f"output_{current_time}/{row[0]}.pdf", "wb") as output_stream:
                writer.write(output_stream)
