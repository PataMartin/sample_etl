import sys
from awsglue.transforms import ApplyMapping, ResolveChoice, DropNullFields
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(
    sys.argv,
    [
        "JOB_NAME",
        "GLUE_DB",
        "PROCESSING_FOLDER",
        "PROCESSED_FOLDER",
        "BUCKET_NAME",
    ],
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)
datasource0 = glueContext.create_dynamic_frame.from_catalog(
    database=args["GLUE_DB"],
    table_name=args["PROCESSING_FOLDER"],
    transformation_ctx="datasource0",
)
applymapping1 = ApplyMapping.apply(
    frame=datasource0,
    mappings=[
        ("date", "string", "date", "string"),
        ("description", "string", "description", "string"),
        ("deposits", "double", "deposits", "double"),
        ("withdrawls", "double", "withdrawls", "double"),
        ("balance", "double", "balance", "double"),
        ("year", "long", "year", "int"),
        ("month", "long", "month", "int"),
        ("day", "long", "day", "int"),
    ],
    transformation_ctx="applymapping1",
)
resolvechoice2 = ResolveChoice.apply(
    frame=applymapping1,
    choice="make_struct",
    transformation_ctx="resolvechoice2",
)
dropnullfields3 = DropNullFields.apply(
    frame=resolvechoice2, transformation_ctx="dropnullfields3"
)
datasink4 = glueContext.write_dynamic_frame.from_options(
    frame=dropnullfields3,
    connection_type="s3",
    format_options={"compression": "snappy"},
    connection_options={
        "path": "s3://{}/{}".format(
            args["BUCKET_NAME"], args["PROCESSED_FOLDER"]
        ),
        "partitionKeys": ["year", "month", "day"],
    },
    format="glueparquet",
    transformation_ctx="datasink4",
)
job.commit()
