import PyPDF2

import config as cf
from algorithms.pdf_parser import extract_data, check_filepath


def extract_toc(pages: dict, toc_range: list) -> dict:
    return {}


def create_hyperlinks_for_existing_toc_not_scan(filepath: str, toc: dict, toc_range: list) -> None:
    pass


def insert_exsisting_toc_for_scan(filepath: str, toc: str, toc_range: list):
    pass


def create_toc_not_exist(pages: str) -> dict:
    return {}


def insert_toc(filepath: str, toc: dict, page_number: int = 2) -> None:
    pass


def toc_process_pdf_file(filepath: str):
    extracted_text = extract_data(filepath)

    if extracted_text['has_toc'] and extracted_text['has_hyperlinks']:
        return
    
    if extracted_text['has_toc']:
        toc = extract_toc(extracted_text['pages'], extracted_text['toc_range'])

        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            page = reader.pages[extracted_text['toc_range'][0]]
            text = page.extract_text()
            if text and text.strip(): 
                create_hyperlinks_for_existing_toc_not_scan(filepath, toc, extracted_text['toc_range'])
            else:
                insert_exsisting_toc_for_scan(filepath, toc, extracted_text['toc_range'])
        return

    toc = create_toc_not_exist(extracted_text['pages'])
    insert_toc(filepath, toc)
