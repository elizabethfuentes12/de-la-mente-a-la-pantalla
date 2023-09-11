import aws_cdk as core
import aws_cdk.assertions as assertions

from back_end.back_end_stack import BackEndStack

# example tests. To run these tests, uncomment this file along with the example
# resource in back_end/back_end_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = BackEndStack(app, "back-end")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
