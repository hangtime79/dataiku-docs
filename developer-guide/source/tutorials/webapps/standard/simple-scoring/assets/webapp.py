from flask import request
import dataikuapi


@app.route('/score', methods=['POST'])
def getit():
    """
    Query the API endpoint with the data passed in the body of the request.

    Returns:
        A response object containing the prediction is everything goes well
        or an object with an error as the result.
    """
    body = request.get_json()
    url = body.get('url', None)
    endpoint = body.get('endpoint', None)
    features = body.get('features', None)
    if url and endpoint and features:
        try:
            client = dataikuapi.APINodeClient(url, endpoint)
            record_to_predict = features
            prediction = client.predict_record("predict_authorized", record_to_predict)
            return prediction
        except Exception as e:
            return {"result": str(e)}
    else:
        return {"result": "Unable to reach the endpoint"}
