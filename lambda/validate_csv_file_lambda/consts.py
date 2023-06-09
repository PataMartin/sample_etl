import os


class Service:
    SERVICE_NAME = "validate-csv-lambda"

    def __init__(self):
        """
        Init consts based on env variables
        """
        self.SCHEMA = os.environ.get("SCHEMA")
        self.PROCESSING_PREFIX = os.environ.get("PROCESSING_PREFIX")
