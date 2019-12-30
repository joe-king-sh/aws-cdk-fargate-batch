#!/usr/bin/env python3

from aws_cdk import core

from aws_cdk_fargate_batch.aws_cdk_fargate_batch_stack import AwsCdkFargateBatchStack


app = core.App()
AwsCdkFargateBatchStack(app, "aws-cdk-fargate-batch")

app.synth()
