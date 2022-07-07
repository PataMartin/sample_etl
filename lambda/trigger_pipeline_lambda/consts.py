import os


class Service:
    SERVICE_NAME = "trigger-etl-pipeline"

    def __init__(self):
        """
        Inits consts based on env variables
        """
        self.STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")
