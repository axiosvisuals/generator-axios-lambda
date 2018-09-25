#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
import json
import logging

import boto3
import botocore


def get_secret(secret_name, region_name):
    """
    A helper function for getting secrets from AWS Secrets Manager.
    This assumes you have secrets manager permissions in AWS.

    Accepts: the name of the secret, the region the secrets is held in
    Returns: a dictionary of API secrets, binary data, or None if an error occurs
    """
    logger = logging.getLogger()
    session = boto3.session.Session()
    client = session.client(
        service_name="secretsmanager",
        region_name=region_name,
        endpoint_url="https://secretsmanager." + region_name + ".amazonaws.com",
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            logger.error("The requested secret " + secret_name + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            logger.error("The request was invalid due to: " + str(e))
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            logger.error("The request had invalid params: " + str(e))
        return None
    else:
        # Decrypted secret using the associated KMS CMK
        # Depending on whether the secret was a string or binary,
        # one of these fields will be populated
        if "SecretString" in get_secret_value_response:
            secret = get_secret_value_response["SecretString"]
            secret_dict = json.loads(secret)
            return secret_dict
        else:
            binary_secret_data = get_secret_value_response["SecretBinary"]
            return binary_secret_data
