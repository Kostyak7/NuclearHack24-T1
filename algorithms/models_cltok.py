import pytesseract
from transformers import T5ForConditionalGeneration, T5Tokenizer
from transformers import BertTokenizer, BertForSequenceClassification

from . import config as cf


# pytesseract.pytesseract.tesseract_cmd = cf.TESSERACT_CMD

create_toc_tokenizer = T5Tokenizer.from_pretrained("cointegrated/rut5-base-absum"  )
create_toc_model = T5ForConditionalGeneration.from_pretrained("cointegrated/rut5-base-absum"  )

search_title_classifier = BertForSequenceClassification.from_pretrained(cf.SEARCH_TITLE_MODEL_DIR_PATH)
search_title_tokenizer = BertTokenizer.from_pretrained(cf.SEARCH_TITLE_MODEL_DIR_PATH)

search_toc_classifier = BertForSequenceClassification.from_pretrained(cf.SEARCH_TOC_MODEL_DIR_PATH)
search_toc_tokenizer = BertTokenizer.from_pretrained(cf.SEARCH_TOC_MODEL_DIR_PATH)