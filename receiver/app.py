import connexion
from connexion import NoContent
import json
import os
import requests
import yaml
import logging
import logging.config
from datetime import datetime
from pykafka import KafkaClient

with open("app_conf.yml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

def report_laundry_provider_location(body):
    unique_id = datetime.now().strftime('%H%M%S%f')
    logger.info('Received event request with a unique id of ' + unique_id)
    client = KafkaClient(hosts=(app_config["events"]["hostname"] + ":" + str(app_config["events"]["port"])))
    topic = client.topics[app_config["events"]["topic"]]
    producer = topic.get_sync_producer()
    msg = {
        "type": "reportService",
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body,
    }
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return (NoContent, 201)

def report_service_requested(body):
    unique_id = datetime.now().strftime('%H%M%S%f')
    logger.info('Received event request with a unique id of ' + unique_id)
    client = KafkaClient(hosts=(app_config["events"]["hostname"] + ":" + str(app_config["events"]["port"])))
    topic = client.topics[app_config["events"]["topic"]]
    producer = topic.get_sync_producer()
    msg = {
        "type": "requestService",
        "datetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "payload": body,
    }
    logger.info(msg['payload'])
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))
    return (NoContent, 201)

app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
