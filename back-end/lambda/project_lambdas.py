import sys

from aws_cdk import (
    Duration,
    aws_lambda,
    aws_ssm as ssm,
    Stack

)

from constructs import Construct


LAMBDA_TIMEOUT= 60

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=256,
    tracing= aws_lambda.Tracing.ACTIVE)

COMMON_LAMBDA_CONF = dict (runtime=aws_lambda.Runtime.PYTHON_3_8, **BASE_LAMBDA_CONFIG)


class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.cool_image_hook = aws_lambda.Function(
            self, "Transcribe", handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/cool_image_hook"),
            **COMMON_LAMBDA_CONF)
