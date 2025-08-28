import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def h_H1WHSE(pos_data):
    location = pos_data.get('location', {})
    warehouse = location.get('locationId', '')
    logger.info("Header Warehouse # %s", warehouse)
    return warehouse


def h_H1REG(pos_data):
    transaction_details = pos_data.get('transactionDetails', {})
    terminal = transaction_details.get('terminal', {})
    register = terminal.get('terminalId', '')
    logger.info("Header Register # %s", register)
    return register


def h_H1PLUS(pos_data):
    totals = pos_data.get('totals', [])
    gross_plus = 0.0
    for total in totals:
        if total.get('totalType') == 'TransactionGrossAmount':
            gross_plus = float(total.get('totalAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Gross Plus %s", gross_plus)
    return gross_plus


def h_H1MNUS(pos_data):
    totals = pos_data.get('totals', [])
    gross_amount = 0.0
    net_amount = 0.0
    
    for total in totals:
        if total.get('totalType') == 'TransactionGrossAmount':
            gross_amount = float(total.get('totalAmount', {}).get('amount', 0.0))
        elif total.get('totalType') == 'TransactionNetAmount':
            net_amount = float(total.get('totalAmount', {}).get('amount', 0.0))
    
    gross_minus = gross_amount - net_amount
    logger.info("Header Gross Minus %s", gross_minus)
    return gross_minus


def h_H1XAAM(pos_data):
    taxes = pos_data.get('taxes', [])
    tax_a_amount = 0.0
    for tax in taxes:
        if tax.get('taxAuthority') == 'TaxA':
            tax_a_amount = float(tax.get('taxAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Tax A Amount %s", tax_a_amount)
    return tax_a_amount


def h_H1XBAM(pos_data):
    taxes = pos_data.get('taxes', [])
    tax_b_amount = 0.0
    for tax in taxes:
        if tax.get('taxAuthority') == 'TaxB':
            tax_b_amount = float(tax.get('taxAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Tax B Amount %s", tax_b_amount)
    return tax_b_amount


def h_H1XCAM(pos_data):
    taxes = pos_data.get('taxes', [])
    tax_c_amount = 0.0
    for tax in taxes:
        if tax.get('taxAuthority') == 'TaxC':
            tax_c_amount = float(tax.get('taxAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Tax C Amount %s", tax_c_amount)
    return tax_c_amount


def h_H1XDAM(pos_data):
    taxes = pos_data.get('taxes', [])
    tax_d_amount = 0.0
    for tax in taxes:
        if tax.get('taxAuthority') == 'TaxD':
            tax_d_amount = float(tax.get('taxAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Tax D Amount %s", tax_d_amount)
    return tax_d_amount

def h_H1TSAL(pos_data):
    totals = pos_data.get('totals', [])
    transaction_total = 0.0
    for total in totals:
        if total.get('totalType') == 'TransactionNetAmount':
            transaction_total = float(total.get('totalAmount', {}).get('amount', 0.0))
            break
    logger.info("Header Transaction Total %s", transaction_total)
    return transaction_total


def h_H1TRSL(pos_data):
    items = pos_data.get('items', [])
    resale_total = 0.0
    for item in items:
        if item.get('resaleItem', False):
            net_amount = item.get('prices', {}).get('netAmount', {}).get('amount', 0.0)
            resale_total += float(net_amount)
    logger.info("Header Resale Total %s", resale_total)
    return resale_total