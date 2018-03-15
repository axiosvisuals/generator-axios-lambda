# generator-axios-lambda
Yeoman generator to make developing Lambda Functions at Axios simpler and faster.

## Setup

Within the generator-axios-lambda dir
`npm run setup`

This will
* Install global dependencies: `yo`, `yeoman-generator`, `gulp-cli`
* Install local dependencies
* Link `generators/app/` to `yo`

## Developing

### Encrypting secrets

With this example, we'll use AWS KMS to store an encrypted copy of our API keys and then decrypt it on the fly with the Lambda function.  AWS MFA must be enabled to create the CMK.

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

## Deploying

### Connecting to AWS Lambda
We use a build tool `apex`. For more information, documentation, and examples visit [apex.run](http://apex.run).

If your lambda function utilizes an RDS database you'll need to follow these additional instructions to make sure the function has access to the database (for now this will need to be done in the console, ideally we can get this linked up to apex too):

1. Set up new Lambda functions in us-west-2 only, to keep them in the same region as production database.

2. When configuring the function, click on advanced settings and change the 'no VPC' setting to 'default VPC'.  This will trigger two more options for subnet and security group.

3. Set the subnet group to the one labeled 'The Lambda Zone' and the security group to the one labeled 'Lambda Security Group'   


### Multiple Environments

Multiple environments are supported with the --env flag. By default project.json and function.json are used, however when --env is specified project.ENV.json and function.ENV.json will be used, falling back on function.json for cases when staging and production config is the same. For example your directory structure may look something like the following:

```
project.stage.json
project.prod.json
functions
├── bar
│   ├── function.stage.json
│   ├── function.prod.json
│   └── index.js
└── foo
    ├── function.stage.json
    ├── function.prod.json
    └── index.js
```

If you prefer your "dev" or "staging" environment to be the implied default then leave the files as project.json and function.json:

```
project.json
project.prod.json
functions
├── bar
│   ├── function.json
│   ├── function.prod.json
│   └── index.js
└── foo
    ├── function.json
    ├── function.prod.json
    └── index.js
```

### Building a zip with dependencies for Lambda

Apex generates a zip file for you upon deploy, however sometimes it can be useful to see exactly what's included in this file for debugging purposes. The `apex build` command outputs the zip to STDOUT for this purpose.

#### Examples

Output zip to out.zip:

```sh
$ apex build foo > tmp/out.zip
$ apex deploy foo --zip tmp/foo.zip
```

OR

```sh
$ apex deploy foo -z tmp/foo.zip
```

Use environment variables

```sh
$ apex build foo > tmp/out.zip
$ apex deploy foo --env-file env.json --zip tmp/foo.zip
```

OR

```sh
$ apex deploy foo -E env.json -z tmp/foo.zip
```

## Scheduling
Scheduleding a Lambda function must be down within the AWS interface. Login to view the function apex deployed via [console.aws.amazon.com](https://console.aws.amazon.com/lambda/home?region=us-east-1#/)

### Testing
Select "Scheduled Event" from the dropdown to simulate cron trigger a lambda function

### Triggering
Under the "Triggers" table, add a "CloudWatch Events - Schedule" trigger. If you have not set up a CloudWatch Event to trigger a lambda function, you may do so by [creating a CloudWatch Event rule](https://us-east-1.console.aws.amazon.com/cloudwatch/home?region=us-east-1#rules:)

## Troubleshooting
`apex --help`

### Check the logs

`apex logs <function-name>`

Want to watch the logs live?

`apex logs <function-name> --follow`

OR

`apex logs <function-name> --f`

### Check the stats

`apex metrics`

Shows you:

* total cost ($USD)
* invocations (integer & $)
* duration (datetime & $)
* throttles (integer)
* errors (integer)
* memory (integer)

### Rollback to previous version

`apex rollback <function-name>`
