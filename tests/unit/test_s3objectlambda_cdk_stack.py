import aws_cdk as core
import aws_cdk.assertions as assertions

from s3objectlambda_cdk.s3objectlambda_cdk_stack import S3ObjectlambdaCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in s3objectlambda_cdk/s3objectlambda_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = S3ObjectlambdaCdkStack(app, "s3objectlambda-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
