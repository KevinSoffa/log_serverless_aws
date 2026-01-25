import boto3


lmb = boto3.client('lambda', region_name='us-east-1')
iam = boto3.client('iam')

def subir_lambda():
    role_arn = iam.get_role(RoleName='LambdaLogRole')['Role']['Arn']
    
    with open('lambda_function.zip', 'rb') as f:
        zipped_code = f.read()

    try:
        lmb.create_function(
            FunctionName='LogAnalyzer',
            Runtime='python3.9',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=15
        )
        print("Lambda 'LogAnalyzer' criado com sucesso.")
    except Exception as e:
        print(f"Erro ao subir Lambda: {e}")

if __name__ == "__main__":
    subir_lambda()