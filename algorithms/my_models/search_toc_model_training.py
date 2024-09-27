import torch
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments

import training_config as tcf


train_texts = ["Содержание", "Другой текст"] # Сюда текста
train_labels = [1, 0]  # Сюда флаги

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
train_encodings = tokenizer(train_texts, truncation=True, padding=True)

class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CustomDataset(train_encodings, train_labels)

model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)

training_args = TrainingArguments(
    output_dir=tcf.SEARCH_TOC_MODEL_DIR_PATH,
    num_train_epochs=3,
    per_device_train_batch_size=8,
    save_steps=10_000,
    save_total_limit=2,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
)

trainer.train()

model.save_pretrained(tcf.SEARCH_TOC_MODEL_DIR_PATH)
tokenizer.save_pretrained(tcf.SEARCH_TOC_MODEL_DIR_PATH)
