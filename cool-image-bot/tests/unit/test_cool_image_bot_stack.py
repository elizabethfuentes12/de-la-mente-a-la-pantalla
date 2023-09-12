import aws_cdk as core
import aws_cdk.assertions as assertions

from cool_image_bot.cool_image_bot_stack import CoolImageBotStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cool_image_bot/cool_image_bot_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CoolImageBotStack(app, "cool-image-bot")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
