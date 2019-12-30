from aws_cdk import core
from aws_cdk import aws_ecr

class AwsCdkFargateBatchStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # ====================================
        # ECR
        # ====================================
        ecr_repository = aws_ecr.Repository(
            self,
            id='ecr_repository',
            repository_name='sample_repository'
        )