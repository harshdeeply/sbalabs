import connexion
from connexion import NoContent
import json
import os
import logging
import logging.config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from report_service import ReportService
from request_service import RequestService
from base import Base
import datetime
import yaml
from pykafka import KafkaClient
from pykafka.common import OffsetType
from threading import Thread

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

DB_ENGINE = create_engine(
    "mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
        app_config["datastore"]["user"],
        app_config["datastore"]["password"],
        app_config["datastore"]["hostname"],
        app_config["datastore"]["port"],
        app_config["datastore"]["db"],
    )
)
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_request_service(timestamp):
    """ Gets new request service after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = timestamp
    readings = session.query(RequestService).filter(
        RequestService.date_created >= timestamp_datetime
    )
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info(
        "Query for requested service after %s returns %d results"
        % (timestamp, len(results_list))
    )
    return results_list, 200


def get_report_service(timestamp):
    """ Gets new reported service after the timestamp """
    session = DB_SESSION()
    timestamp_datetime = timestamp
    readings = session.query(ReportService).filter(
        ReportService.date_created >= timestamp_datetime
    )
    results_list = []
    for reading in readings:
        results_list.append(reading.to_dict())
    session.close()
    logger.info(
        "Query for reported service after %s returns %d results"
        % (timestamp, len(results_list))
    )
    return results_list, 200


def process_messages():
    """ Process event messages """
    hostname = "%s:%d" % (
        app_config["events"]["hostname"],
        app_config["events"]["port"],
    )
    client = KafkaClient(hosts=hostname)
    topic = client.topics[app_config["events"]["topic"]]
    # Create a consume on a consumer group, that only reads new messages
    consumer = topic.get_simple_consumer(
        consumer_group="event_group",
        reset_offset_on_start=False,
        auto_offset_reset=OffsetType.LATEST,
    )
    # This is blocking -it will wait for a new message
    for msg in consumer:
        msg_str = msg.value.decode("utf-8")
        msg = json.loads(msg_str)
        payload = msg["payload"]
        if msg["type"] == "reportService":  # Change this to your event type
            session = DB_SESSION()
            repSer = ReportService(
                payload["businessID"],
                payload["serviceOffered"],
                payload["openingHours"],
                payload["closingHours"],
                payload["phoneNumber"],
                payload["streetAddress"]["streetNumber"],
                payload["streetAddress"]["city"],
                payload["streetAddress"]["province"],
                payload["streetAddress"]["country"],
                payload["streetAddress"]["postalCode"],
            )
            session.add(repSer)
            session.commit()
            session.close()
        elif msg["type"] == "requestService":  # Change this to your event type
            session = DB_SESSION()
            reqSer = RequestService(
                payload["serviceType"],
                payload["laundryType"],
                payload["numberOfItems"],
                payload["phoneNumber"],
                payload["emailAddress"],
                payload["streetAddress"]["streetNumber"],
                payload["streetAddress"]["city"],
                payload["streetAddress"]["province"],
                payload["streetAddress"]["country"],
                payload["streetAddress"]["postalCode"],
            )
            session.add(reqSer)
            session.commit()
            session.close()

        # Commit the new message as being read
        consumer.commit_offsets()


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", base_path="/storage", strict_validation=True, validate_responses=True)

if __name__ == "__main__":
    t1 = Thread(target=process_messages)
    t1.setDaemon(True)
    t1.start()
    app.run(port=8090)
