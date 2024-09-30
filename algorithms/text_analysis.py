from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

import config as cf
from my_models.create_toc_model_training import generate_headline
from pdf_parser import full_extract_data, fast_extract_data, check_filepath



def extract_number_from_end(text: str) -> int:
    text = text.rstrip()
    number_str = ""
    for char in reversed(text):
        if char.isdigit():
            number_str = char + number_str
        else:
            break
    return int(number_str) if number_str else None


def extract_toc(pages: dict, toc_range: list) -> dict:
    toc = {}

    for i in range(toc_range[0], toc_range[1] + 1):
        lines = pages[i].spltlines()
        for line in lines:
            number_from_end = extract_number_from_end(line)
            if line is not None:
                toc[line] = number_from_end
    return toc


def create_hyperlinks_for_existing_toc_not_scan(filepath: str, toc: dict, toc_range: list) -> None:
    pass


def insert_exsisting_toc_for_scan(filepath: str, toc: str, toc_range: list):
    pass


def try_extract_structure(pages: dict) -> dict:
    toc = {}

    for page_num, text in pages.items():
        lines = text.splitlines()
        for line in lines:
            stripped_line = line.strip()
            first_word = stripped_line.split()[0] if stripped_line else ""
            if first_word.lower() in cf.KEY_STRUCTURE_WORDS:
                toc[stripped_line] = page_num

    return toc if len(toc) > 1 else None


def text_tiling_toc_generating(pages: dict) -> dict:
    toc = {}
    return toc


def t5_toc_generating(pages: dict, max_paragraph_number: int = 20, max_word_number: int = 1024, max_page_number: int = 2) -> dict:
    toc = {}
    last_page_num = 1
    accumulated_text = ''
    paragraphas_counter = 0
    word_counter = 0
    page_counter = 0
    for page_num, text in pages.items():
        page_counter += 1

        paragraphas = text.splitlines()
        for paragraph in paragraphas:
            if len(paragraph) == 0 or paragraph.isdigit() or paragraph.isdecimal() or len(paragraph) < 5:
                continue
            paragraphas_counter += 1
            len_splited_text = len(paragraph.split())
            word_counter += len_splited_text

            if paragraphas_counter > max_paragraph_number or word_counter > max_word_number or page_counter > max_page_number:
                accumulated_text += paragraph
                headline = generate_headline(accumulated_text, n_words=8)
                if len(headline) > 0:
                    toc[headline] = last_page_num

                paragraphas_counter = 0
                word_counter = 0
                page_counter = 1
                accumulated_text = ''
                last_page_num = page_num
            else:
                accumulated_text += paragraph
    
    for header, page_num in toc.items():
        if len(header) > 160:
            print(f'{header}.........{page_num}')
        else:
            print(header, '.' * (160 - len(header)), page_num, sep='')
    return toc


def create_toc_not_exist(pages: str) -> dict:
    toc = try_extract_structure(pages)
    if toc is not None:
        return toc
        
    toc = text_tiling_toc_generating(pages)
    if toc is not None:
        return toc

    return t5_toc_generating(pages)


def create_pdf_page(text: str) -> PdfReader:
    packet = BytesIO()
    c = canvas.Canvas(packet)
    c.drawString(100, 750, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)


def insert_toc(filepath: str, toc: dict, page_number: int = 2) -> None:
    output_filepath = file_path + cf.OUTPUT_FILENAME_ADDITIVE
    reader = PdfReader(filepath)
    writer = PdfWriter()

    # Создание новой страницы с текстом
    new_page = create_pdf_page(text)

    for i in range(len(reader.pages) + 1):
        if i == page_number:
            writer.add_page(new_page)
        if i < len(reader.pages):
            writer.add_page(reader.pages[i])

    with open(output_filepath, "wb") as output_pdf:
        writer.write(output_pdf)


def toc_process_pdf_file(filepath: str):
    extracted_text = fast_extract_data(filepath)
    print(extracted_text)
    if extracted_text is None:
        return

    if extracted_text['has_toc'] and extracted_text['has_hyperlinks']:
        return
    
    if extracted_text['has_toc']:
        toc = extract_toc(extracted_text['pages'], extracted_text['toc_range'])

        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            page = reader.pages[extracted_text['toc_range'][0]]
            text = page.extract_text()
            if text and text.strip(): 
                create_hyperlinks_for_existing_toc_not_scan(filepath, toc, extracted_text['toc_range'])
            else:
                insert_exsisting_toc_for_scan(filepath, toc, extracted_text['toc_range'])
        return

    toc = create_toc_not_exist(extracted_text['pages'])
    insert_toc(filepath, toc)


if __name__ == "__main__":
    # file_path = cf.TEST_SCAN_NO_TOC_FILE_PATH
    # file_path = cf.TEST_SCAN_WITH_TOC_FILE_PATH
    file_path = cf.TEST_TEXT_NO_TOC_FILE_PATH
    # file_path = cf.TEST_TEXT_WITH_TOC_FILE_PATH

    toc_process_pdf_file(file_path)