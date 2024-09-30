import os
import fitz
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from io import BytesIO

from . import config as cf
from .my_models.create_toc_model_training import generate_headline
from .pdf_parser import fast_extract_data, full_extract_data


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
                toc[line.strip()] = number_from_end
    return toc


def create_hyperlinks_for_existing_toc_not_scan(filepath: str, toc: dict, toc_range: list) -> None:
    doc = fitz.open(filepath)
    for page_num in range(toc_range[0] - 1, toc_range[1]):
        page = doc.load_page(page_num)
        blocks = page.get_text("blocks")
        for block in blocks:
            x1, y1, x2, y2, text, *_ = block
            lines = text.split('\n')

            y_offset = y1
            for line in lines:
                line_text = line.strip()
                if line_text in toc:
                    rect = (x1, y_offset, x2, y_offset + (y2 - y1) / len(lines))
                    page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "from": rect,  
                        "page": toc[line_text] - 1,
                    })
                y_offset += (y2 - y1) / len(lines)
    doc.save(filepath)
    doc.close()


# кажется на скан можно вставлять гиперссылку, но тогда придеться точно определять какую область текст занимает
def insert_exsisting_toc_for_scan(filepath: str, toc: str, toc_range: list):
    reader = PdfReader(filepath)
    writer = PdfWriter()
    for i in range(len(reader.pages)):
        if i < toc_range[0] - 1 or i > toc_range[1] - 1: 
            writer.add_page(reader.pages[i])

    os.remove(filepath)
    with open(filepath, "wb") as f:
        writer.write(f)
    insert_toc(filepath, toc, toc_range[0])


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
    linked_pages_filepath = os.path.splitext(file_path)[0] + cf.LINKED_PAGES_FILENAME_ADDITIVE + '.pfd'
    new_page_amount = 1
    c = canvas.Canvas(linked_pages_filepath)
    for link_text, page_num in toc.items():
        x, y = 100, 75 # todo перемещаться правильно
        if y > 500:
            y = 75
            new_page_amount += 1
        c.drawString(x, y, link_text)
        c.linkRect("", (x, y, x + 100, y + 10), destination=page_num - 1, relative=1)
    c.save()

    output_filepath = os.path.splitext(file_path)[0] + cf.OUTPUT_FILENAME_ADDITIVE + '.pfd'
    reader = PdfReader(filepath)
    writer = PdfWriter()

    page_counter = 0
    new_reader = PdfReader(linked_pages_filepath)
    for page in reader.pages:
        page_counter += 1
        if page_counter >= page_number and page_counter <= page_number + new_page_amount - 1:
            for i in len(new_page_amount):
                writer.add_page(new_reader.pages[i])
        writer.add_page(page)

    with open(output_filepath, "wb") as output_pdf:
        writer.write(output_pdf)


def toc_process_pdf_file(filepath: str, lang: str = 'rus', hints: dict = {}) -> None:
    extracted_text = fast_extract_data(filepath, lang=lang, hints=hints)
    print(extracted_text)
    if extracted_text is None:
        return

    if extracted_text['has_toc'] and extracted_text['has_hyperlinks']:
        return
    
    if extracted_text['has_toc']:
        toc = extract_toc(extracted_text['pages'], extracted_text['toc_range'])

        is_text = False
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            page = reader.pages[extracted_text['toc_range'][0]]
            text = page.extract_text()
            is_text = text and text.strip()
        if is_text:
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