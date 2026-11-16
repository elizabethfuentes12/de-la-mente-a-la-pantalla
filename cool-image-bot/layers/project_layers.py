import json
from constructs import Construct

from aws_cdk import (
    aws_lambda

)


class Pillow(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #layer pillow
        pillow = aws_lambda.LayerVersion(
            self, "pillow", code=aws_lambda.Code.from_asset("./layers/pil.zip"),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_13], 
            description = 'Pillow 12.2.0 built for python3.13 x86_64')
        
        self.layer = pillow

class bs4_requests(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #layer con beautiful soup y requests
        bs4_requests = aws_lambda.LayerVersion(
            self, "Bs4Requests", code=aws_lambda.Code.from_asset("./layers/bs4_requests.zip"),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_13], 
            description = 'BeautifulSoup y Requests')
        
        self.layer = bs4_requests
