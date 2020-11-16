import connexion
from connexion import NoContent
import json
import os
import logging
import logging.config
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
import yaml
import requests

def initJsonFile():
    if os.path.isfile("events.json") == False:
        with open("events.json", "w") as jsonfile:
            json.dump({"stats": []}, jsonfile)


def write_json(data, filename="events.json"):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def writeJsonFile(body):
    with open("events.json", "r+") as jsonfile:
        data = json.load(jsonfile)
        temp = data["stats"]
        if len(temp) == 0:
            temp.append(body)
        else:
            temp[0] = body
    write_json(data)


with open("app_conf.yaml", "r") as f:
    app_config = yaml.safe_load(f.read())

with open("log_conf.yml", "r") as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger("basicLogger")


def get_stats():
    """ Gets stats """
    logger.info("getting stats request")
    with open("events.json") as r:
        stats = json.load(r)
    logger.info("got following stats: " + str(stats["stats"]))
    logger.info("completed the stats request")
    return stats["stats"], 200


def populate_stats():
    """ Periodically update stats """
    try:
        with open(app_config["datastore"]["filename"]) as r:
            stats = json.load(r)
            time = stats["stats"][0]["timestamp"]
            print(time)
    except:
        time = str(datetime.datetime.now())
    logger.info("Start Periodic Processing")
    response_request_service = requests.get(
        app_config["eventstore"]["url"] + "/requestService", params={"timestamp": time}
    )
    response_report_service = requests.get(
        app_config["eventstore"]["url"] + "/laundryRegister", params={"timestamp": time}
    )
    response_request_service_json = json.loads(response_request_service.content)
    response_report_service_json = json.loads(response_report_service.content)
    if (
        response_report_service.status_code == 200
        and response_request_service.status_code == 200
        and response_report_service_json != []
        and response_request_service_json != []
    ):
        try:
            with open(app_config["datastore"]["filename"]) as r:
                stats = json.load(r)
                num_request_service_j = stats["stats"][0]["num_request_service"]
                num_report_service_j = stats["stats"][0]["num_report_service"]
                max_num_of_item_j = stats["stats"][0]["max_num_of_item"]
        except:
            num_request_service_j = 0
            num_report_service_j = 0
            max_num_of_item_j = 0
        time = str(datetime.datetime.now())
        logger.info("received events")
        num_request_service = len(response_request_service_json) + num_request_service_j
        num_report_service = len(response_report_service_json) + num_report_service_j
        max_num_of_item = max(
            [x["numberOfItems"] for x in response_request_service_json]
        )
        if max_num_of_item < max_num_of_item_j:
            max_num_of_item = max_num_of_item_j
        stat_obj = {
            "max_num_of_item": max_num_of_item,
            "num_report_service": num_report_service,
            "num_request_service": num_request_service,
            "timestamp": time,
        }
        writeJsonFile(stat_obj)
        logger.debug("Updated stats: " + str(stat_obj))
    else:
        time_obj = {"timestamp": time}
        try:
            with open(app_config["datastore"]["filename"]) as r:
                stats = json.load(r)
                num_request_service_j = stats["stats"][0]["num_request_service"]
                num_report_service_j = stats["stats"][0]["num_report_service"]
                max_num_of_item_j = stats["stats"][0]["max_num_of_item"]
                stat_obj = {
                    "max_num_of_item": max_num_of_item_j,
                    "num_report_service": num_report_service_j,
                    "num_request_service": num_request_service_j,
                    "timestamp": time,
                }
                writeJsonFile(stat_obj)
        except:
            writeJsonFile(time_obj)
        logger.error("Did not get any events")
    logger.info("Ended Periodic Processing")


def init_scheduler():
    sched = BackgroundScheduler(daemon=True)
    sched.add_job(
        populate_stats, "interval", seconds=app_config["scheduler"]["period_sec"]
    )
    sched.start()


app = connexion.FlaskApp(__name__, specification_dir="")
app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)

initJsonFile()
if __name__ == "__main__":
    init_scheduler()
    initJsonFile()
    app.run(port=8100, use_reloader=False)
