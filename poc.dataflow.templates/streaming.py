import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import json
		
class ExtractAttributesFn(beam.DoFn):
    def process(self, element):
        message = json.loads(element.decode('utf-8'))
        # Extract specific attributes
        extracted = {
            'id': message.get('id'),
            'timestamp': message.get('timestamp'),
            'value': message.get('value')
        }
        yield json.dumps(extracted)

def run():
    options = PipelineOptions()
    options.view_as(StandardOptions).streaming = True

    with beam.Pipeline(options=options) as p:
        (
            p
            | 'Read from PubSub' >> beam.io.ReadFromPubSub(subscription='projects/sales-poc-465319/subscriptions/YOUR_SUB')
            | 'Extract Attributes' >> beam.ParDo(ExtractAttributesFn())
            | 'Write to GCS' >> beam.io.WriteToText('gs://ext-df-json-bucket/output', file_name_suffix='.json')
        )

if __name__ == '__main__':
    run()