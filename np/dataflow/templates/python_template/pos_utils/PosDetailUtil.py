import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def d_D1WHSE(detailData):
    logger.info("Detail Warehouse # %s", detailData)
    return detailData

def d_D1REG(detailData):
    logger.info("Detail Register # %s", detailData)
    return detailData