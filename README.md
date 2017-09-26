# generator-axios-graphic
Yeoman generator to make developing Lambda Functions at Axios simpler and faster.

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

## Setup

`npm run setup`

This will
* Install global dependencies: `yo`, `yeoman-generator`, `gulp-cli`
* Install local dependencies
* Link `generators/app/` to `yo`
