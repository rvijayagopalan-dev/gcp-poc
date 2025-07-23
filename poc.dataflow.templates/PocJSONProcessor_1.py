import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from google.cloud.sql.connector import Connector
import sqlalchemy
from sqlalchemy.engine import URL
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CustomOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input_subscription', required=True)
        parser.add_argument('--db_user', required=True)
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
            username=self.options.db_user,
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
                user=self.options.db_user,
                password=self.options.db_password,
                db=self.options.db_name,
            )

        self.engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
            pool_pre_ping=True
        )
        logger.info("✅ SQLAlchemy engine ready.")



    def process(self, element):
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
