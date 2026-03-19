import os
import logging
from dotenv import load_dotenv

# 加载.env环境变量文件
load_dotenv()

# ===== 基础配置 =====
# 智谱AI API Key（从环境变量读取）
ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
if not ZHIPU_API_KEY:
    raise ValueError("未配置ZHIPU_API_KEY环境变量，请先配置！")

# 文件上传配置
UPLOAD_DIR = "data/uploads"
# 允许的文件类型（扩展可自行添加）
ALLOWED_EXTENSIONS = {"txt", "docx", "pdf"}
# 最大文件大小（50MB）
MAX_FILE_SIZE = 50 * 1024 * 1024

# 向量库配置
CHROMA_PERSIST_DIR = "data/chroma_db"
# 检索相关配置
RETRIEVE_TOP_K = 3

# ===== 日志配置 =====
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/rag_system.log"),  # 日志文件
        logging.StreamHandler()  # 控制台输出
    ]
)
logger = logging.getLogger("rag_system")

# ===== 智谱AI调用配置 =====
ZHIPU_MODEL = "glm-4-flash"
ZHIPU_TEMPERATURE = 0.0
# 接口重试次数/超时时间
ZHIPU_RETRY_TIMES = 3
ZHIPU_TIMEOUT = 30