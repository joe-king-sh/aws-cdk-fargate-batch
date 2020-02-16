#!/usr/bin/env python3
from aws_cdk import core
from aws_cdk_fargate_batch.aws_cdk_fargate_batch_stack import AwsCdkFargateBatchStack
from continuous_delivery.continuous_delivery_stack import ContinuousDeliveryStack
app = core.App()

fargate_batch_stack = AwsCdkFargateBatchStack(app, "aws-cdk-fargate-batch")
ContinuousDeliveryStack(app, id="continuous-delivery", deploy_stack=fargate_batch_stack)

app.synth()
