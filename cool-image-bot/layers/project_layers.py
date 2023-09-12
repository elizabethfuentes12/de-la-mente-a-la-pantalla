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
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_7], 
            description = 'pillow')
        
        self.layer = pillow

class bs4_requests(Construct):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #layer con beautiful soup y requests
        bs4_requests = aws_lambda.LayerVersion(
            self, "Bs4Requests", code=aws_lambda.Code.from_asset("./layers/bs4_requests.zip"),
            compatible_runtimes = [aws_lambda.Runtime.PYTHON_3_8,aws_lambda.Runtime.PYTHON_3_7], 
            description = 'BeautifulSoup y Requests')
        
        self.layer = bs4_requests

class Numpylayer(Construct):
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #layer con beautiful soup y requests
        numpy_layer = aws_lambda.LayerVersion.from_layer_version_arn(self, "numpy", "arn:aws:lambda:us-west-2:420165488524:layer:AWSLambda-Python38-SciPy1x:107")
           
        
        self.layer = numpy_layer






    

