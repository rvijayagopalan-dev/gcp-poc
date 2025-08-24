import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def t_T1WHSE(tenderData):
    logger.info("Tender Warehouse # %s", tenderData)
    return tenderData

def t_T1REG(tenderData):
    logger.info("Tender Register # %s", tenderData)
    return tenderData