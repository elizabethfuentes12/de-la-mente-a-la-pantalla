import sys

from aws_cdk import (
    Duration,
    aws_lambda,
    aws_ssm as ssm,
    aws_iam as iam, 
    Stack

)

from constructs import Construct

from layers import (Pillow,Numpylayer)


LAMBDA_TIMEOUT= 60

BASE_LAMBDA_CONFIG = dict (
    timeout=Duration.seconds(LAMBDA_TIMEOUT),       
    memory_size=256,
    tracing= aws_lambda.Tracing.ACTIVE)

COMMON_LAMBDA_CONF = dict (runtime=aws_lambda.Runtime.PYTHON_3_8, **BASE_LAMBDA_CONFIG)


class Lambdas(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pil = Pillow(self, 'PilLay')
        numpy_layer = Numpylayer(self, 'numpy_layer')

        common = aws_lambda.LayerVersion(
            self, "common-layer", code=aws_lambda.Code.from_asset("./layers/common/"),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_9], 
            description = 'librerias adicionales', layer_version_name = "librerias-adicionales"
        )
        
        self.common = common

        self.cool_image_hook = aws_lambda.Function(
            self, "Transcribe", handler="lambda_function.lambda_handler",
            description = "Esta Lambda maneja la convesación del bot Cool Image de Amazon Lex, traduce con Amazon Translate e invoca el endopoint de Amazon SageMaker",
            code=aws_lambda.Code.from_asset("./lambdas/code/cool_image_hook"),
            layers= [common, pil.layer,numpy_layer.layer],
            **COMMON_LAMBDA_CONF)
        
        self.list_bots  = aws_lambda.Function(
            self, "listBots", handler="lambda_function.lambda_handler",
            code=aws_lambda.Code.from_asset("./lambdas/code/list_bots/"),
            **COMMON_LAMBDA_CONF)

        self.list_bots.add_to_role_policy(iam.PolicyStatement(
            actions=['lex:*'],
            resources=["*"]
            )
        )
        
        
        
        
       
