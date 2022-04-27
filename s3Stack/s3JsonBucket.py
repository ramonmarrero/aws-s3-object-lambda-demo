import aws_cdk as cdk
import aws_cdk.aws_s3 as s3
from aws_cdk import aws_iam as _iam
            
class s3ObjectLambdaJson(cdk.Stack):

    def __init__(self, scope: cdk.App, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create S3 Bucket to host Json file
        self.bucket = s3.Bucket(self, "awss3objectlambda-json", bucket_name="aws-s3-object-lambda-json", 
                                removal_policy=cdk.RemovalPolicy.DESTROY, versioned=True)

        self.bucket.add_to_resource_policy(
            _iam.PolicyStatement(
                actions=["*"],
                principals=[_iam.AnyPrincipal()],
                resources=[
                    f"{self.bucket.bucket_arn}",
                    f"{self.bucket.arn_for_objects('*')}"
                ],
                conditions={
                    "StringEquals":
                    {
                        "s3:DataAccessPointAccount": f"{cdk.Aws.ACCOUNT_ID}"
                    }
                }
            )
        )


        ################# OUTPUTS #################
   
        output_1 = cdk.CfnOutput(
            self,
            "JsonEventsBucket",
            value=f"{self.bucket.bucket_name}",
            description=f"The Json input bucket name"
        )
        output_2 = cdk.CfnOutput(
            self,
            "JsonEventsBucketURL",
            value=f"https://console.aws.amazon.com/s3/buckets/{self.bucket.bucket_name}",
            description=f"The Json input bucket name"
        )