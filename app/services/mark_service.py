from typing import List
import concurrent.futures
from app.core.database import get_db
from app.models.article import Article
from app.models.record import ArticleRecord
from app.utils.summarizer import summarize
from app.utils.milvus_client import MilvusClient
from app.utils.vectorizer import get_embedding_vector
from app.core.config import settings

milvus_client_articles = MilvusClient("articles")

def process_articles_without_summary(articles: List[Article]):
    contents = [(f"Title: {article.title} \n\n Content: {article.content}", article.id) for article in articles]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(summarize, content): article_id for content, article_id in contents}
        for future in concurrent.futures.as_completed(futures):
            article_id = futures[future]
            success, summary = future.result()
            if success:
                yield article_id, summary

def process_articles_without_summary_short(articles: List[Article]):
    contents_short = [(article.summary, article.id) for article in articles]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(summarize, content, short=True): article_id for content, article_id in contents_short}
        for future in concurrent.futures.as_completed(futures):
            article_id = futures[future]
            success, summary_short = future.result()
            if success:
                yield article_id, summary_short

def process_articles_without_vector_summary(articles: List[Article]):
    def do_embedding(article):
        vector = get_embedding_vector(f"Title: {article.title} \n\n Content: {article.summary}")
        return (article.id, vector)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=settings.EMBEDDING_API_WORKER) as executor:
        future_to_article = {executor.submit(do_embedding, article): article for article in articles}
        vectors = [future.result() for future in concurrent.futures.as_completed(future_to_article)]
    return vectors

    
def process_new_marks():
    db = next(get_db())
    
    # Process articles without summary
    articles_without_summary = db.query(Article).filter(Article.summary == None).all()
    if articles_without_summary:
        for article_id, summary in process_articles_without_summary(articles_without_summary):
            article = db.query(Article).filter(Article.id == article_id).first()
            if article:
                article.summary = summary
                db.add(article)
        db.commit()

    # Process articles without short summary
    articles_without_summary_short = db.query(Article).filter(Article.summary != None, Article.summary_short == None).all()
    if articles_without_summary_short:
        for article_id, summary_short in process_articles_without_summary_short(articles_without_summary_short):
            article = db.query(Article).filter(Article.id == article_id).first()
            if article:
                article.summary_short = summary_short
                db.add(article)
        db.commit()

    # Process articles without vector summary
    articles_without_vector_summary = db.query(Article).filter(Article.has_vector_summary != True).all()
    # breakpoint()
    if articles_without_vector_summary:
        vectors = process_articles_without_vector_summary(articles_without_vector_summary)
        # 过滤掉空向量
        vectors = [(article_id, vector) for article_id, vector in vectors if len(vector) > 0]
        # breakpoint()
        milvus_client_articles.insert(vectors)
        for article_id, _ in vectors:
            article = db.query(Article).filter(Article.id == article_id).first()
            if article:
                article.has_vector_summary = True
                db.add(article)
        db.commit()

async def search_sim_marks(query: str) -> List[ArticleRecord]:
    query_vector = get_embedding_vector(query)
    
    results = milvus_client_articles.search(query_vector)
    article_ids = [result["id"] for result in results]
    
    db = next(get_db())
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    
    return [ArticleRecord(**article.__dict__) for article in articles]
