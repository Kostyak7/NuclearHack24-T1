import torch
from .create_toc_model import model, tokenizer


def generate_headline(
    text, n_words=None, compression=None,
    max_length=512, num_beams=7, repetition_penalty=10.0, 
    **kwargs
):
    if n_words:
        text = '[{}] '.format(n_words) + text
    elif compression:
        text = '[{0:.1g}] '.format(compression) + text
    x = tokenizer(text, return_tensors='pt', padding=True).to(model.device)
    with torch.inference_mode():
        out = model.generate(
            **x, 
            max_length=max_length, num_beams=num_beams, repetition_penalty=repetition_penalty, 
            **kwargs
        )
    return tokenizer.decode(out[0], skip_special_tokens=True)
