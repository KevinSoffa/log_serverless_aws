from watchtower import CloudWatchLogHandler
from fastapi import FastAPI
import logging
import json


app = FastAPI()

# Configura o logger para enviar ao grupo que você criou
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("FastAPI-App")
logger.addHandler(CloudWatchLogHandler(log_group="fastapi-logs"))

@app.get("/gerar-erro")
async def disparar_erro():
    # Log estruturado conforme definido no projeto [cite: 21, 22]
    erro_payload = {
        "level": "ERROR",
        "message": "Falha crítica na API de Teste 3",
        "service": "checkout-service"
    }
    logger.error(json.dumps(erro_payload))
    return {"status": "Erro enviado ao CloudWatch"}