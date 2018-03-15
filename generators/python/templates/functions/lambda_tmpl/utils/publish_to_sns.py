#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
import json
import logging

import boto3

def publish_to_sns(json_message, topic_arn, summary_string="SNS summary"):
    """
    A helper function for publishing a message to SNS.
    This assumes you have SNS publish permissions in AWS.

    Accepts:
        * a JSON containing the message to publish
        * an SNS topic ARN string
        * an optional summary string describing this message
    Returns: None
    """
    logger = logging.getLogger()
    sns = boto3.client('sns')
    try:
        sns.publish(
            TopicArn=topic_arn,
            Message=json.dumps(json_message),
            MessageStructure='string',
            MessageAttributes={
                'summary': {
                    'StringValue': summary_string,
                    'DataType': 'String'
                }
            }
        )
    except Exception as e:
        logger.error(e, "Error publishing to SNS")
    pass
