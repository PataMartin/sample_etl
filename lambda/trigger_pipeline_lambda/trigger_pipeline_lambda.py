import json

from consts import Service

import boto3
from aws_lambda_powertools import Logger

step_function = boto3.client("stepfunctions")
service = Service()
logger = Logger(service_name=service.SERVICE_NAME)


def lambda_handler(event, context):
    """
    This lambda starts the etl pipeline execution.
    This lambda will be automatically triggered every time a new object is
    created on the data bucket.

    Args:
        - event(Event):
        - context(Context):

    Returns(dict):
        event

    """
    logger.info("Event: {}".format(event))
    for record in event["Records"]:
        logger.info("New object created: {}".format(record))
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        data = {}
        data["bucket"] = bucket
        data["key"] = key

        logger.info("Starting new execution with data: {}".format(data))
        step_function_response = step_function.start_execution(
            stateMachineArn=service.STATE_MACHINE_ARN, input=json.dumps(data)
        )
        logger.info(
            "Start execution response: {}".format(step_function_response)
        )

    return event
