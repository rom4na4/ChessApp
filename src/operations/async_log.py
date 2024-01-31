from loguru import logger

logger.add("../backups/debug.log", format="{time} {level} {message}", level="DEBUG", rotation="1 MB", compression="zip")


async def logging_job(host, port, status_code, method, text):
    try:
        if status_code == 200:
            logger.info(f"{host}:{port}, status_code:{status_code}, {method}. \n body: {text}")
            return "log is created"
        else:
            logger.warning(f"{host}:{port}, status_code:{status_code}, {method}. \n body: {text}")
            return "log is created"
    except Exception as e:
        logger.error(f"{host}:{port}, status_code:{status_code}, {method}. \n body: {text} \n ERROR: {e}")
        print("Logger: ", e)
        return "log is created"
