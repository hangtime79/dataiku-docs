import dataiku
import pandas as pd
from flask import Response, request
import logging
import json


@app.route('/first_form', methods=['POST', 'PUT'])
def first_form():
    """
    Process the request sent from the frontend.

    :return: a response containing the data coming from the request.
    """
    request_body = request.get_json()
    resp = add_json_to_dataset(request_body)

    response = Response(response=json.dumps(resp),
                        status=resp['status'],
                        mimetype='application/json')
    response.headers["Content-Type"] = "text/json; charset=utf-8"
    return response


def add_content_to_dataset(name, json):
    """
    Add a new row in JSON format to an existing data.
    :param name: Name of the dataset.
    :param json: Value to append.
    """
    dataset = dataiku.Dataset(name)
    df = dataset.get_dataframe()
    df = df.append(json, ignore_index=True)
    logging.info(df.head())
    dataset.write_dataframe(df)


def add_json_to_dataset(json):
    """
    Add a row to a dataset, only if the dataset exists.
    :param json: Value to add.
    :return: a dict representing the result of the addition.
    """

    # This could be a part of data sent by the frontend.
    dataset_name = "mydataset"
    client = dataiku.api_client()
    project = client.get_default_project()
    dataset = project.get_dataset(dataset_name)
    if dataset.exists():
        add_content_to_dataset(dataset_name, json)
        return {'status': 200, 'name': json.get('name', '')}
    else:
        return {'status': 400, 'reason': "Dataset {} does not exist".format(dataset_name)}
