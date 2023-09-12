
from aws_cdk import (
    aws_apigateway as apg,
    Stack
)

from constructs import Construct



class WebhookApi(Construct):

    def __init__(self, scope: Construct, construct_id: str,lambdas, cognito=None,  **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        api = apg.RestApi(self, "getBots")
        api.root.add_cors_preflight(allow_origins=["*"], allow_methods=["GET", "OPTIONS"], allow_headers=["*"])

        bots = api.root.add_resource("bots",default_integration=apg.LambdaIntegration(lambdas.list_bots, allow_test_invoke=False))
        bots.add_cors_preflight(allow_origins=["*"], allow_methods=["GET", "OPTIONS"], allow_headers=["*"])


        if cognito:
            auth = apg.CognitoUserPoolsAuthorizer(self, "apiauthorizer",
                cognito_user_pools=[cognito]
            )
            print("API with authorizer")
            bots.add_method("GET", authorizer=auth, authorization_type=apg.AuthorizationType.COGNITO)
        else: 
            print("API without authorizer")
            bots.add_method("GET") 

        

