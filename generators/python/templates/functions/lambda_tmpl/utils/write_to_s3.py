#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
import json
import logging

import boto3

def write_to_s3(data_dict, filename, s3_bucket_name):
    """
    A helper function for publishing a Python dictionary to S3 as a JSON file.
    This assumes you have S3 write permissions in AWS.

    Accepts:
        * a Python dictionary of the data you wish to put on S3
        * the filename (and optionally its path) string to write to on S3
        * the S3 bucket's name as a string
    Returns: None
    """
    logger = logging.getLogger()
    s3_client = boto3.client('s3')
    try:
        s3_client.put_object(
            Bucket=s3_bucket_name,
            Key=filename,
            Body=json.dumps(data_dict),
            Metadata={'Content-Type': 'application/json'}
        )
    except Exception as e:
        logger.error(e, "Error uploading file to S3")
    pass
