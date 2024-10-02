import os
import re
import fitz
import torch
from math import ceil
from PyPDF2 import PdfReader, PdfWriter

from . import config as cf
from .models_cltok import search_title_classifier, search_title_tokenizer
from .my_models.create_toc_model import generate_headline, text_tiling
from .pdf_parser import fast_extract_data, full_extract_data, parse_page_to_text, check_filepath


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
        lines = pages[i].splitlines()
        for line in lines:
            number_from_end = extract_number_from_end(line)
            if line is not None and len(line) and number_from_end is not None:
                toc[line.strip()] = number_from_end
    return toc


def create_hyperlinks_for_existing_toc_not_scan(filepath: str, toc: dict, toc_range: list) -> None:
    output_filepath = os.path.splitext(filepath)[0] + cf.OUTPUT_FILENAME_ADDITIVE + '.pdf'
    doc = fitz.open(filepath)
    for page_num in range(toc_range[0] - 1, toc_range[1]):
        page = doc.load_page(page_num)
        blocks = page.get_text("dict")["blocks"]
        c = 0
        for block in blocks:
            c += 1
            if c < 2 or "lines" not in block:
                continue
            for line in block["lines"]:
                y1 = line["bbox"][1]
                y2 = line["bbox"][3]
                
                line_text = "".join(span["text"] for span in line["spans"]).strip()
                
                if line_text in toc and toc[line_text] <= doc.page_count:
                    rect = fitz.Rect(block["bbox"][0], y1, block["bbox"][2], y2)
                    page.insert_link({
                        "kind": fitz.LINK_GOTO,
                        "from": rect,
                        "page": toc[line_text] - 1,
                    })
        
    doc.save(output_filepath)
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


