from aws_cdk import (
    Stack, 
    aws_iam as iam,
    aws_sagemaker as sm
)
from sagemaker import (Model, Endpoint, EndpointConfig, AsyncEndpointConfig)


from constructs import Construct
from config import (upscaler)


upsacaler_image_uri = upscaler.get("image_uri")
upscaler_model_uri = upscaler.get("model_uri")
upscaler_s3_path = upscaler.get("s3_path")
upscaler_instance_count =  upscaler.get("instance_count")
upscaler_invocation_per_instance =  upscaler.get("invocation_per_instance")
upscaler_instance_type = upscaler.get("instance_type")


class StableDiffusionDeployments(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        execution_role = iam.Role(self, "SMRole", assumed_by=iam.ServicePrincipal("sagemaker.amazonaws.com"))
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSNSFullAccess"))
        execution_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSageMakerFullAccess"))

        model_sd = Model(self, 'M_x4', execution_role.role_arn, upsacaler_image_uri, upscaler_model_uri)
        
        config_sd = EndpointConfig(self, 'C_SDXL',  model_sd.model.attr_model_name,
                                instance_type=upscaler_instance_type, instance_count=upscaler_instance_count)
        
        endpoint_sd = Endpoint(self, 'E_SDXL', config_sd.config.attr_endpoint_config_name)  


        self.endpoint_sd_name     = endpoint_sd.endpoint.attr_endpoint_name