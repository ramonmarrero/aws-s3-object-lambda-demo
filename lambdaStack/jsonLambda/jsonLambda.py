#from constructs import Construct
import aws_cdk as cdk
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import Aws

class LambdaJson(cdk.Stack):

    def __init__(
        self,
        scope: cdk.App,
        construct_id: str,
        stack_log_level: str,
        inputBucket,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #Create role
        lambda_role = _iam.Role(scope=self, id='cdk-lambda-json-role',
                                assumed_by =_iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='aws-cdk-s3-object-json-lambda-role',
                                managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaVPCAccessExecutionRole'),
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole')
                                ])

        #Create lambda function
        lambda_fn = _lambda.Function(
            self,
            "LambdaJson",
            function_name=f"lambda-json-fn",
            description="Create JSON file in Input S3 Bucket.",
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambdaStack/jsonLambda/lambdaSrc'),
            handler="createJson.handler",
            role=lambda_role,
            environment={
                'NAME': 'lambda-json-fn',
                "APP_ENV": "Development"
            }

        )

        #Grant Lambda write access to S3 Input Bucket
        inputBucket.grant_read_write(lambda_fn)

        ###########################################
        ################# OUTPUTS #################
        ###########################################

        output = cdk.CfnOutput(
            self,
            "LambdaFunction",
            value=f"https://console.aws.amazon.com/lambda/home?region={Aws.REGION}#/functions/{lambda_fn.function_name}",
            description="Lambda function to create JSON input."
        )
