from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam,
)
from constructs import Construct

from lambdas import Lambdas


class CoolImageBackEnd(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stk = Stack.of(self)
        account_id = stk.account

        REGION_NAME = self.region
        REGION_ENDPOINT = you_endpoint_region

        endpoint_text_to_image = your_text_to_image_endpoint
        bucket_name = your_bucket_name
        distribution_name = distribution_name

        Fn  = Lambdas(self,'Fn')

        Fn.cool_image_hook.add_environment(key='ENV_ENDPOINT_TEXT_TO_IMAGE', value= endpoint_text_to_image)
        Fn.cool_image_hook.add_environment(key='ENV_BUCKET_NAME', value= bucket_name)
        Fn.cool_image_hook.add_environment(key='ENV_DISTRIBUTION_NAME', value= distribution_name)
        Fn.cool_image_hook.add_environment(key='REGION_ENDPOINT', value= you_endpoint_region)


        Fn.cool_image_hook.add_to_role_policy(
            aws_iam.PolicyStatement(
                        actions=["translate:TranslateText","comprehend:DetectDominantLanguage"], 
                        resources=['*'])
                    )
        
        Fn.cool_image_hook.add_to_role_policy(aws_iam.PolicyStatement(
            actions=["sagemaker:InvokeEndpoint"],resources=[f"arn:aws:sagemaker:{REGION_ENDPOINT}:{account_id}:endpoint/{endpoint_text_to_image}"])
        )

        Fn.cool_image_hook.add_to_role_policy(aws_iam.PolicyStatement(
            actions=[
				"s3:PutObject",
				"s3:GetObject"
			],resources=[f"arn:aws:s3:::{bucket_name}/*",f"arn:aws:s3:::{bucket_name}"
			]))