import os


class Bucket:
    def __init__(self):
        """
        Initialize consts based on env variables
        """
        self.DATA_PREFIX = os.environ.get("DATA_PREFIX")
        self.DATA_FILE_NAME = os.environ.get("DATA_FILE_NAME")
        self.BUCKET_NAME = os.environ.get("BUCKET_NAME")
        self.BUCKET_ARN = os.environ.get("BUCKET_ARN")


class File:
    CSV_FILE = "Sample_Bank_Transaction_Raw_Dataset.csv"
