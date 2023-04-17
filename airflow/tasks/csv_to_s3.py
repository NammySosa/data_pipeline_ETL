import boto3
import botocore
import configparser
import pathlib
import sys


parser = configparser.ConfigParser()
path = pathlib.Path(__file__).parent.resolve()
parser.read(f"{path}/configuration.conf")
bucket_name = parser.get("aws_config", "bucket_name")
aws_region = parser.get("aws_config", "aws_region")
output_name = sys.argv[1]


# Name for our S3 file
file_name = f"{output_name}.csv"
key = file_name


def main():
    conn = connect_to_s3()
    create_bucket_if_not_exists(conn)
    upload_file_to_s3(conn)


def connect_to_s3():
    conn = boto3.resource("s3")
    return conn

def create_bucket_if_not_exists(conn):
    exists = True
    try:
        conn.meta.client.head_bucket(Bucket=bucket_name)
    except botocore.exceptions.ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "404":
            exists = False
    if not exists:
        conn.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": aws_region},
        )


def upload_file_to_s3(conn):
    conn.meta.client.upload_file(
        Filename="/tmp/" + file_name, Bucket=bucket_name, Key=key
    )

if __name__ == "__main__":
    main()
