from aws_cdk import core
from aws_cdk import aws_ecr
from aws_cdk import aws_ec2

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
        
        # ====================================
        # VPC
        # ====================================
        vpc = aws_ec2.Vpc(self,
            id='vpc',
            cidr='10.0.0.0/16',
            max_azs=2,
            nat_gateways=1,
            vpn_gateway=False
        )


        # ====================================
        # ECS
        # ====================================
        # クラスターの作成
        ecs_cluster = aws_ecs.Cluster(
            self,
            id='ecs_cluster,
            cluster_name='sample_cluester_name',
            vpc=vpc
        )

        # Fargeteのタスク定義の作成
        fargate_task_definition = ecs.FargateTaskDefinition(
            self,
            id=utility.create_name(project_name, 'task-def'),
            cpu=256,
            memory_limit_mib=512,
            family=utility.create_name(project_name, 'task-def')
        )

        # タスク定義にコンテナイメージを登録する
        fargate_task_definition.add_container(
            id=utility.create_name(project_name, 'container-image'),
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
            logging=ecs.LogDriver.aws_logs(
                stream_prefix='ecs',
                log_group=logs.LogGroup(
                    self,
                    id=utility.create_name(project_name, 'log-group'),
                    log_group_name='/ecs/fargate/{}'.format(project_name)
                )
            )
            # environment
        )

        # 定期実行するようにイベントに紐付ける
        rule = events.Rule(
            self,
            id=utility.create_name(project_name, 'rule'),
            rule_name=utility.create_name(project_name, 'execute-task-rule'),
            description='Event rule for using in {} project to execute ecs task.'.format(project_name),
            schedule=events.Schedule.cron(
                day=None,
                hour=None,
                minute='*/5',
                month=None,
                week_day=None,
                year='1970'
            )
        )

        rule.add_target(
            target=targets.EcsTask(
                cluster=ecs_cluster,
                task_definition=fargate_task_definition,
                task_count=1,
                security_group=sg_lambda,  # やることはLambdaと同じなので同じSGをつける
                subnet_selection=ec2.SubnetSelection(subnets=private_subnets)
            )
        )