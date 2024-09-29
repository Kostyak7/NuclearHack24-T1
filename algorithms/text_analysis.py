import PyPDF2

import config as cf
from my_models.create_toc_model_training import generate_headline
from pdf_parser import full_extract_data, fast_extract_data, check_filepath


def extract_toc(pages: dict, toc_range: list) -> dict:
    return {}


def create_hyperlinks_for_existing_toc_not_scan(filepath: str, toc: dict, toc_range: list) -> None:
    pass


def insert_exsisting_toc_for_scan(filepath: str, toc: str, toc_range: list):
    pass


def create_toc_not_exist(pages: str, max_paragraph_number: int = 20, max_word_number: int = 1024, max_page_number: int = 2) -> dict:
    toc = {}

    # if 

    # if doesn`t exist clear structure
    last_page_num = 1
    accumulated_text = ''
    paragraphas_counter = 0
    word_counter = 0
    page_counter = 0
    for page_num, text in pages.items():
        page_counter += 1

        paragraphas = text.split('\n')
        for paragraph in paragraphas:
            if len(paragraph) == 0 or paragraph.isdigit() or paragraph.isdecimal() or len(paragraph) < 5:
                continue
            paragraphas_counter += 1
            len_splited_text = len(paragraph.split())
            word_counter += len_splited_text

            if paragraphas_counter > max_paragraph_number or word_counter > max_word_number or page_counter > max_page_number:
                accumulated_text += paragraph
                headline = generate_headline(accumulated_text, n_words=8)
                # print(headline, ":\n", accumulated_text, end="\n\n\n")
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


def insert_toc(filepath: str, toc: dict, page_number: int = 2) -> None:
    pass


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


if __name__ == "__main__":
    # file_path = cf.TEST_SCAN_NO_TOC_FILE_PATH
    # file_path = cf.TEST_SCAN_WITH_TOC_FILE_PATH
    file_path = cf.TEST_TEXT_NO_TOC_FILE_PATH
    # file_path = cf.TEST_TEXT_WITH_TOC_FILE_PATH

    toc_process_pdf_file(file_path)