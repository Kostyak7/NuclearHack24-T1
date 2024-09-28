import my_models.training_config as tcf

TRAIN_MODE = True

TRAIN_DATA_DIR_PATH = 'train_data/'
TOC_TRAIN_FILE_PATH = TRAIN_DATA_DIR_PATH + 'toc.txt'


TEST_SCAN_NO_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Альфа/Устав Банка от 14.09.2023 (нот).pdf'
TEST_SCAN_WITH_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Кировский_завод/Промежуточная консолидированная отчетность  за 6 мес 2023г.pdf'
TEST_TEXT_NO_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Альфа/Приглашение_ЗО-02.pdf' 
TEST_TEXT_WITH_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Кировский_завод/2023.08.29 Отчет эмитента 6 мес 2023.pdf'

TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

MY_MODELS_DIR_PATH = 'my_models/'
SEARCH_TOC_MODEL_DIR_PATH = MY_MODELS_DIR_PATH + tcf.SEARCH_TOC_MODEL_DIR_PATH
CREATE_TOC_MODEL_DIR_PATH = MY_MODELS_DIR_PATH + tcf.CREATE_TOC_MODEL_DIR_PATH