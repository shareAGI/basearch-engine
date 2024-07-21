from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
from app.core.config import settings
from logging import getLogger

logger = getLogger(__name__)

class MilvusClient:
    def __init__(self, collection_name: str):
        # 连接到 Milvus 实例
        connections.connect(host=settings.MILVUS_HOST, port=settings.MILVUS_PORT)

        ######### 生产环境需要删除 #########
        # 创建 Collection 对象
        if settings.EMBEDDING_CLEAR_WHEN_START:
            try:
                collection = Collection(name=collection_name)

                # 删除集合
                collection.drop()
            except Exception as e:            
                pass
        #################################

        self.collection_name = collection_name
        self._create_collection()
        self._create_index()

    def _create_collection(self):
        # 定义字段
        fields = [
            FieldSchema(name="emb_id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="id", dtype=DataType.INT64),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=settings.EMBEDDING_DIM),
        ]

        # 创建集合模式
        schema = CollectionSchema(fields, f"{self.collection_name} collection")

        # 创建集合
        self.collection = Collection(self.collection_name, schema)

    def _create_index(self):
        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128},
            "metric_type": "COSINE"
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)

    def insert(self, vectors: list):
        # 插入单条向量
        if isinstance(vectors[0], int):
            rows = [{"id": vectors[0], "embedding": vectors[1]}]
        
        # 插入多条向量
        else:
            rows = []
            for index, vector in vectors:
                if not len(vector) > 0:
                    logger.error(f"向量长度为 0，id: {index}")
                    continue
                
                if len(vector) != settings.EMBEDDING_DIM:
                    logger.error(f"向量长度不匹配，id: {index}, len: {len(vector)}")
                    continue
                
                rows.append({
                    "id": index,
                    "embedding": vector,
                })
        
        if len(rows) == 0:
            return
        
        self.collection.insert(rows)

    def search(self, vector: list, top_k: int = 10, threshold: float = 20):
        self.collection.load()

        # search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

        # breakpoint()
        results = self.collection.search([vector], "embedding", search_params, limit=top_k)
        # results = sorted(results[0], key=lambda x: x.distance)
        logger.info(f"sim results: {results}")
        
        # 提取搜索结果中的 ID
        ids = [hit.id for hit in results[0] if hit.distance < threshold]

        # 使用 ID 查询详细记录
        records = self.collection.query(expr=f"emb_id in {ids}", output_fields=["emb_id", "id", "embedding"])
        # logger.info(f"sim records: {records}")
        
        return records