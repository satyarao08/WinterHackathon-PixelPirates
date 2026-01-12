import os
import pandas as pd
import pandas_gbq


def upload_dataframe(df: pd.DataFrame, table_name: str):
    """
    Upload a DataFrame to BigQuery.
    Reads project & dataset from environment variables.
    """

    project_id = os.environ["GCP_PROJECT_ID"]
    dataset_id = os.environ["BIGQUERY_DATASET"]

    full_table_id = f"{dataset_id}.{table_name}"

    pandas_gbq.to_gbq(
        df,
        full_table_id,
        project_id=project_id,
        if_exists="replace",
    )
