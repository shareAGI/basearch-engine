from fastapi import APIRouter, Query
from typing import List
from app.models.record import ArticleRecord, ChunkRecord
from app.services.mark_service import search_sim_marks, process_new_marks
from app.services.chunk_service import search_sim_chunks, process_new_article_chunks

from threading import Thread

router = APIRouter()

# 搜索query相关收藏书签，返回相似度最高的n个结果
@router.get("/search_sim_articles", response_model=List[ArticleRecord])
async def search_marks_endpoint(query: str = Query(..., description="Search query")):
    results = await search_sim_marks(query)
    return results

# 搜索query相关文字段，返回相似度最高的n个结果
@router.get("/search_sim_chunks", response_model=List[ChunkRecord])
async def search_marks_endpoint(query: str = Query(..., description="Search query")):
    results = await search_sim_chunks(query)
    return results

# 上层调用该接口进行通知，当数据库有新入库的文章（url, title, content），对新入库的文章开始处理流程
# 具体流程：
# 1. 总结文章内容，生成summary(~500字)、summary_short(~30字)
# 2. 生成summary的embedding，存入数据库
# 3. 对content切分chunk(~500字)，每个chunk生成embedding，存入数据库
@router.get("/process")
async def process_endpoint():
    def process():
        process_new_marks()
        # process_new_article_chunks()
    
    thread = Thread(target=process)
    thread.start()
    return {"message": "Processing new marks started"}
