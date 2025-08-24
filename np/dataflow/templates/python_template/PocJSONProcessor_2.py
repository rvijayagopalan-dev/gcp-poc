import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.engine import URL
import json
import logging

from pos_utils import PosHeaderUtil, PosDetailUtil, PosTenderUtil

# Configure logging
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

            header_record = self.pos_header_extractor(data)
            detail_record = self.pos_detail_extractor(data)
            tender_record = self.pos_tender_extractor(data)

            with self.engine.connect() as conn:
                self.insertHeaderRecord(conn, header_record)
                self.insertDetailRecord(conn, detail_record)
                self.insertTenderRecord(conn, tender_record)

        except Exception as e:
            logger.error("Error inserting row: %s", e)

    def pos_header_extractor(self, pos_record):
        return {
        'locationId': PosHeaderUtil.h_H1WHSE(pos_record['location']['locationId']),
        'registerId': PosHeaderUtil.h_H1REG(pos_record["transactionDetails"]["terminal"]["terminalId"])
        }

    def pos_detail_extractor(self, pos_record): 
        return {
        'locationId': PosDetailUtil.d_D1WHSE(pos_record['location']['locationId']),
        'registerId': PosDetailUtil.d_D1REG(pos_record["transactionDetails"]["terminal"]["terminalId"])
        }

    def pos_tender_extractor(self, pos_record):
        return {
        'locationId': PosTenderUtil.t_T1WHSE(pos_record['location']['locationId']),
        'registerId': PosTenderUtil.t_T1REG(pos_record["transactionDetails"]["terminal"]["terminalId"])
        }
    
    def insertHeaderRecord(self, conn, header_record):
        stmt = sqlalchemy.text(
            "INSERT INTO INTLH1P (H1WHSE, H1REG) " 
            "VALUES (:value1, :value2)"
        )
        conn.execute(stmt, {
            "value1": header_record.get("locationId"),
            "value2": header_record.get("registerId")
        })
        conn.commit()
        logger.info("Inserted Header Row with ID: %s-%s", header_record.get("locationId"), header_record.get("registerId"))

    def insertDetailRecord(self, conn, detail_record):
        stmt = sqlalchemy.text(
            "INSERT INTO INTLD1P (D1WHSE, D1REG) " 
            "VALUES (:value1, :value2)"
        )
        conn.execute(stmt, {
            "value1": detail_record.get("locationId"),
            "value2": detail_record.get("registerId")
        })
        conn.commit()
        logger.info("Inserted Detail Row with ID: %s-%s", detail_record.get("locationId"), detail_record.get("registerId"))

    def insertTenderRecord(self, conn, tender_record):
        stmt = sqlalchemy.text(
            "INSERT INTO INTLT1P (T1WHSE, T1REG) " 
            "VALUES (:value1, :value2)"
        )
        conn.execute(stmt, {
            "value1": tender_record.get("locationId"),
            "value2": tender_record.get("registerId")
        })
        conn.commit()
        logger.info("Inserted Tender Row with ID: %s-%s", tender_record.get("locationId"), tender_record.get("registerId"))

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