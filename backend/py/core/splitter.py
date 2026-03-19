import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import logger, ALLOWED_EXTENSIONS

# 扩展：支持docx/pdf解析
try:
    from docx import Document
    from PyPDF2 import PdfReader
except ImportError:
    logger.warning("未安装docx/pdf解析依赖，仅支持txt文件！")
    Document = None
    PdfReader = None


def get_file_extension(filename: str) -> str:
    """获取文件后缀（小写）"""
    return os.path.splitext(filename)[1].lower().lstrip(".")


def read_file_content(file_path: str, ext: str) -> str:
    """根据文件类型读取内容，处理编码/格式"""
    content = ""
    try:
        if ext == "txt":
            # 尝试多种编码读取txt
            encodings = ["utf-8", "gbk", "gb2312", "utf-16"]
            for encoding in encodings:
                try:
                    with open(file_path, "r", encoding=encoding) as f:
                        content = f.read()
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("txt文件编码不支持（仅支持utf-8/gbk/gb2312/utf-16）")

        elif ext == "docx" and Document:
            doc = Document(file_path)
            content = "\n".join([para.text for para in doc.paragraphs])

        elif ext == "pdf" and PdfReader:
            reader = PdfReader(file_path)
            content = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

        else:
            raise ValueError(f"不支持的文件类型：{ext}（或未安装对应解析依赖）")

        if not content.strip():
            raise ValueError("文件内容为空")
        return content

    except Exception as e:
        logger.error(f"读取文件{file_path}失败：{str(e)}", exc_info=True)
        raise RuntimeError(f"文件读取失败：{str(e)}")


def split_document(file_path: str) -> list:
    """切分文档为文本块，添加完整异常处理"""
    try:
        # 获取文件类型
        filename = os.path.basename(file_path)
        ext = get_file_extension(filename)

        # 校验文件类型
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"不支持的文件类型：{ext}，仅支持{ALLOWED_EXTENSIONS}")

        # 读取文件内容
        text = read_file_content(file_path, ext)

        # 切分文本
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", "！", "？", "，", "、", " ", ""]
        )
        chunks = splitter.split_text(text)
        logger.info(f"文件{filename}切分完成，得到{len(chunks)}个文本块")
        return chunks

    except Exception as e:
        logger.error(f"文件{file_path}切分失败：{str(e)}", exc_info=True)
        raise RuntimeError(f"文档切分失败：{str(e)}")