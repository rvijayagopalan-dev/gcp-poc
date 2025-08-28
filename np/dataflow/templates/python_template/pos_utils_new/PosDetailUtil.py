import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def d_D1WHSE(pos_data):
    location = pos_data.get('location', {})
    warehouse = location.get('locationId', '')
    logger.info("Details Warehouse # %s", warehouse)
    return warehouse

def d_D1REG(pos_data):
    transaction_details = pos_data.get('transactionDetails', {})
    terminal = transaction_details.get('terminal', {})
    register = terminal.get('terminalId', '')
    logger.info("Detail Register # %s", register)
    return register

def d_D1SELL(pos_data):
    prices = pos_data.get('prices', {})
    extended_amount_obj = prices.get('extendedAmount', {})
    extended_sell = float(extended_amount_obj.get('amount', 0.0))
    logger.info("Details Extended Sell %s", extended_sell)
    return extended_sell


def d_D1DEPT(pos_data):
    item_info = pos_data.get('item', {})
    department = item_info.get('department', '')
    logger.info("Details Department %s", department)
    return department


def d_D1USEL(pos_data):
    prices = pos_data.get('prices', {})
    actual_unit_price_obj = prices.get('actualUnitPrice', {})
    unit_sell = float(actual_unit_price_obj.get('amount', 0.0))
    logger.info("Details Unit Sell %s", unit_sell)
    return unit_sell