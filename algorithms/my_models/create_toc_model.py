from transformers import T5ForConditionalGeneration, T5Tokenizer

model_name = "cointegrated/rut5-base-absum"  
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)