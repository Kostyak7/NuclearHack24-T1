import os
import PyPDF2
import pytesseract
from pathlib import Path
from pdf2image import convert_from_path

import training_config as tcf


def get_train_dataset_from_txt(folder_path: str, MAX_N: int = 200) -> list:
    if not Path(folder_path).exists():
        print("The path doesn't exist")
        return []

    labels = []  
    contents = [] 

    file_counter = 0
    for file_name in Path(folder_path).glob('*.txt'):
        print(file_name)
        if file_counter > MAX_N:
            break
        
        if file_name.is_file():
            with open(str(file_name), "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    if lines[0].strip().isdigit():
                        labels.append(int(lines[0].strip()))
                
                        remaining_content = "".join(lines[1:]).strip()
                        contents.append(remaining_content)

                        file_counter += 1
                    
    return [labels, contents]


def get_train_dataset_from_pdf(folder_path: str, lang: str = 'rus', MAX_N: int = 200) -> list:
    if not Path(folder_path).exists():
        print("The path doesn't exist")
        return []

    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

    result = []
    file_counter = 0
    for file_name in Path(folder_path).glob('*.pdf'):
        if file_name.is_file():
            parsed_text = ''
            with open(file_name, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                if reader.is_encrypted:
                    continue

                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]

                    text = page.extract_text()
                    if text and text.strip():  
                        parsed_text += text 
                    else:
                        images = convert_from_path(file_name, first_page=page_num + 1, last_page=page_num + 1)
                
                        ocr_text = ""
                        for image in images:
                            ocr_text += pytesseract.image_to_string(image, lang=lang)  
                        parsed_text += ocr_text  
            result.append(parsed_text)
    return result
