import boto3


logs = boto3.client('logs', region_name='us-east-1')
lmb = boto3.client('lambda', region_name='us-east-1')

def conectar_logs_ao_lambda():
    lambda_arn = lmb.get_function(FunctionName='LogAnalyzer')['Configuration']['FunctionArn']
    
    # Permissão para o CloudWatch invocar o Lambda
    try:
        lmb.add_permission(
            FunctionName='LogAnalyzer',
            StatementId='cwlogs',
            Action='lambda:InvokeFunction',
            Principal='logs.amazonaws.com'
        )
    except: pass

    # Criar o Filtro [cite: 28, 29]
    logs.put_subscription_filter(
        logGroupName='fastapi-logs',
        filterName='ErrorFilter',
        filterPattern='{ $.level = "ERROR" }',
        destinationArn=lambda_arn
    )
    print("Conexão estabelecida! O sistema já está monitorando.")

if __name__ == "__main__":
    conectar_logs_ao_lambda()
