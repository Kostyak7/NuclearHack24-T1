import torch
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from ..models_cltok import create_toc_model, create_toc_tokenizer


def generate_headline(
    text: str, n_words: int = None, compression=None,
    max_length: int = 512, num_beams: int = 7, repetition_penalty: float = 10.0, 
    **kwargs
) -> str:
    if n_words:
        text = f'headline [{n_words}] | ' + text
    elif compression:
        text = '[{0:.1g}] '.format(compression) + text
    x = create_toc_tokenizer(text, return_tensors='pt', padding=True).to(create_toc_model.device)
    with torch.inference_mode():
        out = create_toc_model.generate(
            **x, 
            max_length=max_length, num_beams=num_beams, repetition_penalty=repetition_penalty, 
            **kwargs
        )
    return create_toc_tokenizer.decode(out[0], skip_special_tokens=True)


def get_blocks(sentences: list, block_size: int) -> list:
    blocks = []
    for i in range(len(sentences) - block_size + 1):
        block = ' '.join(sentences[i:i + block_size])
        blocks.append(block)
    return blocks


def cosine_similarity_blocks(blocks: list):
    vectorizer = CountVectorizer().fit_transform(blocks)
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)


def find_boundaries(similarity_matrix, threshold: float) -> list:
    boundaries = []
    for i in range(1, len(similarity_matrix)):
        if similarity_matrix[i] < threshold:
            boundaries.append(i)
    return boundaries


def text_tiling(text: str, block_size: int, threshold: float) -> list:
    sentences = sent_tokenize(text, language='russian')

    blocks = get_blocks(sentences, block_size)

    similarity_matrix = cosine_similarity_blocks(blocks).diagonal(offset=1)
    
    boundaries = find_boundaries(similarity_matrix, threshold)
    
    segments = []
    prev_boundary = 0
    for boundary in boundaries:
        segments.append(' '.join(sentences[prev_boundary:boundary + block_size]))
        prev_boundary = boundary + block_size
    segments.append(' '.join(sentences[prev_boundary:])) 
    
    return segments