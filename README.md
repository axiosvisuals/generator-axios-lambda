# generator-axios-graphic
Yeoman generator to make developing Lambda Functions at Axios simpler and faster.

## Setup

`npm run setup`

This will
* Install global dependencies: `yo`, `yeoman-generator`, `gulp-cli`
* Install local dependencies
* Link `generators/app/` to `yo`

## Developing

### Encrypting secrets

With this example, we'll use AWS KMS to store an encrypted copy of our API keys and then decrypt it on the fly with the Lambda function.

1. [Create a customer master key (CMK) in KMS](http://docs.aws.amazon.com/kms/latest/developerguide/create-keys.html) and note the keyId that is automatically generated.

2. Encrypt the certificate in KMS using the AWS CLI tools:

```
aws kms encrypt --key-id KEY_FROM_STEP_1 --plaintext file://functions/SOME_FUNCTION/secrets.json --output json > functions/SOME_FUNCTION/encrypted_secrets.json`
```

This comand takes a file from the `file://` path, outputs JSON with the encrypted secrets, and saves it to a new file `encrypted_secrets.json`.

3.You will receive a response with a CiphertextBlob if successful.  An example of a successful response will look like:

```
{
    "KeyId": "arn:aws:kms:us-east-1:123456789000:key/<YOUR KEY ID HERE>",
    "CiphertextBlob": "<CIPHER TEXT BLOB HERE>"
}
```

See the [AWS KMS CLI help](http://docs.aws.amazon.com/cli/latest/reference/kms/index.html) for more information on input and output encoding.

### Decrypting secrets

Within the Python, `main.py`, you'll be able to decrypt the JSON and use it in your Python code

```python
import boto3
from base64 import b64decode

kms = boto3.client('kms')

with open('encrypted_secrets.json', 'r') as encrypted_f:
  encrypted_secrets_dict = json.loads(encrypted_f.read())

encrypted_cipher_str = encrypted_secrets_dict['CiphertextBlob']
decrypted_secrets_str = kms.decrypt(CiphertextBlob=b64decode(encrypted_cipher_str))['Plaintext']
decrypted_secrets_dict = json.loads(decrypted_secrets_str)
```

The code uses an AWS Python client, boto3, to establish a KMS client for decrypting your secrets. **Your Lambda function will also need permissions to use this KMS key**. Once you open up and read the encrypted file, you can read it in as a JSON string, then convert that to a Python dictionary.

## Generators

### axios-lambda:node

`yo axios-lambda:node function_name`

Generate an AWS Lambda project with a Node.js function, named `function_name`

```bash
mkdir [project-name] && cd $_
yo axios-lambda:node [function-name]
```

#### Multiple functions

To generate multiple Lambda functions within a project, just re-use the generator

```bash
yo axios-lambda:node [function-name]
```

### axios-lambda:python

`yo axios-lambda:python function_name`

Generate an AWS Lambda project with a Python function, named `function_name`

```bash
mkdir [project-name] && cd $_
yo axios-lambda:python [function-name]
```

#### Multiple functions

To generate multiple Lambda functions within a project, just re-use the generator

```bash
yo axios-lambda:python [function-name]
```
