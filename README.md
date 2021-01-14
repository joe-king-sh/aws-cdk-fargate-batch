# aws-cdk-fargate-batch
Repository for building python batches running on Fargate with AWS CDK.

## Getting Started

### Prerequisites

- Python 3.6.8
- aws-cdk 1.19.0
- pipenv 2018.11.26

### Installing

1. aws-cdk cli
    
    ```bash
    $ npm install aws-cdk
    $ cdk --version
    1.19.0 (build 5597bbe)$ 
    ```

2. pipenv

    ```bash
    $ pip install pipenv
    ```

3. python library

    ```bash
    $ pipenv run install -d
    ```

### Deployment

#### Deploy CodePipelineStack

```bash
cdk deploy continuous-delivery
```
#### Deploy FargateBatchStck

Deploy automatically using codepipeline.

## Reference
[AWS-CDK app_delivery](https://docs.aws.amazon.com/cdk/api/latest/python/aws_cdk.app_delivery.README.html)

## Link
[AWS CDKをデプロイするCodepipelineをCDK(Python)で構築する](https://qiita.com/joe-king-sh/items/fbd6e185632adf75a1a3)
