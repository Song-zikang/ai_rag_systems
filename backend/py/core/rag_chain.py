import time
from zhipuai import ZhipuAI
# 删掉这行：from zhipuai.exceptions import APIException, RateLimitError
from langchain.chains import RetrievalQA
from langchain_core.runnables import RunnableLambda
from config import (
    ZHIPU_API_KEY, ZHIPU_MODEL, ZHIPU_TEMPERATURE,
    RETRIEVE_TOP_K, ZHIPU_RETRY_TIMES, ZHIPU_TIMEOUT, logger
)
from py.core.vector_store import vector_store


def llm_invoke_with_retry(prompt: str, **kwargs) -> str:
    """智谱AI调用，添加重试/超时/异常处理（兼容所有zhipuai版本）
    添加**kwargs接收LangChain传递的stop等参数
    """
    # 忽略kwargs（不需要使用，但必须接收）
    client = ZhipuAI(api_key=ZHIPU_API_KEY)
    retry_times = ZHIPU_RETRY_TIMES

    for i in range(retry_times):
        try:
            response = client.chat.completions.create(
                model=ZHIPU_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=ZHIPU_TEMPERATURE,
                timeout=ZHIPU_TIMEOUT
            )
            content = response.choices[0].message.content.strip()
            logger.info(f"智谱AI调用成功（重试次数：{i}）")
            return content
        except Exception as e:
            # 兼容所有版本：通过异常信息判断是否是限流
            error_msg = str(e).lower()
            if "限流" in error_msg or "rate limit" in error_msg:
                logger.warning(f"智谱AI限流，{i + 1}秒后重试（第{i + 1}次）")
                time.sleep(i + 1)
            else:
                logger.error(f"智谱AI调用异常：{str(e)}", exc_info=True)
                if i == retry_times - 1:
                    raise RuntimeError(f"智谱AI调用失败：{str(e)}")

    raise RuntimeError(f"智谱AI调用重试{retry_times}次后仍失败")


def get_rag_chain():
    """构建RAG链，添加检索兜底（简化版，避免参数传递问题）"""
    # 初始化检索器
    retriever = vector_store.as_retriever(search_kwargs={"k": RETRIEVE_TOP_K})

    # 自定义RAG逻辑（不依赖LangChain的RetrievalQA，避免参数问题）
    def rag_chain_func(inputs):
        query = inputs.get("query", "").strip()
        if not query:
            raise ValueError("问题不能为空")

        # 1. 检索相关文档
        docs = retriever.get_relevant_documents(query)
        context = "\n\n".join([doc.page_content for doc in docs])

        # 2. 构建提示词
        if docs:
            prompt = f"""请根据以下参考文档回答问题：
{context}

问题：{query}
"""
        else:
            # 无检索结果时直接回答
            prompt = f"请回答以下问题：{query}"

        # 3. 调用LLM（直接调用自定义函数，不通过RunnableLambda）
        answer = llm_invoke_with_retry(prompt)

        # 4. 返回结果（保持和之前一致的格式）
        return {
            "result": answer,
            "source_documents": docs,
            "query": query
        }

    return rag_chain_func  # 直接返回函数，不封装为RunnableLambda