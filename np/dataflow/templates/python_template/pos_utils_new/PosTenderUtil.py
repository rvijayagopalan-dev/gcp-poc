import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def t_T1WHSE(pos_data):
    location = pos_data.get('location', {})
    warehouse = location.get('locationId', '')
    logger.info("Tender Warehouse # %s", warehouse)
    return warehouse


def t_T1REG(pos_data):
    transaction_details = pos_data.get('transactionDetails', {})
    terminal = transaction_details.get('terminal', {})
    register = terminal.get('terminalId', '')
    logger.info("Tender Register # %s", register)
    return register


def t_T1AMT(pos_data):
    tender_amount_obj = pos_data.get('tenderAmount', {})
    tender_amount = float(tender_amount_obj.get('amount', 0.0))
    logger.info("Tender Amount %s", tender_amount)
    return tender_amount