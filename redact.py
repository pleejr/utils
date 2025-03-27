import pymupdf
from sensitive_values import redaction_words
import tkinter as tk
from tkinter import filedialog
import pytesseract

tessdatapath = "C:/Program Files/Tesseract-OCR/tessdata"

def select_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file.")
    return file_path

def redact_text(pdf_path, output_postfix, words_to_redact):
    doc = pymupdf.open(pdf_path)
    for page in doc.pages():
        ocr_page = page.get_textpage_ocr(tessdata=tessdatapath)
        for word in words_to_redact:
            areas = ocr_page.search(word)
            for area in areas:
                page.add_redact_annot(area, fill=(0, 0, 0))
        page.apply_redactions()

    output_path = pdf_path[:-4] + output_postfix + ".pdf"
    doc.save(output_path)
    print(f"Redacted PDF saved at: {output_path}")

redact_text(select_file(), "_redacted", redaction_words)