def roman_to_arabic(roman: str) -> int:
    roman_to_arabic_map = { 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
    total = 0
    prev_value = 0
    for char in reversed(roman):
        value = roman_to_arabic_map[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value
    return total


def is_roman(roman: str) -> bool:
    roman_to_arabic_map = { 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000 }
    return all(char in roman_to_arabic_map for char in roman)


def replace_roman_with_arabic(text: str) -> str:
    if '.' not in text:
        return text
    before_dot = text.split('.')[0].strip()    

    if is_roman(before_dot):
        arabic_value = roman_to_arabic(before_dot)
        new_text = text.replace(before_dot, str(arabic_value))
        return new_text
    else:
        return text 


def try_extract_structure(pages: dict) -> dict:
    toc = {}
    num_pattern = re.compile(r'^(?P<number>\d+(\.\d+)*)\.\s+(?P<text>[^.!?,]*[a-zA-Zа-яА-Я])$')
    kw_pattern = re.compile(r'^[\w\s]+$')
    prev_number = [0]

    for page_num, text in pages.items():
        lines = text.splitlines()
        for line in lines:
            stripped_line = line.strip()
            non_arabic_line = replace_roman_with_arabic(stripped_line)
            match_str = num_pattern.match(non_arabic_line)
            if match_str:
                cur_number = list(map(int, match_str.group(1).split('.')))
                if cur_number and cur_number > prev_number:
                    prev_number = cur_number
                    toc[stripped_line] = page_num
            
            first_word = stripped_line.split()[0] if stripped_line else ""
            if (stripped_line.lower() in cf.KEY_STRUCTURE_WORDS or first_word.lower() in cf.KEY_STRUCTURE_WORDS_ALONE) and kw_pattern.match(stripped_line):
                toc[stripped_line] = page_num
    return toc if len(toc) > 1 else None


def text_tiling_toc_generating(pages: dict) -> dict:
    toc = {}
    text = ""
    for page_num, page_text in pages.items():
        if page_num < 5:
            if is_title_page(page_text):
                text += page_text            
        else:
            text += page_text

    segments = text_tiling(text, block_size=2, threshold=0.15)
    segment_index = 0
    for page_num, page_text in pages.items():
        if segments[segment_index][:min(len(segments[segment_index]), 40)] in page_text:
            chapter = generate_headline(segments[segment_index], n_words=8,)
            toc[chapter] = page_num
            segment_index += 1
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

    return toc


def create_toc_not_exist(pages: str) -> dict:
    toc = try_extract_structure(pages)
    if toc is not None:
        return toc
    
    toc = text_tiling_toc_generating(pages)
    if toc is not None:
        return toc

    return t5_toc_generating(pages)


def split_text_into_lines(text: str, max_length: int = 100) -> list:
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_length:
            if current_line:
                current_line += " "  
            current_line += word
        else:
            lines.append(current_line) 
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def insert_toc(filepath: str, toc: dict, page_number: int = 2) -> None:
    linked_pages_filepath = os.path.splitext(filepath)[0] + cf.LINKED_PAGES_FILENAME_ADDITIVE + '.pdf'
    sample_doc = fitz.open()
    new_page_amount = ceil((len(toc) * (cf.DEFAULT_TEXT_SIZE + cf.DEFAULT_LINE_SPACING) + 200) / 860)
    for _ in range(new_page_amount):
        sample_doc.new_page()
    sample_doc.save(linked_pages_filepath)
    
    output_filepath = os.path.splitext(filepath)[0] + cf.OUTPUT_FILENAME_ADDITIVE + '.pdf'
    target_doc = fitz.open(filepath)
    target_doc.insert_pdf(sample_doc, from_page=0, to_page=new_page_amount - 1)
    sample_doc.close()
    for i in range(new_page_amount):
        target_doc.move_page(target_doc.page_count - new_page_amount + i, page_number - 1 + i)
    
    page_iter = page_number - 1
    cur_page = target_doc.load_page(page_iter)
    cur_page.insert_font(fontfile=cf.ARIAL_FONT_PATH, fontname="F0")
    # cur_page.insert_font(fontfile=cf.ARIAL_BOLD_FONT_PATH, fontname="F0_BOLD")
    cur_page.insert_text((80, 50), "Содержание", fontsize=cf.DEFAULT_HEADLINE_SIZE, fontname='F0')
    y_position = 100
    for chapter, page_num in toc.items():
        if page_num > target_doc.page_count:
            continue
        if y_position > 720:
            y_position = 70
            page_iter += 1
            cur_page = target_doc.load_page(page_iter)
            cur_page.insert_font(fontfile=cf.ARIAL_FONT_PATH, fontname="F0")
        start_y_position = y_position + 0
        for line in split_text_into_lines(chapter, max_length=70):
            cur_page.insert_text((50, y_position), line, fontsize=cf.DEFAULT_TEXT_SIZE, fontname="F0")
            y_position += cf.DEFAULT_TEXT_SIZE + 3
        y_position -= cf.DEFAULT_TEXT_SIZE + 3

        cur_page.insert_text((500, y_position), str(page_num), fontsize=cf.DEFAULT_TEXT_SIZE, fontname="F0")
        cur_page.insert_link({"kind": fitz.LINK_GOTO, "page": page_num - 1 + new_page_amount, "from": fitz.Rect(50, start_y_position - cf.DEFAULT_TEXT_SIZE - 2, 520, y_position + 2)})
        y_position += cf.DEFAULT_TEXT_SIZE + cf.DEFAULT_LINE_SPACING

    for pn in range(new_page_amount):
        page = target_doc.load_page(page_number - 1 + pn)
        page.insert_font(fontfile=cf.ARIAL_FONT_PATH, fontname="F0")
        page.insert_text((550, 800), str(page_number + pn), fontsize=8, fontname='F0')

    target_doc.save(output_filepath)
    target_doc.close()


def is_title_page(text: str) -> bool:
    upbound = min(len(text), 512)
    input = search_title_tokenizer([text[:upbound]], truncation=True, padding=True, return_tensors='pt')
    with torch.no_grad():
        logits = search_title_classifier(**input).logits

    predictions = torch.argmax(logits, dim=-1)

    for pred in predictions:
        return pred.item()


def detect_title_pages(filepath: str, lang: str = 'rus') -> int:
    last_title_page = 0
    with open(filepath, 'rb') as file:
        reader = PdfReader(file)

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            page_text = parse_page_to_text(page, page_num=page_num + 1, filepath=filepath, lang=lang)
            if is_title_page(page_text):
                last_title_page += 1
            else:
                break
    return last_title_page


def toc_process_pdf_file(filepath: str, lang: str = 'rus', hints: dict = {}) -> None:
    if not check_filepath(filepath):
        return
    extracted_text = fast_extract_data(filepath, lang=lang, hints=hints)
    print(extracted_text)
    if extracted_text is None:
        return

    if extracted_text['has_toc'] and extracted_text['has_hyperlinks']:
        return
    
    if extracted_text['has_toc']:
        toc = extract_toc(extracted_text['pages'], extracted_text['toc_range'])

        is_text = True
        with open(filepath, 'rb') as file:
            reader = PdfReader(file)
            for page_num in len(extracted_text['toc_range'][0], extracted_text['toc_range'][1] + 1):
                page = reader.pages[page_num]
                text = page.extract_text()
                is_text = text and text.strip() and is_text
        if is_text:
            create_hyperlinks_for_existing_toc_not_scan(filepath, toc, extracted_text['toc_range'])
        else:
            insert_exsisting_toc_for_scan(filepath, toc, extracted_text['toc_range'])
        return

    toc = create_toc_not_exist(extracted_text['pages'])
    insert_into = detect_title_pages(filepath, lang) + 1
    insert_toc(filepath, toc, page_number=insert_into)
