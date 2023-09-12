from aws_cdk import (
    aws_iam as iam, Stack,
    aws_cognito as cognito,RemovalPolicy,
    CfnOutput
)

from constructs import Construct



class UserPool(Construct):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)


        stk = Stack.of(self)
        region = stk.region
        stack_name = stk.stack_name

        sufijo  = stack_name.split('-')[-1]
        prefijo = 'dominio'

        self.user_pool = cognito.UserPool(
            self, "user_pool",
            password_policy = cognito.PasswordPolicy(min_length=8),
            self_sign_up_enabled = True, 
            standard_attributes = cognito.StandardAttributes(
                email=cognito.StandardAttribute(required=True),
                fullname=cognito.StandardAttribute(required=True)),
            sign_in_aliases= cognito.SignInAliases(email=True),
            removal_policy= RemovalPolicy.DESTROY,
            account_recovery= cognito.AccountRecovery.EMAIL_ONLY,
            auto_verify = cognito.AutoVerifiedAttrs(email=True)
        )


        self.user_pool_client = cognito.UserPoolClient(self, "Client",
            user_pool=self.user_pool,

        )

        '''
        self.user_pool_domain = cognito.UserPoolDomain(
            self, "cognitoDomain",
            cognito_domain = cognito.CognitoDomainOptions(
                domain_prefix = "{}-{}".format(prefijo, sufijo)),
            user_pool=self.user_pool
        )
        '''




        self.id_pool = cognito.CfnIdentityPool(
            self,'idpool', 
            allow_unauthenticated_identities = True, 
            allow_classic_flow=None, 
            cognito_identity_providers=[
                cognito.CfnIdentityPool.CognitoIdentityProviderProperty(
                    client_id=self.user_pool_client.user_pool_client_id, provider_name=self.user_pool.user_pool_provider_name
                    )
            ]
        )

        self.auth_role = iam.Role(
            self, "authRole", 
            assumed_by = iam.FederatedPrincipal(
                federated = 'cognito-identity.amazonaws.com',
                conditions = {
                    "StringEquals": { "cognito-identity.amazonaws.com:aud": self.id_pool.ref },
                    "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "authenticated" }
                },
                assume_role_action= "sts:AssumeRoleWithWebIdentity"
            )
        )

        self.unauth_role = iam.Role(
            self, "unAuthRole", 
            assumed_by = iam.FederatedPrincipal(
                federated = 'cognito-identity.amazonaws.com',
                conditions = {
                    "StringEquals": { "cognito-identity.amazonaws.com:aud": self.id_pool.ref },
                    "ForAnyValue:StringLike": { "cognito-identity.amazonaws.com:amr": "unauthenticated" }
                },
                assume_role_action= "sts:AssumeRoleWithWebIdentity"
            )
        )

        for role in [ self.auth_role,  self.unauth_role]:
            role.add_to_policy(iam.PolicyStatement(
                actions=["lex:PostContent","lex:PostText","lex:PutSession","lex:GetSession","lex:DeleteSession","lex:RecognizeText",
                    "lex:RecognizeUtterance", "lex:List*",
                    "lex:StartConversation"],
                resources=["*"]
                ))
        

        cognito.CfnIdentityPoolRoleAttachment(self, 'authRoleAttachment', identity_pool_id = self.id_pool.ref, 
            roles = {'authenticated': self.auth_role.role_arn, 'unauthenticated': self.unauth_role.role_arn})


        CfnOutput(self, 'identity_pool_id', description= "identity_pool_id", value=self.id_pool.ref)

        CfnOutput(self, 'user_pool_id', description= "user_pool_id",value=self.user_pool.user_pool_id)
        
        CfnOutput(self, 'user_pool_client', description= "user_pool_client",value=self.user_pool_client.user_pool_client_id)

        CfnOutput(self, 'cognito-region', description= "cognito region",value=region)