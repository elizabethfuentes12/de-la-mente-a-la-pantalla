from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam,
)
from constructs import Construct

from sagemaker import StableDiffusionDeployments #Para desplegar modelo y endpoint en Amazon SageMaker
from lambdas import Lambdas #Para desplegar la Funcion Lambda
from bots import LexBotV2, S3BotFiles #Para desplegar el bot de Amazon Lex
from s3_cloudfront import S3DeployWithDistribution
from cognito_stack import UserPool
from apis import WebhookApi

class CoolImageBotStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stk = Stack.of(self)
        account_id = stk.account
        REGION_NAME = self.region
        Fn  = Lambdas(self,'Fn')

        idp = UserPool(self, "Users")

        Api = WebhookApi(self, "API", lambdas=Fn, cognito=idp.user_pool)

        website = S3DeployWithDistribution(self, "www", "front_end/build", "")

        bucket_name = website.bucket.bucket_name

        sd = StableDiffusionDeployments(self, "SD")


        REGION_ENDPOINT = self.region
        endpoint_text_to_image = sd.endpoint_sd_name
        distribution_name = website.distribution.domain_name
        
        #+++++++++++++++++++++++++++++++++++++++++++++
        #++++ Desplegar Funcion Lambda y permisos ++++
        #+++++++++++++++++++++++++++++++++++++++++++++

        
        lambda_hook = Fn.cool_image_hook

        lambda_hook.add_environment(key='ENV_ENDPOINT_TEXT_TO_IMAGE', value= endpoint_text_to_image)
        lambda_hook.add_environment(key='ENV_BUCKET_NAME', value= bucket_name)
        lambda_hook.add_environment(key='ENV_DISTRIBUTION_NAME', value= distribution_name)
        lambda_hook.add_environment(key='REGION_ENDPOINT', value= REGION_ENDPOINT)


        lambda_hook.add_to_role_policy(
            aws_iam.PolicyStatement(
                        actions=["translate:TranslateText","comprehend:DetectDominantLanguage"], 
                        resources=['*'])
                    )
        
        lambda_hook.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["sagemaker:InvokeEndpoint"],resources=[f"arn:aws:sagemaker:{REGION_ENDPOINT}:{account_id}:endpoint/{endpoint_text_to_image}"])
        )

        lambda_hook.add_to_role_policy(aws_iam.PolicyStatement(
            actions=[
				"s3:PutObject",
				"s3:GetObject"
			],resources=[f"arn:aws:s3:::{bucket_name}/*",f"arn:aws:s3:::{bucket_name}"
			]))
        
        #+++++++++++++++++++++++++++++++++++++
        #++++ Desplegar el bot y permisos ++++
        #+++++++++++++++++++++++++++++++++++++

        bot_language = ["en_US"]
        bot_zip_file =  "demo-cool-image-LexJson.zip"
        bot_name = "cool-image"

        _bot_files = S3BotFiles(self, "Files", "./bots/bot_files")
        demo_bot = LexBotV2(self, "Bot", bot_name, lambda_hook, bot_zip_file, _bot_files, bot_language)
    
