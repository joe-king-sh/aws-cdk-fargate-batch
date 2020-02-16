from aws_cdk import core
from aws_cdk import app_delivery
from aws_cdk import aws_codebuild
from aws_cdk import aws_codecommit
from aws_cdk import aws_codepipeline
from aws_cdk import aws_codepipeline_actions
import boto3

class ContinuousDeliveryStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, deploy_stack: core.Stack, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        # ========================================
        # CodePipeline
        # ========================================
        codepipeline = aws_codepipeline.Pipeline(
            self,
            id='sample_pipeline',
            pipeline_name='sample_pipeline_name',
        )
        
        
        # ============ source stage ============
        source_output = aws_codepipeline.Artifact('source_output')

        # Change to your setting.
        owner = 'joe-king-sh'
        repo = 'aws-cdk-fargate-batch'
        branch = 'master'
        oauth_token = get_parameters('GITHUB_OAUTH_TOKEN')
        
        # Create source collect stage.
        source_action = aws_codepipeline_actions.GitHubSourceAction(
            action_name='source_collect_action_from_github',
            owner=owner,
            repo=repo,
            trigger=aws_codepipeline_actions.GitHubTrigger.POLL,
            oauth_token=core.SecretValue.plain_text(oauth_token),
            output=source_output
        )
        # Add source stage to my pipeline.
        codepipeline.add_stage(
            stage_name='Source',
            actions=[source_action]
        )
        # ============ source stage ============


        # ============ build stage =============
        # Create build project.
        project = aws_codebuild.PipelineProject(
            self,
            id='sample_build_project',
            project_name='sample_build_project_name'
        )
        
        # Add build stage to my pipeline.
        build_output = aws_codepipeline.Artifact('build_output')
        codepipeline.add_stage(
            stage_name='Build',
            actions=[
                aws_codepipeline_actions.CodeBuildAction(
                    action_name='CodeBuild',
                    project=project,
                    input=source_output,
                    outputs=[build_output]
                )
           ]
        )
        # ============ build stage =============

        # ============ deploy stage ============
        # Add deploy stage to pipeline.
        codepipeline.add_stage(
            stage_name='Deploy',
            actions=[
                app_delivery.PipelineDeployStackAction(
                    stack=deploy_stack,
                    input=build_output,
                    admin_permissions=True,
                    change_set_name='change_set_name'
                )
            ]
        )
        # ============ deploy stage ============


def get_parameters(param_key):
    """
    Get parameter encrypted from parameter store.
    """
    ssm = boto3.client('ssm', region_name='ap-northeast-1')
    response = ssm.get_parameters(
        Names=[
            param_key,
        ],
        WithDecryption=True
    )
    return response['Parameters'][0]['Value']