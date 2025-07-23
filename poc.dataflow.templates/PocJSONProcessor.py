import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from google.cloud.sql.connector import Connector
import sqlalchemy
import json

class CustomOptions(PipelineOptions):
    @classmethod
    def _add_argparse_args(cls, parser):
        parser.add_argument('--input_subscription', required=True)
        parser.add_argument('--db_user', required=True)
        parser.add_argument('--db_password', required=True)
        parser.add_argument('--db_name', required=True)
        parser.add_argument('--db_instance_connection_name', required=True)

class WriteToCloudSQL(beam.DoFn):
    def __init__(self, db_user, db_password, db_name, db_instance_connection_name):
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.db_instance_connection_name = db_instance_connection_name

    def setup(self):
        connector = Connector()
        self.engine = sqlalchemy.create_engine(
            connector.connect(
                self.db_instance_connection_name,
                "pymysql",
                user=self.db_user,
                password=self.db_password,
                db=self.db_name,
            ),
            pool_pre_ping=True,
        )

    

    def process(self, element):
        try:
            data = json.loads(element)
            with self.engine.connect() as conn:
                stmt = sqlalchemy.text(
                    "INSERT INTO your_table_name (ID, DESCRIPTION, VALUE, CREATE_DATE, UPDATE_DATE) " \
                    "VALUES (:value1, :value2, :value3, sysdate, sysdate)"
                )
                conn.execute(stmt, {
                    "value1": data.get("id"),
                    "value2": data.get("description"),
                    "value3": data.get("value")
                })
        except Exception as e:
            yield f"Error inserting row: {e}"

def run(argv=None):
    pipeline_options = PipelineOptions(argv)
    custom_options = pipeline_options.view_as(CustomOptions)
    pipeline_options.view_as(StandardOptions).streaming = True
    pipeline_options.view_as(SetupOptions).save_main_session = True

    with beam.Pipeline(options=pipeline_options) as p:
        (
            p
            | "Read from Pub/Sub" >> beam.io.ReadFromPubSub(subscription=custom_options.input_subscription).with_output_types(bytes)
            | "Decode" >> beam.Map(lambda x: x.decode("utf-8"))
            | "Write to Cloud SQL" >> beam.ParDo(
                WriteToCloudSQL(
                    db_user=custom_options.db_user,
                    db_password=custom_options.db_password,
                    db_name=custom_options.db_name,
                    db_instance_connection_name=custom_options.db_instance_connection_name
                )
            )
        )

if __name__ == "__main__":
    run()
