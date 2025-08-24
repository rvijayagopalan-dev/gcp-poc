import json
import PosHeaderUtil as PosHeaderUtil
import PosDetailUtil as PosDetailUtil
import PosTenderUtil as PosTenderUtil


poc_json_file_path = 'c:/working/gcp/gcp-poc/data/gcp/pos/poslog_00001.json'
# Open and read the JSON file
with open(poc_json_file_path, 'r') as file:
    data = json.load(file)

# Print the data
#print(data)

def pos_header_extractor(pos_record):
    return {
        'locationId': PosHeaderUtil.h_H1WHSE(pos_record['location']['locationId']),
        'registerId': PosHeaderUtil.h_H1REG(pos_record["transactionDetails"]["terminal"]["terminalId"])
    }

print(pos_header_extractor(data))


def pos_detail_extractor(pos_record): 
    return {
        'locationId': PosDetailUtil.d_D1WHSE(pos_record['location']['locationId']),
        'registerId': PosDetailUtil.d_D1REG(pos_record["transactionDetails"]["terminal"]["terminalId"])
    }
print(pos_detail_extractor(data))


def pos_tender_extractor(pos_record):
    
    
    pos_tenders = pos_record.get('tenders', [])

    # Create new array with selected attributes
    extracted_tenders = []

    for pos_tender in pos_tenders:
        tenderObj = {
            'type': pos_tender['type'],
            'tenderType': pos_tender['tenderType'],
            'amount': pos_tender['tenderAmount']['amount']
        }
    extracted_tenders.append(tenderObj)

    return {
        'locationId': PosTenderUtil.t_T1WHSE(pos_record['location']['locationId']),
        'registerId': PosTenderUtil.t_T1REG(pos_record["transactionDetails"]["terminal"]["terminalId"]), 
        'tenders':extracted_tenders
    }

    
    
print(pos_tender_extractor(data))