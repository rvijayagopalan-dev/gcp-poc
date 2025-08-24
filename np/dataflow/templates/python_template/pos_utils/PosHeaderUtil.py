import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def h_H1WHSE(headerData):
    logger.info("Warehouse # %s", headerData)
    return headerData

def h_H1REG(headerData):
    logger.info("Register # %s", headerData)
    return headerData

def h_H1PLUS(headerData):
    logger.info("Gross Plus %s", headerData)
    return 

def h_H1MNUS(headerData):
    logger.info("Gross Minus %s", headerData)
    return 

def h_H1XAAM(headerData):
    logger.info("Tax A Amount %s", headerData)
    return 

def h_H1XBAM(headerData):
    logger.info("Tax B Amount %s", headerData)
    return
 
def h_H1XCAM(headerData):
    logger.info("Tax C Amount %s", headerData)
    return

def h_H1XDAM(headerData):
    logger.info("Tax D Amount %s", headerData)
    return

def h_H1TSAL(headerData):
    logger.info("Transaction Total %s", headerData)
    return

def H1TRSL(headerData):
    logger.info("Resale Total %s", headerData)
    return