#!/usr/bin/env python3
import os

import aws_cdk as cdk

from s3Stack.s3JsonBucket import s3ObjectLambdaJson
from lambdaStack.transformLambda.transformLambda import s3ObjectLambdaTransform
from lambdaStack.piiLambda.piiLambda import s3ObjectLambdaPII
from lambdaStack.jsonLambda.jsonLambda import LambdaJson

app = cdk.App()

# S3 Bucket to store JSON files
bkt_json = s3ObjectLambdaJson(app, "s3-object-bucket",
    description="S3 Bucket to store JSON files")

# Lambda Function to create Json input 
lambda_input = LambdaJson(app, "s3-object-create-json-lambda-stack",    
                            stack_log_level="INFO",
                            inputBucket=bkt_json.bucket,
                            description="Generate JSON files.")


# Process S3 requests in flight using lambda
s3_obj_transform_lambda_stack = s3ObjectLambdaTransform(
    app,
    f"s3-object-transform-lambda-stack",
    stack_log_level="INFO",
    transform_lambda_ap_name="lambda-transform-json",
    inputBucket=bkt_json.bucket, 
    description="Transform JSON file to delete columns."
)

# Process S3 requests in flight using lambda
s3_obj_PII_lambda_stack = s3ObjectLambdaPII(
    app,
    f"s3-object-PII-lambda-stack",
    stack_log_level="INFO",
    pii_lambda_ap_name="lambda-pii-hash",
    inputBucket=bkt_json.bucket, 
    description="Transform JSON file to hash Customer column."
)

app.synth()
