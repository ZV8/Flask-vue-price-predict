import dill
import pandas as pd
import numpy as np
import os
import datetime
import pytz
import re
import pymorphy2
import dill
import uuid
import flask
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from time import strftime
from nltk.corpus import stopwords
from razdel import tokenize

import nltk
nltk.download('stopwords')

dill._dill._reverse_typemap['ClassType'] = type

EXAMPLES = [
    {
        'id': uuid.uuid4().hex,
        'date': '03-11-2021 16:42:40',
        'roomsCount': '2',
        'totalArea': '40',
        'kitchenArea': '6',
        'livingArea': '24',
        'floorNumber': '4',
        'floorsCount': '14',
        'lat_lng_min': '',
        'undergrounds': '69',
        'transportType': 'walk',
        'time': '5',
        'description': 'состояние среднее',
        'predict': '38912'
    }
]

# initialize our Flask application and the model
app = flask.Flask(__name__)
model = None

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

handler = RotatingFileHandler(filename='app.log', maxBytes=100000, backupCount=10)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


def load_model(model_path):
    # load the pre-trained model
    global model
    with open(model_path, 'rb') as f:
        model = dill.load(f)


modelpath = "/server/models/cian_test_pipeline.dill"
load_model(modelpath)


@app.route("/", methods=["GET"])
def general():
    return """Welcome to prediction process. Please use 'http://<address>/predict' to POST"""


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return flask.jsonify('pong!')


def remove_item(item_id):
    for example in EXAMPLES:
        if example['id'] == item_id:
            EXAMPLES.remove(example)
            return True
    return False


@app.route('/get-examples', methods=['GET'])
def all_examples():
    data = {"success": False}
    if flask.request.method == "GET":
        data["success"] = True
        data["examples"] = EXAMPLES[:50]
    # return the data dictionary as a JSON response
    return flask.jsonify(data)


@app.route('/predict', methods=['POST'])
def predict_object():
    data = {"success": False}

    tz_Moscow = pytz.timezone('Europe/Moscow')
    now_Moscow = datetime.datetime.now(tz_Moscow)
    dt = now_Moscow.strftime("[%Y-%b-%d %H:%M:%S]")
    date_in_obj = now_Moscow.strftime("%d-%m-%Y %H:%M:%S")
    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":

        # description, company_profile, benefits = "", "", ""
        roomsCount, totalArea, kitchenArea, livingArea, floorNumber, description, \
        lat_lng_min, undergrounds, transportType, time, floorsCount \
            = '0', '0', '0', '0', '0', '', '0_0', '0', 'unknown', '0', '0'
        request_json = flask.request.get_json()
        print('request_json', request_json)

        if request_json["roomsCount"]:
            roomsCount = request_json['roomsCount']
        if request_json["totalArea"]:
            totalArea = request_json['totalArea']
        if request_json["kitchenArea"]:
            kitchenArea = request_json['kitchenArea']
        if request_json["livingArea"]:
            livingArea = request_json['livingArea']
        if request_json["floorNumber"]:
            floorNumber = request_json['floorNumber']
        if request_json["description"]:
            description = request_json['description']
        if request_json["lat_lng_min"]:
            lat_lng_min = request_json['lat_lng_min']
        if request_json["undergrounds"]:
            undergrounds = request_json['undergrounds']
        if request_json["transportType"]:
            transportType = request_json['transportType']
        if request_json["time"]:
            time = request_json['time']
        if request_json["floorsCount"]:
            floorsCount = request_json['floorsCount']

        logger.info(f'{dt} Data: roomsCount={roomsCount}, totalArea={totalArea}, kitchenArea={kitchenArea}, '
                    f'livingArea={livingArea}, floorNumber={floorNumber},  description={description},  '
                    f'lat_lng_min={lat_lng_min}, undergrounds={undergrounds},  transportType={transportType},  '
                    f'time={time}, floorsCount={floorsCount}')
        try:
            preds = model.predict(pd.DataFrame({"roomsCount": [roomsCount], "totalArea": [totalArea],
                                                "livingArea": [livingArea], "floorNumber": [floorNumber],
                                                "description": [description], "lat_lng_min": [lat_lng_min],
                                                "undergrounds": [undergrounds], "transportType": [transportType],
                                                "time": [time], "floorsCount": [floorsCount],
                                                "kitchenArea": [kitchenArea]}))
        except AttributeError as e:
            logger.warning(f'{dt} Exception: {str(e)}')
            data['predictions'] = str(e)
            data['success'] = False
            return flask.jsonify(data)

        data["predictions"] = int(preds[0])
        # indicate that the request was a success
        data["success"] = True

        EXAMPLES.insert(0, {
            'id': uuid.uuid4().hex,
            'date': date_in_obj,
            'roomsCount': roomsCount,
            'totalArea': totalArea,
            'kitchenArea': kitchenArea,
            'livingArea': livingArea,
            'floorNumber': floorNumber,
            'floorsCount': floorsCount,
            'lat_lng_min': '',
            'undergrounds': undergrounds,
            'transportType': transportType,
            'time': time,
            'description': description,
            'predict': data["predictions"]
        })
        data['message'] = 'Объект добавлен!'
    else:
        data["success"] = False

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


@app.route('/delete/<item_id>', methods=['DELETE'])
def single_object(item_id):
    response_object = {'status': 'success'}
    if flask.request.method == 'DELETE':
        remove_item(item_id)
        response_object['message'] = 'Запись об объекте удалена!'
    return flask.jsonify(response_object)


# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
    print(("* Loading the model and Flask starting server..."
           "please wait until server has fully started"))
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
