# generator-axios-lambda
Yeoman generator to make developing Lambda Functions at Axios simpler and faster.

## What's in here?
Files necessary for creating a Lambda function managed by Apex, a command line tool for building, managing, and deploying functions.

* `generators`
  * `app` a Yeoman app for generating a Lambda functions' subdirectories
  * `node` templates for a Node Lambda function
  * `python` template for a Python Lambda function

## Setup

Within the generator-axios-lambda dir
`npm run setup`

This will
* Install global dependencies: `yo`, `yeoman-generator`, `gulp-cli`
* Install local dependencies
* Link `generators/app/` to `yo`

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

## Developing

### Utils

#### Decrypting secrets

```python
def get_secret(secret_name, region_name):
    """
    A helper function for getting secrets from AWS Secrets Manager.

    Required: Function role permissions for Secrets Manager.
    Accepts: the name of the secret, the region the secrets is held in
    Returns: a dictionary of API secrets, binary data, or None if an error occurs
    """
```

#### Publishing a message via SNS
You can use SNS to create email alerts. Just [create](https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html) an SNS topic and [subscribe](https://docs.aws.amazon.com/sns/latest/dg/SubscribeTopic.html) to it.

```python
def publish_to_sns(json_message, topic_arn, summary_string="SNS summary"):
    """
    A helper function for publishing a message to SNS.
    
    Required: Function role permissions for SNS:Publish.
    Accepts:
        * a JSON containing the message to publish
        * an SNS topic ARN string
        * an optional summary string describing this message
    Returns: None
    """
```

#### Writing to S3

```python
def write_to_s3(data, filename, s3_bucket_name, output_type, s3_client=boto3.client('s3'), acl='private'):
    """
    A helper function for publishing a Python dictionary to S3 as a JSON file.

    Required: Function role permissions for S3:PutObject, S3:PutObjectAcl
    Accepts:
        * a Python dictionary or list of the data you wish to put on S3
        * the filename (and optionally its path) string to write to on S3
        * the S3 bucket's name as a string
        * the output filetype which is a string specifying CSV or JSON
    Returns: None
    """
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

## Invoking

After you've deployed, you can run the function and check the logs.

```sh
apex invoke -L [function_name]
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
