import pdfplumber
import os
from config import PDF_DIR, TEXT_DIR

pdf_directory = PDF_DIR
txt_directory = TEXT_DIR

os.makedirs(txt_directory, exist_ok=True)

for filename in sorted(os.listdir(pdf_directory)):
    chapter_number = filename.split("Chapter ")[1].split(" –")[0]
    output_filename = f"chapter_{chapter_number.zfill(2)}.txt"

    with pdfplumber.open(os.path.join(pdf_directory, filename)) as pdf:
        pages = []
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)

        full_text = "\n\n".join(pages)

    with open(os.path.join(txt_directory, output_filename), "w", encoding="utf-8") as f:
        f.write(full_text)

print("Done.")