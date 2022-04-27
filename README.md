
# AWS S3 Object Lambda Demo

Data stored  on AWS S3 can be easily shared across different applications and services. Requirements and access may differ for each application and therefore, they might need a different view of a single data source. 
For instance, a dataset created by the the sales department may include personally identifiable information (PII) that is not needed when the same data is processed for reporting and should be redacted.
With this use case in mind, we will take a look at how to use S3 Object Lambda. It is a new feature that enable us to add code to process data retrieved from S3 before returning it to an application or service. 
S3 Object Lambda uses Lambda functions to process and transform data. The Lambda function is invoked inline with a standard S3 GET request. This enable developers to present multiple views from the same dataset, with the possibility to update the Lambda functions and modify these views at any time.
In this post, we will learn how to use S3 Object Lambda by solving a simple use case. In this scenario, we have 2 applications that ingest data from a single bucket. 
Considerations
We will create a single bucket to store the data.
The data will be in JSON format. 
- We will create 3 AWS Lambda functions. 
- The 1st Lambda function will be used to generate JSON files. 
- The 2nd Lambda function will be used to transform data for Application 1.
- The 3rd Lambda function will be used to hash columns in the data for Application 2.
- We will create all necessary resources using AWS Cloud Development Kit (AWS CDK) and Python as our programming language.To manually create a virtualenv on MacOS and Linux:

## Setup Environment
```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
