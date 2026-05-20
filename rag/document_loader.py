import os
from typing import List

import fitz  # PyMuPDF
import pdfplumber

from langchain_core.documents import Document


# =========================
# TEXT EXTRACTION
# =========================

def extract_text_blocks(pdf_path: str) -> List[Document]:
    docs = []

    file_name = os.path.basename(pdf_path)

    pdf = fitz.open(pdf_path)

    for page_index, page in enumerate(pdf, start=1):

        text = page.get_text("text")

        if text and text.strip():

            docs.append(
                Document(
                    page_content=text.strip(),

                    metadata={
                        "file_name": file_name,
                        "page": page_index,
                        "content_type": "text"
                    }
                )
            )

    pdf.close()

    return docs


# =========================
# TABLE EXTRACTION
# =========================

def extract_tables(pdf_path: str) -> List[Document]:

    docs = []

    file_name = os.path.basename(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:

        for page_index, page in enumerate(pdf.pages, start=1):

            tables = page.extract_tables() or []

            for table_index, table in enumerate(tables, start=1):

                rows = []

                for row in table:

                    clean_row = [
                        str(cell).strip() if cell else ""
                        for cell in row
                    ]

                    rows.append(" | ".join(clean_row))

                table_text = "\n".join(rows)

                if table_text.strip():

                    docs.append(
                        Document(
                            page_content=f"Table {table_index}:\n{table_text}",

                            metadata={
                                "file_name": file_name,
                                "page": page_index,
                                "content_type": "table",
                                "table_index": table_index
                            }
                        )
                    )

    return docs


# =========================
# OPTIONAL IMAGE EXTRACTION
# =========================
# We are NOT storing image placeholders now
# because they disturb retrieval quality.
#
# Later:
# - OCR
# - Gemini Vision
# - Image Captioning
#
# can be added here.


# =========================
# LOAD SINGLE PDF
# =========================

def load_pdf_documents(pdf_path: str) -> List[Document]:

    documents = []

    # Extract normal text
    documents.extend(extract_text_blocks(pdf_path))

    # Extract tables
    documents.extend(extract_tables(pdf_path))

    # IMAGE PLACEHOLDERS REMOVED

    return documents


# =========================
# LOAD ALL PDFs
# =========================

def load_all_pdfs(pdf_dir: str) -> List[Document]:

    all_docs = []

    for file in os.listdir(pdf_dir):

        if file.lower().endswith(".pdf"):

            pdf_path = os.path.join(pdf_dir, file)

            all_docs.extend(
                load_pdf_documents(pdf_path)
            )

    return all_docs