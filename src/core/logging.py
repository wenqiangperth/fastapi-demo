import sys
from pathlib import Path

from loguru import logger

from src.core.config import settings


def setup_logging():
    """配置 loguru 日志"""

    # 移除默认配置
    logger.remove()

    # 创建日志目录
    log_dir = Path(settings.LOG_FILE_PATH)
    log_dir.mkdir(exist_ok=True)

    log_format = (
        "[<green>{time:YYYY-MM-DD HH:mm:ss}</green>] "
        "[<level>{level: <8}</level>] "
        "[<cyan>{extra[request_id]}</cyan>] "
        "[<cyan>{name}</cyan>:<cyan>{line}</cyan>] "
        "<level>{message}</level>"
    )

    file_format = (
        "{time:YYYY-MM-DD HH:mm:ss} | "
        "{level: <8} | "
        "{extra[request_id]} | "
        "{name}:{line} | "
        "{message}"
    )

    # 控制台输出（彩色）
    logger.add(sys.stdout, colorize=True, format=log_format, level=settings.LOG_LEVEL)

    # 文件输出 - 普通日志
    logger.add(
        log_dir / "app_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # 每天午夜轮转
        retention="30 days",  # 保留30天
        compression="zip",  # 压缩旧日志
        format=file_format,
        level=settings.LOG_LEVEL,
        encoding="utf-8",
    )

    # 文件输出 - 错误日志
    logger.add(
        log_dir / "error_{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention="30 days",
        compression="zip",
        format=file_format,
        level="ERROR",
        encoding="utf-8",
    )
    # ⭐ 配置默认的 request_id（避免在非请求上下文中报错）
    logger.configure(extra={"request_id": "-"})

    return logger
