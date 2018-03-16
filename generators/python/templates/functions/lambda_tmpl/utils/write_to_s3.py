#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
import csv
import io
import json
import logging

import boto3

def write_to_s3(data, filename, s3_bucket_name, output_type):
    """
    A helper function for publishing a Python dictionary to S3 as a JSON file.
    This assumes you have S3 write permissions in AWS.

    Accepts:
        * a Python dictionary or list of the data you wish to put on S3
        * the filename (and optionally its path) string to write to on S3
        * the S3 bucket's name as a string
        * the output filetype which is a string specifying CSV or JSON
    Returns: None
    """
    logger = logging.getLogger()
    s3_client = boto3.client('s3')
    if output_type is not in ('csv', 'json'):
        logger.error(e, "Error: invalid S3 output filetype")
        pass
    try:
        if output_type is 'json':
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key=filename,
                Body=json.dumps(data),
                Metadata={'Content-Type': 'application/json'}
            )ß
        elif output_type is 'csv':
            csv_buffer = io.StringIO()
            # Todo: QUOTE_ALL? QUOTE_MINIMAL? QUOTE_NONNUMERIC?
            # prevents commas in a CSV column from creating an additional column
            writer = csv.writer(csv_buffer, quoting=csv.QUOTE_NONNUMERIC)
            for row in file_list:
                writer.writerow(row)
            s3_client.put_object(
                Bucket=s3_bucket_name,
                Key=filename,
                Body=json.dumps(data),
                Metadata={'Content-Type': 'text/csv'}
            )
    except Exception as e:
        logger.error(e, "Error uploading file to S3")
