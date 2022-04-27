#from constructs import Construct
import aws_cdk as cdk
import aws_cdk.aws_s3 as _s3
from aws_cdk import aws_s3objectlambda as _s3objlambda
from aws_cdk import aws_iam as _iam
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_logs as _logs
from aws_cdk import Aws


class s3ObjectLambdaPII(cdk.Stack):

    def __init__(
        self,
        scope: cdk.App,
        construct_id: str,
        stack_log_level: str,
        pii_lambda_ap_name: str,
        inputBucket,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #Create role
        lambda_role = _iam.Role(scope=self, id='cdk-lambda-pii-hash-role',
                                assumed_by =_iam.ServicePrincipal('lambda.amazonaws.com'),
                                role_name='aws-cdk-s3-object-pii-lambda-role',
                                managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaVPCAccessExecutionRole'),
                                _iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole')
                                ])
        # Allow permissions to trigger Object Lambda
        lambda_pol = _iam.PolicyStatement(
            effect=_iam.Effect.ALLOW,
            resources=["*"],
            actions=["s3-object-lambda:WriteGetObjectResponse"]
        )
       
        lambda_pol.sid = "AllowObjectLambdaS3Access"

        s3_object_lambda_fn = _lambda.DockerImageFunction(self, "lambda-pii-hash",
                                    function_name=f"s3-object-lambda-pii-hash-fn",
                                    description="Transform JSON file to hash customer column.",
                                    role=lambda_role,
                                    code=_lambda.DockerImageCode.from_image_asset("lambdaStack/piiLambda/lambdaAssets"),
                                    environment={
                                        'NAME': 's3-object-lambda-pii-hash-fn',
                                        "APP_ENV": "Development"
                                     })

        #Add policy to the Lambda function
        s3_object_lambda_fn.add_to_role_policy(lambda_pol)

        # Create lambda Access Point
        lambda_s3_access_point_prefix = "pii_hash"
        lambda_s3_access_point_policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": [
                            f"{lambda_role.role_arn}",
                        ]
                    },
                    "Action": ["s3:GetObject", "s3:PutObject"],
                    "Resource": f"arn:aws:s3:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:accesspoint/{pii_lambda_ap_name}/object/{lambda_s3_access_point_prefix}/*"
                }
            ]
        }

        self.lambda_pii_access_point = _s3.CfnAccessPoint(
            self,
            "lambda-pii-hash-access-point",
            bucket=inputBucket.bucket_name,
            name=f"{pii_lambda_ap_name}",
            policy=lambda_s3_access_point_policy_doc
        )


        s3_obj_lambda_access_point = _s3objlambda.CfnAccessPoint(
            self,
            "s3ObjectLambdaApConfig",
            name="aws-cdk-pii-hash-s3-object",
            object_lambda_configuration=_s3objlambda.CfnAccessPoint.ObjectLambdaConfigurationProperty(
                supporting_access_point=f"arn:aws:s3:{Aws.REGION}:{Aws.ACCOUNT_ID}:accesspoint/{pii_lambda_ap_name}",
                transformation_configurations=[_s3objlambda.CfnAccessPoint.TransformationConfigurationProperty(
                    actions=["GetObject"],
                    content_transformation={
                        "AwsLambda": {
                            "FunctionArn": f"{s3_object_lambda_fn.function_arn}"
                        }
                    }
                )]
            )
        )




        ###########################################
        ################# OUTPUTS #################
        ###########################################

        output = cdk.CfnOutput(
            self,
            "S3ObjectLambda",
            value=f"https://console.aws.amazon.com/lambda/home?region={Aws.REGION}#/functions/{s3_object_lambda_fn.function_name}",
            description="Transform JSON file to csv."
        )

        output_1 = cdk.CfnOutput(
            self,
            "S3ObjectLambdaArn",
            value=f"{s3_obj_lambda_access_point.attr_arn}",
            description=f"S3 Object Lambda access point bucket ARN"
        )