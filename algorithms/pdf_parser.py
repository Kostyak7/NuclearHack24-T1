import re
import fitz 
import torch
import PyPDF2
import pytesseract
from pathlib import Path
from pdf2image import convert_from_path

from .models_cltok import search_toc_classifier, search_toc_tokenizer
from . import config as cf


# pytesseract.pytesseract.tesseract_cmd = cf.TESSERACT_CMD


def check_filepath(filepath: str, suffix: str = ".pdf") -> bool:
    if len(filepath) == 0:
        return False
    filepath = Path(filepath)
    return filepath.exists() and filepath.is_file() and filepath.suffix == suffix


def check_text(text: str) -> bool:
    text_striped = text.strip()
    return len(text_striped) > 1 and not text_striped.isdigit()


def parse_page_to_text(page, page_num: int, filepath: str, lang: str = "rus") -> str:
    text = page.extract_text()
    if text and text.strip():
        return text if check_text(text) else "" 
    
    ocr_text = ""
    images = convert_from_path(filepath, first_page=page_num, last_page=page_num)
    for image in images:
        ocr_text += pytesseract.image_to_string(image, lang=lang)  
    return ocr_text if check_text(ocr_text) else ""


def full_parse_pdf(filepath: str, lang: str = "rus") -> dict:    
    parsed_text = {}
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            parsed_text[page_num + 1] = parse_page_to_text(page, page_num=page_num + 1, filepath=filepath, lang=lang)

    return parsed_text


def extract_links_from_pdf(filepath: str, toc_pages: list) -> dict:
    if len(toc_pages) < 2 or toc_pages[0] is None or toc_pages[1] is None:
        return {}
    
    doc = fitz.open(filepath)
    if len(doc) < toc_pages[1]:
        doc.close()
        return {}
    
    links = {}
    for page_num in range(toc_pages[0], toc_pages[1] + 1):
        page = doc.load_page(page_num)
        link_list = page.get_links()

        if link_list:
            links[page_num + 1] = link_list 

    doc.close()
    return links


def is_table_of_contents(text: str) -> bool:
    upbound = min(len(text), 512)
    input = search_toc_tokenizer([text[:upbound]], truncation=True, padding=True, return_tensors='pt')
    with torch.no_grad():
        logits = search_toc_classifier(**input).logits

    predictions = torch.argmax(logits, dim=-1)

    for pred in predictions:
        if pred.item():
            return True
        pattern = re.compile(r'^\s*(' + '|'.join(re.escape(word) for word in cf.TOC_SEARCH_KEYWORDS) + r')\s*$', re.MULTILINE)
        return bool(pattern.search(text.lower()))


def detect_toc_in_file(pages: dict) -> list:
    toc_pages = [None] * 2
    
    for page_num, text in pages.items():
        if is_table_of_contents(text):
            if toc_pages[0] == None:
                toc_pages[0] = page_num    
            toc_pages[1] = page_num
        elif toc_pages[1] is not None and page_num > toc_pages[1]:
            break
    
    return toc_pages


def full_extract_data(filepath: str, lang: str = "rus") -> dict:
    if not check_filepath(filepath):
        return None
    
    parsed_text = full_parse_pdf(filepath, lang=lang)
    toc = detect_toc_in_file(parsed_text)
    hyperlinks = extract_links_from_pdf(filepath, toc)

    return {
        'pages': parsed_text,
        'has_toc':  toc[0] is not None,
        'toc_range': toc,
        'has_hyperlinks': len(hyperlinks) > 0
    }


def fast_extract_data(filepath: str, lang: str = "rus", hints: dict = {}) -> dict:
    parsed_text = {}

    if "has_toc" in hints and hints["has_toc"] and "toc_range" in hints:
        toc_pages = hints["toc_range"]

        is_correct_hint = True
        for page_num in range(toc_pages[0], toc_pages[1] + 1):
            page = reader.pages[page_num]
            parsed_text[page_num + 1] = parse_page_to_text(page, page_num=page_num + 1, filepath=filepath, lang=lang)

            if not is_table_of_contents(parsed_text[page_num + 1]):
                is_correct_hint = False

        if is_correct_hint:
            hyperlinks = extract_links_from_pdf(filepath, toc_pages)
            return {
                'pages': parsed_text,
                'has_toc':  True,
                'toc_range': toc_pages,
                'has_hyperlinks': len(hyperlinks) > 0
            }
    
    toc_pages = [None] * 2
    with open(filepath, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        pages_amount = len(reader.pages)
        pages_amount_div_4 = pages_amount // 4

        for page_num in range(pages_amount):
            page = reader.pages[page_num]
            parsed_text[page_num + 1] = parse_page_to_text(page, page_num=page_num + 1, filepath=filepath, lang=lang)
            
            if page_num <= pages_amount_div_4 or page_num >= pages_amount - pages_amount_div_4:
                if is_table_of_contents(parsed_text[page_num + 1]):
                    if toc_pages[0] == None:
                        toc_pages[0] = page_num + 1
                    toc_pages[1] = page_num + 1
                elif toc_pages[1] is not None and page_num + 1 > toc_pages[1]:
                    break
    
    hyperlinks = extract_links_from_pdf(filepath, toc_pages)

    return {
        'pages': parsed_text,
        'has_toc':  toc_pages[0] is not None,
        'toc_range': toc_pages,
        'has_hyperlinks': len(hyperlinks) > 0
    }
