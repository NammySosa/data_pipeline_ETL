import configparser
import pathlib
import psycopg2
import sys
from psycopg2 import sql


parser = configparser.ConfigParser()
path = pathlib.Path(__file__).resolve().parent
parser.read(f"{path}/configuration.conf")

# Store our configuration variables
username = parser.get("aws_config", "redshift_username")
pwd = parser.get("aws_config", "redshift_password")
hostname = parser.get("aws_config", "redshift_hostname")
portno = parser.get("aws_config", "redshift_port")
rs_role = parser.get("aws_config", "redshift_role")
database = parser.get("aws_config", "redshift_database")
bucket_name = parser.get("aws_config", "bucket_name")
account_id = parser.get("aws_config", "account_id")
table_name = "reddit"


output_name = sys.argv[1]


file_path = f"s3://{bucket_name}/{output_name}.csv"
role_string = f"arn:aws:iam::{account_id}:role/{rs_role}"

sql_create_table = sql.SQL(
    """CREATE TABLE IF NOT EXISTS {table} (
                            id varchar PRIMARY KEY,
                            title varchar(max),
                            score int,
                            num_comments int,
                            author varchar(max),
                            created_utc timestamp,
                            url varchar(max),
                            upvote_ratio float,
                            part varchar(max),
                            seller varchar(max)
                        );"""
).format(table=sql.Identifier(table_name))

# Create staging / temporary table to delete records that already exist in the redshift server

create_temp_table = sql.SQL(
    "CREATE TEMP TABLE our_staging_table (LIKE {table});"
).format(table=sql.Identifier(table_name))

# Copy data from this dag's CSV into temporary staging table

sql_copy_to_temp = f"COPY our_staging_table FROM '{file_path}' iam_role '{role_string}' IGNOREHEADER 1 DELIMITER ',' CSV;"

# Delete records from Redshift if they exist in this batch to give updated information

delete_from_table = sql.SQL(
    "DELETE FROM {table} USING our_staging_table WHERE {table}.id = our_staging_table.id;"
).format(table=sql.Identifier(table_name))

# Insert new records into redshift table

insert_into_table = sql.SQL(
    "INSERT INTO {table} SELECT * FROM our_staging_table;"
).format(table=sql.Identifier(table_name))

# Delete staging table
drop_temp_table = "DROP TABLE our_staging_table;"


def main():
    rs_conn = connect_to_redshift()
    load_data_into_redshift(rs_conn)


def connect_to_redshift():
    rs_conn = psycopg2.connect(
            dbname=database, user=username, password=pwd, host=hostname, port=portno
        )
    return rs_conn


def load_data_into_redshift(rs_conn):
    with rs_conn:
        cur = rs_conn.cursor()
        cur.execute(sql_create_table)
        cur.execute(create_temp_table)
        cur.execute(sql_copy_to_temp)
        cur.execute(delete_from_table)
        cur.execute(insert_into_table)
        cur.execute(drop_temp_table)
        rs_conn.commit()


if __name__ == "__main__":
    main()

