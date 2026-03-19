import os
import asyncio
from fastapi import File, UploadFile, HTTPException, Query, APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, StreamingResponse

from config import (
    UPLOAD_DIR, MAX_FILE_SIZE,
    logger, ALLOWED_EXTENSIONS
)
from py.core.splitter import split_document, get_file_extension
from py.core.vector_store import add_chunks_to_vector_store
from py.core.rag_chain import get_rag_chain

# 创建路由实例
router = APIRouter()

# 初始化变量
os.makedirs(UPLOAD_DIR, exist_ok=True)
qa_chain = get_rag_chain()


# 工具函数：验证文件
def validate_file(file: UploadFile) -> None:
    file_content = file.file.read()
    file_size = len(file_content)
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds limit (max {MAX_FILE_SIZE / 1024 / 1024}MB)"
        )

    ext = get_file_extension(file.filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {ext}"
        )

# 工具函数：生成唯一文件名
def generate_unique_filename(filename: str) -> str:
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(UPLOAD_DIR, new_filename)):
        new_filename = f"{name}_{counter}{ext}"
        counter += 1
    return new_filename

# 根路由
@router.get("/")
async def root():
    return {"message": "System running", "status": "running"}

# 文件上传接口
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        validate_file(file)
        unique_filename = generate_unique_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, unique_filename)

        await asyncio.to_thread(
            lambda: open(file_path, "wb").write(file.file.read())
        )
        logger.info(f"File saved: {unique_filename}")

        try:
            chunks = await asyncio.to_thread(split_document, file_path)
            await asyncio.to_thread(add_chunks_to_vector_store, chunks, unique_filename)
        except Exception as e:
            os.remove(file_path)
            raise HTTPException(status_code=400, detail=f"Processing failed: {str(e)}")

        return {
            "message": "File processed successfully",
            "file_name": unique_filename,
            "chunk_count": len(chunks)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Upload failed: {str(e)}")

# 流式问答接口
@router.post("/ask")
async def ask_question(question: str = Query(..., min_length=1, max_length=1000)):
    async def stream_generator():
        try:
            result = await asyncio.to_thread(qa_chain, {"query": question})
            answer_text = result["result"]
            source_files = [doc.metadata["source"] for doc in result.get("source_documents", [])]

            for char in answer_text:
                yield char
                await asyncio.sleep(0.015)

        except Exception as e:
            yield f"[Error] {str(e)}"

    return StreamingResponse(
        stream_generator(),
        media_type="text/plain; charset=utf-8"
    )

# 清理上传文件接口
@router.delete("/clean_uploads")
async def clean_uploads():
    try:
        for filename in os.listdir(UPLOAD_DIR):
            file_path = os.path.join(UPLOAD_DIR, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return {"message": "All uploaded files cleaned"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Clean failed: {str(e)}")