#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
import json
import logging

import boto3

def write_to_s3(data_dict, filename, s3_bucket_name):
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
