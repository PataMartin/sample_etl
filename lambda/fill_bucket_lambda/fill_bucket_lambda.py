from consts import Bucket, File

import boto3
import cfnresponse

from aws_lambda_powertools import Logger

bucket = Bucket()
s3 = boto3.client("s3")
logger = Logger(service="FILL_BUCKET_SERVICE")


def lambda_handler(event, context):
    """
    This lambda function copy data to the data bucket on bucket creation.
    This lambda is invoked on deployment by a cfn custom resource

    Args:
        - event(Event):
        - context(context):

    Returns(dict):
        S3 Client response
    """
    logger.info("Event: {}\nContext: {}".format(event, context))

    logger.info("Reading CSV file")
    csv_file = open(File.CSV_FILE, "r")
    csv_file_content = csv_file.read()
    csv_file.close()

    logger.info("Uploading data file to bucket {}".format(bucket.BUCKET_NAME))
    key = "{}/{}".format(bucket.DATA_PREFIX, bucket.DATA_FILE_NAME)
    try:
        s3_response = s3.put_object(
            Bucket=bucket.BUCKET_NAME, Key=key, Body=csv_file_content
        )

        logger.info("S3 client response: {}".format(s3_response))

        logger.info("Sending response to CFN")
        response = {}
        response["Data"] = 120
        cfnresponse.send(
            event,
            context,
            cfnresponse.SUCCESS,
            response,
        )
    except Exception as e:
        logger.error("Sending ERROR response to CFN: {}".format(e))
        response = {}
        response["Data"] = 120
        cfnresponse.send(
            event,
            context,
            cfnresponse.ERROR,
            response,
        )

    return s3_response
