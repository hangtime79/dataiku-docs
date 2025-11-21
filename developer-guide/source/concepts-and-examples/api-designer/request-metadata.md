(request-metadata)=

# Access HTTP Request Metadata

You can access the metadata of HTTP requests from "Python function" and "Custom prediction (Python)" endpoints by using the `dku_http_request_metadata` variable within your custom code.

The `dku_http_request_metadata` variable is an object with the following properties:
- `headers` - an instance of [`wsgiref.headers.Headers`](https://docs.python.org/3/library/wsgiref.html#wsgiref.headers.Headers) that holds headers used in a request.
- `path` - a relative URL's path as a string to which the client sent an HTTP request. Example: `"/public/api/v1/python-service/py-func/run"`.

The feature is disabled by default and can be enabled by an infrastructure admin in the following ways:
- Use the *"Enable `dku_http_request_metadata` variable"* setting in the general settings of the **Kubernetes cluster**, **Azure ML**, **Amazon SageMaker**, **Snowflake Snowpark**, and **Google Vertex AI** infrastructures.
- On a **Static Dataiku API node** infrastructure, add the following key-value pair to an API node's `<api-node-root-dir>/config/server.json` file
  ```json
  "isRequestMetadataEnabled": true
  ```
- The variable is always enabled when running test queries in the API Designer

## Python function
```py
def api_py_function():
    # Your custom logic for handling specific header values
    if not dku_http_request_metadata.headers.get("Authorization"):
        raise Exception("Received no Authorization header")

    # Python function logic
    result = ...

    return result
```

## Custom prediction (classification)
The `dku_http_request_metadata` is accessible from the `predict` method

```py
from  dataiku.apinode.predict.predictor import ClassificationPredictor
import pandas as pd
class MyPredictor(ClassificationPredictor):
    def predict(self, features_df):
        # Your custom logic for handling specific header values
        if not dku_http_request_metadata.headers.get("Authorization"):
            raise Exception("Received no Authorization header")

        # Prediction logic
        predictions = ...
        return (predictions, None)
```

## Custom prediction (regression)
The `dku_http_request_metadata` is accessible from the `predict` method

```py
from  dataiku.apinode.predict.predictor import RegressionPredictor
import pandas as pd
class MyPredictor(RegressionPredictor):
    def predict(self, features_df):
        # Your custom logic for handling specific header values
        if not dku_http_request_metadata.headers.get("Authorization"):
            raise Exception("Received no Authorization header")

        # Prediction logic
        predictions = ...
        return (predictions, None)
```
