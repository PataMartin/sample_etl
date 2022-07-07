import json
from datetime import datetime

from consts import Service
from etl_exceptions import NoRecordsException, SchemaValidationException

import boto3
import pandas as pd
from aws_lambda_powertools import Logger
from cerberus import Validator

service = Service()
logger = Logger(service_name=service.SERVICE_NAME)
s3 = boto3.client("s3")


def lambda_handler(event, context):
    """
    This lambda function validates the contents of the uploaded csv file.

    Args:
        - event(Event): {"bucket": data bucket name, "key": path to csv}
          context(Context):

    Returns(Event):
        event

    """
    bucket = event["bucket"]
    file_key = event["key"]
    schema = json.loads(service.SCHEMA)

    logger.info("Validating againts {}".format(schema))
    for key in schema:
        if "format" in schema[key]:
            date_format_provided = schema[key]["format"]
            to_date = lambda s: datetime.strptime(s, date_format_provided)
            schema[key].pop("format")
            schema[key]["coerce"] = to_date

    schema_validator = Validator(schema)
    schema_validator.allow_unknown = False
    schema_validator.require_all = True
    s3_csv_path = "s3://{}/{}".format(bucket, file_key)

    df = pd.read_csv(s3_csv_path)
    df_dict = df.to_dict(orient="records")

    if not df_dict:
        logger.error("No records found")
        raise NoRecordsException

    for idx, record in enumerate(df_dict):
        if not schema_validator(record):
            logger.error(
                "Error validating record {}: {}".format(
                    idx, schema_validator.errors
                )
            )
            raise SchemaValidationException

    logger.info("Validation completed")
    df["Month"] = df["Date"].astype(str).str[0:2]
    df["Day"] = df["Date"].astype(str).str[3:5]
    df["Year"] = df["Date"].astype(str).str[6:10]
    processed_file_s3_url = "s3://{}/{}/{}".format(
        bucket, service.PROCESSING_PREFIX, file_key.split("/")[1]
    )
    df.to_csv(processed_file_s3_url, index=False)
    event["processing_file_url"] = processed_file_s3_url
    return event
