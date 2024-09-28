import os
from pathlib import Path


def get_train_dataset(folder_path: str, MAX_N: int = 100) -> list:
    labels = []  
    contents = [] 
    
    file_counter = 0
    for file_name in Path(folder_path).glob('*.txt'):
        if file_counter > MAX_N:
            break
        
        # file_path = os.path.join(folder_path, str(file_name))
        if file_name.is_file():
            with open(str(file_name), "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    labels.append(lines[0].strip())
                
                    remaining_content = "".join(lines[1:]).strip()
                    contents.append(remaining_content)

                    file_counter += 1
                    
    return [labels, contents]
