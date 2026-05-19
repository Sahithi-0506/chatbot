import os
from typing import List
import fitz  # PyMuPDF
import pdfplumber
from langchain_core.documents import Document


def extract_text_blocks(pdf_path: str) -> List[Document]:
    docs = []
    file_name = os.path.basename(pdf_path)
    pdf = fitz.open(pdf_path)

    for page_index, page in enumerate(pdf, start=1):
        text = page.get_text("text")
        if text and text.strip():
            docs.append(Document(
                page_content=text.strip(),
                metadata={
                    "file_name": file_name,
                    "page": page_index,
                    "content_type": "text"
                }
            ))
    pdf.close()
    return docs


def extract_tables(pdf_path: str) -> List[Document]:
    docs = []
    file_name = os.path.basename(pdf_path)

    with pdfplumber.open(pdf_path) as pdf:
        for page_index, page in enumerate(pdf.pages, start=1):
            tables = page.extract_tables() or []
            for table_index, table in enumerate(tables, start=1):
                rows = []
                for row in table:
                    clean_row = [str(cell).strip() if cell else "" for cell in row]
                    rows.append(" | ".join(clean_row))
                table_text = "\n".join(rows)
                if table_text.strip():
                    docs.append(Document(
                        page_content=f"Table {table_index}:\n{table_text}",
                        metadata={
                            "file_name": file_name,
                            "page": page_index,
                            "content_type": "table",
                            "table_index": table_index
                        }
                    ))
    return docs


def extract_image_placeholders(pdf_path: str) -> List[Document]:
    """
    This detects images and stores image metadata.
    For actual image understanding, connect Gemini Vision/OCR later and replace
    the placeholder with an image description.
    """
    docs = []
    file_name = os.path.basename(pdf_path)
    pdf = fitz.open(pdf_path)

    for page_index, page in enumerate(pdf, start=1):
        images = page.get_images(full=True)
        for image_index, _ in enumerate(images, start=1):
            docs.append(Document(
                page_content=(
                    f"Image detected in {file_name}, page {page_index}, image {image_index}. "
                    "Image description is not generated yet. Add OCR/Gemini Vision for full understanding."
                ),
                metadata={
                    "file_name": file_name,
                    "page": page_index,
                    "content_type": "image",
                    "image_index": image_index
                }
            ))
    pdf.close()
    return docs


def load_pdf_documents(pdf_path: str) -> List[Document]:
    documents = []
    documents.extend(extract_text_blocks(pdf_path))
    documents.extend(extract_tables(pdf_path))
    documents.extend(extract_image_placeholders(pdf_path))
    return documents


def load_all_pdfs(pdf_dir: str) -> List[Document]:
    all_docs = []
    for file in os.listdir(pdf_dir):
        if file.lower().endswith(".pdf"):
            all_docs.extend(load_pdf_documents(os.path.join(pdf_dir, file)))
    return all_docs
