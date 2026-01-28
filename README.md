# 📊 Sistema de Monitoramento e Logs Serverless na AWS

<div align="center">
  <img height="180em" src="https://raw.githubusercontent.com/KevinSoffa/API-previdencia-KevinSoffa/refs/heads/develop/img/Kevin%20Soffa%20(2).png"/>
</div>

Projeto de **observabilidade serverless** desenvolvido em **Python**, utilizando **AWS** e **boto3**, com foco em **monitoramento de aplicações**, **análise automática de erros** e **alertas em tempo real**.

Todo o provisionamento e integração com a AWS foi feito **programaticamente via boto3**, sem uso de Console ou IaC externos (Terraform / CloudFormation), reforçando o domínio da SDK da AWS em Python.

<img height="55em" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" />

<img height="55em" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" />

<img height="55em" src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-plain-wordmark.svg" />


---

## 🎯 Objetivo do Projeto

Construir uma solução completa para:

* Centralizar logs estruturados de uma aplicação Python
* Armazenar logs no **Amazon CloudWatch Logs**
* Processar eventos de erro automaticamente via **AWS Lambda**
* Persistir incidentes no **Amazon DynamoDB**
* Enviar alertas em tempo real com **Amazon SNS**

Projeto ideal para **portfólio de Desenvolvedor Python, Data Engineer ou Cloud Engineer**.

---

## 🧱 Arquitetura

```
API Python
   │
   ▼
CloudWatch Logs
   │ (Subscription Filter)
   ▼
AWS Lambda (Log Analyzer)
   ├── DynamoDB (Incidents)
   └── SNS (Alertas)
```

### Fluxo de Funcionamento

1. A API gera logs estruturados em JSON
2. Os logs são enviados ao CloudWatch Logs
3. Um **Subscription Filter** encaminha os logs para uma Lambda
4. A Lambda identifica eventos de erro
5. Os erros são persistidos no DynamoDB
6. Um alerta é disparado via SNS

---

## 🛠️ Stack Tecnológica

* **Python 3.10+**
* **boto3**
* **AWS Lambda**
* **AWS CloudWatch Logs**
* **AWS DynamoDB**
* **AWS SNS**
* **AWS IAM**

---

## 📁 Estrutura do Projeto

```
SCRIPTS/
├── api/
│   └── main.py                  # Aplicação Python que gera logs
│
├── aws/
│   ├── lambda/
│   │   ├── lambda_function.py   # Código da Lambda de análise de logs
│   │   └── lambda_function.zip  # Pacote para upload da Lambda
│   │
│   ├── create_base.py           # Criação de recursos base (IAM, SNS, DynamoDB)
│   ├── create_lambda.py         # Criação da função Lambda via boto3
│   ├── create_logs_lambda.py    # CloudWatch Logs + Subscription Filter
│   └── lambda_function.zip
```

---

## 🧾 Logs Estruturados

A aplicação gera logs em formato estruturado para facilitar análise automática:

### Exemplo de Log

```json
{
  "level": "ERROR",
  "message": "Erro ao processar requisição",
  "service": "orders-api",
  "trace_id": "abc-123"
}
```

---

## ⚙️ AWS Lambda — Log Analyzer

A função Lambda é acionada automaticamente pelo CloudWatch Logs e executa:

* Leitura dos eventos de log
* Filtro por nível `ERROR`
* Persistência do incidente no DynamoDB
* Publicação de alerta no SNS

Essa abordagem garante **processamento assíncrono, escalável e de baixo custo**.

---

## 🗄️ DynamoDB — Tabela `Incidents`

| Campo       | Tipo | Descrição           |
| ----------- | ---- | ------------------- |
| incident_id | PK   | Identificador único |
| service     | STR  | Serviço de origem   |
| message     | STR  | Mensagem de erro    |
| level       | STR  | Nível do log        |
| timestamp   | STR  | Data/hora do evento |

---

## 🚨 Alertas com SNS

Sempre que um erro é detectado:

* Um evento é publicado em um tópico SNS
* Os assinantes recebem notificações (e-mail / SMS / integrações futuras)

Isso permite **resposta rápida a falhas em produção**.

---

## 🚀 Como Executar o Projeto

### 1️⃣ Configurar credenciais AWS

```bash
aws configure
```

### 2️⃣ Criar infraestrutura base

```bash
python aws/create_base.py
```

### 3️⃣ Criar função Lambda

```bash
python aws/create_lambda.py
```

### 4️⃣ Criar CloudWatch Logs + Subscription Filter

```bash
python aws/create_logs_lambda.py
```

### 5️⃣ Executar a API

```bash
python api/main.py
```

---

## 🔮 Evoluções Futuras

* 📈 Dashboards no CloudWatch
* 🔥 Classificação de severidade (LOW / MEDIUM / CRITICAL)
* 🔗 Correlação por `trace_id`
* 🕒 Política de retenção de logs
* 💬 Integração com Slack / Teams
* 🧪 Testes automatizados

---

## 📌 Considerações Finais

Este projeto demonstra:

* Uso prático de **boto3 em produção**
* Arquitetura **serverless orientada a eventos**
* Boas práticas de **observabilidade**
* Integração real entre serviços AWS

Ideal para **portfólio técnico** e estudos avançados em cloud.

---
## ▶️ Exemplo

### Table Incidents
<div align="center">
  <img src="https://raw.githubusercontent.com/KevinSoffa/log_serverless_aws/refs/heads/master/imagens_logs/table_incidents.png"/>
</div>

### Lambda
<div align="center">
  <img src="https://raw.githubusercontent.com/KevinSoffa/log_serverless_aws/refs/heads/master/imagens_logs/lambda.png"/>
</div>

---
👨‍💻 **Autor**: Kevin Soffa

📎 Projeto desenvolvido para fins educacionais e demonstração técnica.
