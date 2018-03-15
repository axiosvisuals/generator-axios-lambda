#!/usr/bin/env python
# _*_ coding:utf-8 _*_0
from base64 import b64decode
import json
import logging

import boto3

def decrypt_secrets(filename):
    """
    A helper function for decrypting a KMS encrypted JSON file.
    This assumes you have KMS decryption permissions in AWS.

    Accepts: a local JSON filename string to decrypt using KMS
    Returns: a dictionary of API secrets
    """
    logger = logging.getLogger()
    kms = boto3.client('kms')
    with open(filename, 'r') as encrypted_f:
        encrypted_secrets_dict = json.loads(encrypted_f.read())
    encrypted_cipher_str = encrypted_secrets_dict['CiphertextBlob']
    try:
        decrypted_secrets_str = kms.decrypt(
            CiphertextBlob=b64decode(encrypted_cipher_str))['Plaintext']
        decrypted_secrets_dict = json.loads(decrypted_secrets_str)
        return(decrypted_secrets_dict)
    except Exception as e:
        logger.error(e, "Error decrypting KMS encrypted file")
    pass

