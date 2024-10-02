from .my_models import training_config as tcf

TRAIN_MODE = True

PROJECT_PATH = 'C:/Proga/projects/NuclearHack24-T1/'
ALGORITHMS_PATH = PROJECT_PATH + 'algorithms/'

TRAIN_DATA_DIR_PATH = ALGORITHMS_PATH + 'train_data/'
TOC_TRAIN_FILE_PATH = TRAIN_DATA_DIR_PATH + 'toc.txt'


TEST_SCAN_NO_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Альфа/Устав Банка от 14.09.2023 (нот).pdf'
TEST_SCAN_WITH_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Кировский_завод/Промежуточная консолидированная отчетность  за 6 мес 2023г.pdf'
TEST_TEXT_NO_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Альфа/Приглашение_ЗО-02.pdf' 
TEST_TEXT_WITH_TOC_FILE_PATH = TRAIN_DATA_DIR_PATH + 'Кировский_завод/2023.08.29 Отчет эмитента 6 мес 2023.pdf'

TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

MY_MODELS_DIR_PATH = ALGORITHMS_PATH + 'my_models/'
CREATE_TOC_MODEL_DIR_PATH = MY_MODELS_DIR_PATH + tcf.CREATE_TOC_MODEL_DIR_PATH
SEARCH_TOC_MODEL_DIR_PATH = MY_MODELS_DIR_PATH + tcf.SEARCH_TOC_MODEL_DIR_PATH
SEARCH_TITLE_MODEL_DIR_PATH = MY_MODELS_DIR_PATH + tcf.SEARCH_TITLE_MODEL_DIR_PATH


KEY_STRUCTURE_WORDS_ALONE = set(['введение', 'вывод', 'заключение'])
KEY_STRUCTURE_WORDS = set(['глава', 'часть', 'раздел', 'введение', 'подраздел', 'пункт'])
TOC_SEARCH_KEYWORDS = ["содержание", "таблица содержимого", "список", "оглавление", "содержимое"]

OUTPUT_FILENAME_ADDITIVE = '_output'
LINKED_PAGES_FILENAME_ADDITIVE = '_linked_pages'

ARIAL_FONT_PATH = r"arial.ttf"
ARIAL_BOLD_FONT_PATH = r"arial_bold.ttf"
ARIAL_LIGHT_FONT_PATH = r"arial_light.ttf"
ARIAL_NARROW_FONT_PATH = r"arial_narrow.ttf"

DEFAULT_TEXT_SIZE = 10
DEFAULT_HEADLINE_SIZE = 24
DEFAULT_LINE_SPACING = 5