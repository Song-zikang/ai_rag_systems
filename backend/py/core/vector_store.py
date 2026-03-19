from langchain_community.embeddings import ZhipuAIEmbeddings
from langchain_chroma import Chroma
from config import ZHIPU_API_KEY, CHROMA_PERSIST_DIR, logger

# 初始化嵌入模型
embeddings = ZhipuAIEmbeddings(
    api_key=ZHIPU_API_KEY,
    model="embedding-2"
)

# 初始化Chroma向量库（新版本自动持久化，无需手动persist）
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory=CHROMA_PERSIST_DIR
)

def add_chunks_to_vector_store(chunks: list, filename: str):
    """将文本块添加到向量库，添加异常处理"""
    try:
        if not chunks:
            logger.warning(f"文件{filename}切分后无文本块，跳过入库")
            return
        # 添加文本块+元数据
        vector_store.add_texts(
            chunks,
            metadatas=[{"source": filename} for _ in chunks]
        )
        logger.info(f"文件{filename}共{len(chunks)}个文本块已成功入库")
    except Exception as e:
        logger.error(f"文件{filename}入库失败：{str(e)}", exc_info=True)
        raise RuntimeError(f"向量库入库失败：{str(e)}")