import boto3
import json


region = "us-east-1"
iam = boto3.client('iam', region_name=region)
dynamodb = boto3.client('dynamodb', region_name=region)
sns = boto3.client('sns', region_name=region)
logs = boto3.client('logs', region_name=region)

def criar_base():
    # 1. DynamoDB: Tabela de Incidentes [cite: 8, 32]
    try:
        dynamodb.create_table(
            TableName='Incidents',
            KeySchema=[{'AttributeName': 'incident_id', 'KeyType': 'HASH'}],
            AttributeDefinitions=[{'AttributeName': 'incident_id', 'AttributeType': 'S'}],
            BillingMode='PAY_PER_REQUEST'
        )
        print("Tabela DynamoDB criada.")
    except: print("Tabela DynamoDB já existe.")

    # 2. SNS: Tópico de Alertas [cite: 9, 31]
    topic = sns.create_topic(Name='LogAlerts')
    print(f"Tópico SNS: {topic['TopicArn']}")

    # 3. CloudWatch: Log Group para a FastAPI [cite: 6, 21]
    try:
        logs.create_log_group(logGroupName='fastapi-logs')
        logs.put_retention_policy(logGroupName='fastapi-logs', retentionInDays=1)
        print("Log Group criado.")
    except: print("Log Group já existe.")

    # 4. IAM: Role do Lambda [cite: 20]
    policy = {
        "Version": "2012-10-17",
        "Statement": [{"Effect": "Allow", "Principal": {"Service": "lambda.amazonaws.com"}, "Action": "sts:AssumeRole"}]
    }
    try:
        role = iam.create_role(RoleName='LambdaLogRole', AssumeRolePolicyDocument=json.dumps(policy))
        for p in ['arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole', 
                  'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess', 
                  'arn:aws:iam::aws:policy/AmazonSNSFullAccess']:
            iam.attach_role_policy(RoleName='LambdaLogRole', PolicyArn=p)
        print("Role IAM criada.")
    except: print("Role IAM já existe.")

if __name__ == "__main__":
    criar_base()