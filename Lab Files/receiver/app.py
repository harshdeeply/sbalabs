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

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, "r") as f:
    app_config = yaml.safe_load(f.read())

with open(log_conf_file, "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

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
app.add_api("openapi.yaml", base_path="/receiver", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    app.run(port=8080)
