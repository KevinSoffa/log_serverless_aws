from datetime import datetime
from decouple import config
import base64
import boto3
import json
import gzip
import uuid


# Inicialização dos recursos AWS
dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')


TABLE_NAME = 'Incidents'
SNS_TOPIC_ARN = config("SNS-TOPIC-ARN")

def lambda_handler(event, context):
    """
    Recebe eventos do CloudWatch via Subscription Filter
    Filtra logs com nível ERROR
    Salva incidentes no DynamoDB.
    Publica alertas no SNS.
    """
    
    # 1. Decodificar e descompactar os dados do CloudWatch
    cw_data = event['awslogs']['data']
    compressed_payload = base64.b64decode(cw_data)
    uncompressed_payload = gzip.decompress(compressed_payload)
    payload = json.loads(uncompressed_payload)
    
    table = dynamodb.Table(TABLE_NAME)
    
    processed_count = 0
    
    for log_event in payload['logEvents']:
        try:
            # Tenta ler a mensagem como JSON (log estruturado da FastAPI)
            log_content = json.loads(log_event['message'])
            
            # 2. Filtrar logs com nível ERROR
            if log_content.get('level') == 'ERROR':
                incident_id = str(uuid.uuid4())
                
                # Montar o item conforme a estrutura do DynamoDB 
                incident = {
                    'incident_id': incident_id,
                    'service': log_content.get('service', 'fastapi-app'),
                    'message': log_content.get('message', 'Erro sem mensagem'),
                    'level': 'ERROR',
                    'timestamp': datetime.now().isoformat()
                }
                
                # 3. Salvar incidente no DynamoDB
                table.put_item(Item=incident)
                
                # 4. Disparar alerta em tempo real via SNS
                sns.publish(
                    TopicArn=SNS_TOPIC_ARN,
                    Subject=f"ALERTA: Erro em {incident['service']}",
                    Message=json.dumps(incident, indent=2)
                )
                
                processed_count += 1
                
        except (json.JSONDecodeError, KeyError):
            # Ignora logs que não estão no formato JSON esperado
            continue

    return {
        'statusCode': 200,
        'body': json.dumps(f'Processados {processed_count} erros com sucesso.')
    }