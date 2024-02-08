import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/mage-de-zoomcamp-b7f659539a2a.json"


bucket_name = 'mage-zoomcamp-rekt'
project_id = 'mage-de-zoomcamp'

table_name = "green_taxi"

# PYARROW will handle the partitioning
root_path = f"{bucket_name}/{table_name}"


@data_exporter
def export_data(data, *args, **kwargs):
    table = pa.Table.from_pandas(data)
    # This lets PYARROW know what our filesystem is and
    # will use the creds from env automatically
    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["lpep_pickup_date"],
        filesystem=gcs,
    )


