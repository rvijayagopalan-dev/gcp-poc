import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.engine import URL
import json
import logging

from pos_utils_new import PosHeaderUtil, PosDetailUtil, PosTenderUtil

# Configure logging changes added
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input_subscription', required=True)
        parser.add_argument('--db_username', required=True)
        parser.add_argument('--db_password', required=True)
        parser.add_argument('--db_name', required=True)
        parser.add_argument('--db_instance_connection_name', required=True)
        parser.add_argument('--db_table', default='json_attributes')  # Optional customization

class WriteToCloudSQL(beam.DoFn):
    def __init__(self, options):
        logger.info("Initializing WriteToCloudSQL with options: %s", options)   
        self.options = options
        
    #* Uncomment this method if you want to use URL.create for SQLAlchemy engine creation
    """def setup(self):
        db_url = URL.create(
            drivername="mysql+pymysql",
            username=self.options.db_username,
            password=self.options.db_password,
            database=self.options.db_name,
            query={"unix_socket": f"/cloudsql/{self.options.db_instance_connection_name}"}
        )
        self.engine = sqlalchemy.create_engine(db_url, pool_pre_ping=True)
        self.engine.connect()
        logger.info("Database engine created successfully. Connection name: %s", self.options.db_instance_connection_name)
    """
    def setup(self):
        logger.info("🔧 Initializing Cloud SQL connection...")
        connector = Connector()

        def getconn():
            return connector.connect(
                self.options.db_instance_connection_name,
                "pymysql",
                user=self.options.db_username,
                password=self.options.db_password,
                db=self.options.db_name,
            )

        self.engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
            pool_pre_ping=True
        )
        logger.info("✅ SQLAlchemy engine ready.")

    """def process(self, element):
        try:
            data = json.loads(element)
            logger.info("json data: %s", data)

            with self.engine.connect() as conn:
                stmt = sqlalchemy.text(
                    "INSERT INTO json_attributes (ID, DESCRIPTION, VALUE, CREATE_DATE, UPDATE_DATE) " 
                    "VALUES (:value1, :value2, :value3, NOW(), NOW())"
                )
                conn.execute(stmt, {
                    "value1": data.get("id"),
                    "value2": data.get("description"),
                    "value3": data.get("value")
                })
                conn.commit()
            logger.info("Inserted row with ID: %s", data.get("id"))
        except Exception as e:
            logger.error("Error inserting row: %s", e)
    """

    def process(self, element):
        try:
            data = json.loads(element)
            logger.info("json data: %s", data)

            header_record  = self.pos_header_extractor(data)
            detail_records = self.pos_detail_extractor(data)
            tender_records = self.pos_tender_extractor(data)

            with self.engine.connect() as conn:
                self.insertHeaderRecord(conn, header_record)
                self.insertDetailRecord(conn, detail_records)
                self.insertTenderRecord(conn, tender_records)

        except Exception as e:
            logger.error("Error inserting row: %s", e)

    def pos_header_extractor(pos_record):
        return {
            'warehouseNumber' : PosHeaderUtil.h_H1WHSE(pos_record),
            'registerNumber'  : PosHeaderUtil.h_H1REG(pos_record),
            'grossPlus'       : PosHeaderUtil.h_H1PLUS(pos_record),
            'grossMinus'      : PosHeaderUtil.h_H1MNUS(pos_record),
            'amountTaxA'      : PosHeaderUtil.h_H1XAAM(pos_record),
            'amountTaxB'      : PosHeaderUtil.h_H1XBAM(pos_record),
            'amountTaxC'      : PosHeaderUtil.h_H1XCAM(pos_record),
            'amountTaxD'      : PosHeaderUtil.h_H1XDAM(pos_record),
            'transactionTotal': PosHeaderUtil.h_H1TSAL(pos_record),
            'resaleTotal'     : PosHeaderUtil.h_H1TRSL(pos_record)
        }

    def pos_detail_extractor(pos_record):
        pos_items = pos_record.get('items', [])
        extracted_details = []
        
        for pos_item in pos_items:
            detailObj = {
                'warehouseNumber'  : PosDetailUtil.d_D1WHSE(pos_record),
                'registerNumber'   : PosDetailUtil.d_D1REG(pos_record),
                'extendedSellPrice': PosDetailUtil.d_D1SELL(pos_item),
                'departmentNumber' : PosDetailUtil.d_D1DEPT(pos_item),
                'unitSellPrice'    : PosDetailUtil.d_D1USEL(pos_item)
            }
            extracted_details.append(detailObj)
        
        return extracted_details

    def pos_tender_extractor(pos_record):
        pos_tenders = pos_record.get('tenders', [])
        extracted_tenders = []

        for pos_tender in pos_tenders:
            tenderObj = {
                'warehouseNumber': PosTenderUtil.t_T1WHSE(pos_record),
                'registerNumber' : PosTenderUtil.t_T1REG(pos_record),
                'tenderAmount'   : PosTenderUtil.t_T1AMT(pos_tender)
            }
            extracted_tenders.append(tenderObj)

        return extracted_tenders
    
    def insertHeaderRecord(self, conn, header_record):
        stmt = sqlalchemy.text(
            "INSERT INTO INTLH1P (H1WHSE, H1REG, H1PLUS, H1MNUS, H1XAAM, H1XBAM, H1XCAM, H1XDAM, H1TSAL, H1TRSL) " 
            "VALUES (:value1, :value2, :value3, :value4, :value5, :value6, :value7, :value8, :value9, :value10)"
        )
        conn.execute(stmt, {
            "value1": header_record.get("warehouseNumber"),
            "value2": header_record.get("registerNumber"),
            "value3": header_record.get("grossPlus"),
            "value4": header_record.get("grossMinus"),
            "value5": header_record.get("amountTaxA"),
            "value6": header_record.get("amountTaxB"),
            "value7": header_record.get("amountTaxC"),
            "value8": header_record.get("amountTaxD"),
            "value9": header_record.get("transactionTotal"),
            "value10": header_record.get("resaleTotal")
        })
        conn.commit()
        logger.info("Inserted Header Row with ID: %s-%s", header_record.get("locationId"), header_record.get("registerId"))

    def insertDetailRecord(self, conn, detail_records):
        stmt = sqlalchemy.text(
            "INSERT INTO INTLD1P (D1WHSE, D1REG, D1SELL, D1DEPT, D1USEL) " 
            "VALUES (:value1, :value2, :value3, :value4, :value5)"
        )

        params = []
        for detail in detail_records:  # <- make sure this is a list
            params.append({
            "value1": detail.get("warehouseNumber"),
            "value2": detail.get("registerNumber"),
            "value3": detail.get("extendedSell"),
            "value4": detail.get("department"),
            "value5": detail.get("unitSell")
            })

        with conn.begin():
            result = conn.execute(stmt, params)
            logger.info("Inserted %s Detail rows.", result.rowcount or 0)
        conn.commit()

    def insertTenderRecord(self, conn, tender_records):        
        stmt = sqlalchemy.text(
            "INSERT INTO INTLT1P (T1WHSE, T1REG, T1AMT) "
            "VALUES (:value1, :value2, :value3)"
        )

        params = []
        for tender in tender_records:  # <- make sure this is a list
            params.append({
                "value1": tender.get("locationId"),
                "value2": tender.get("registerId"),
                "value3": tender.get("tenderAmount"),
            })

        with conn.begin():
            result = conn.execute(stmt, params)
            logger.info("Inserted %s Tender rows.", result.rowcount or 0)

def run(argv=None):
    pipeline_options = PipelineOptions(argv)
    custom_options = pipeline_options.view_as(CustomOptions)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    pipeline_options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription=custom_options.input_subscription).with_output_types(bytes)
            | "Decode bytes to string" >> beam.Map(lambda x: x.decode('utf-8'))
            | "Write to Cloud SQL" >> beam.ParDo(WriteToCloudSQL(custom_options))
        )

if __name__ == '__main__':
    run()