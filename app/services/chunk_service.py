import concurrent.futures
from app.core.database import get_db
from app.models.article import Article
from app.models.record import ChunkRecord
from app.models.chunk import Chunk
from app.utils.chunk import chunk_text
from app.utils.milvus_client import MilvusClient
from app.utils.vectorizer import get_embedding_vector
from typing import List
from app.core.config import settings

milvus_client_chunks = MilvusClient("chunks")

def process_new_article_chunks():
    db = next(get_db())
    
    # Process articles without chunks
    articles_without_chunks = db.query(Article).filter(~Article.chunks.any()).all()
    for article in articles_without_chunks:
        chunks = chunk_text(article.content)
        for chunk in chunks:
            db.add(Chunk(article_id=article.id, content=chunk, url=article.url))
    db.commit()

    # Process chunks without vectors
    chunks_without_vectors = db.query(Chunk).filter(Chunk.has_vector == False).all()
    chunk_texts = [chunk.content for chunk in chunks_without_vectors]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings.EMBEDDING_API_WORKER) as executor:
        futures = {executor.submit(get_embedding_vector, chunk_text): chunk.id for chunk_text, chunk in zip(chunk_texts, chunks_without_vectors)}
        for future in concurrent.futures.as_completed(futures):
            chunk_id = futures[future]
            vector = future.result()
            # breakpoint()
            chunk = db.query(Chunk).filter(Chunk.id == chunk_id).first()
            if chunk and len(vector) > 0:
                milvus_client_chunks.insert([chunk.id, vector])
                chunk.has_vector = True
                db.add(chunk)
    db.commit()

async def search_sim_chunks(query: str) -> List[ChunkRecord]:
    query_vector = get_embedding_vector(query)

    results = milvus_client_chunks.search(query_vector)
    chunk_ids = [result["id"] for result in results]
    
    db = next(get_db())
    chunks = db.query(Chunk).filter(Chunk.id.in_(chunk_ids)).all()
    return [ChunkRecord(**chunk.__dict__) for chunk in chunks]