import re
from typing import List

def contains_chinese(text):
    pattern = re.compile(r'[\u4e00-\u9fa5]')
    match = pattern.search(text)
    return match is not None

def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 300) -> List[str]:
    """
    将文本分割成较小的块，每个块的大小为 chunk_size, 块之间有 overlap 的重叠部分。
    
    Args:
    - text (str): 要分割的文本。
    - chunk_size (int): 每个块的大小。
    - overlap (int): 块之间的重叠部分大小。
    
    Returns:
    - List[str]: 分割后的文本块列表。
    """
    text = text.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ').replace('  ', '')
    words = list(text)
    chunks = []
    start = 0
    if contains_chinese(text):
        chunk_size = 400
        overlap = 100
        
    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append("".join(chunk))
        start = end - overlap  # 移动起始点，考虑重叠部分
    return chunks
