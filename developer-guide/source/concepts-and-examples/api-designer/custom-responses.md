(custom-responses)=

# Return custom HTTP responses

## Define returned HTTP status codes
Using the `DkuCustomApiException` class, you can control which HTTP status code and message are returned by a deployed API endpoint. This is helpful when you want to handle unexpected response states.

The `DkuCustomApiException` exception's constructor has two parameters:
- `message` - mandatory
- `http_status_code` - optional with the default value of `500`

### Python function
```py
def api_py_function(p1, p2, p3):
    http_headers = dku_http_request_metadata.headers

    # Your custom logic for handling specific header values
    if not http_headers.get("Authorization"):
        raise DkuCustomApiException("The caller is not authorized", http_status_code=401)

    # Python function logic
    result = ...

    return result
```

### Custom prediction (classification)
The `DkuCustomApiException` class is only accessible from the `predict` method

```py
from  dataiku.apinode.predict.predictor import ClassificationPredictor
import pandas as pd
    def predict(self, features_df):
        http_headers = dku_http_request_metadata.headers

        # Your custom logic for handling specific header values
        if not http_headers.get("Authorization"):
            raise DkuCustomApiException("The caller is not authorized", http_status_code=401)

        # Prediction logic
        ...
```

### Custom prediction (regression)
The `DkuCustomApiException` class is only accessible from the `predict` method

```py
from  dataiku.apinode.predict.predictor import RegressionPredictor
import pandas as pd
class MyPredictor(RegressionPredictor):
    def predict(self, features_df):
        http_headers = dku_http_request_metadata.headers

        # Your custom logic for handling specific header values
        if not http_headers.get("Authorization"):
            raise DkuCustomApiException("The caller is not authorized", http_status_code=401)

        # Prediction logic
        ...
```

## Customize HTTP response content

**Warning:** this feature is only available for Python function endpoints.

The `DkuCustomHttpResponse` can help define the response content type and HTTP headers returned by a deployed Python function API endpoint.

The feature is disabled by default and can be enabled in Python function endpoint settings by checking the "Returns custom response" option.
Only the **Static Dataiku API node** and **Kubernetes cluster** infrastructure types support this feature.

### Text response
```py
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    response = DkuCustomHttpResponse.create_text_response("Hello, World!")
    return response
```

### XML response
```py
import xml.etree.ElementTree as ET
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    root = ET.Element("person")
    name = ET.SubElement(root, "name")
    name.text = "John Doe"
    age = ET.SubElement(root, "age")
    age.text = str(42)
    xml_string = ET.tostring(root, encoding="unicode")
    response = DkuCustomHttpResponse.create_text_response(xml_string, content_type="text/xml")
    return response
```

### JSON response
```py
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    my_values = dict()
    my_values["a"] = "b"
    my_values["c"] = ["e", 42]
    return DkuCustomHttpResponse.create_json_response(my_values, content_type="application/json")
```

### Image response
You can use a content type that reflects the type of the image: `image/png`, `image/jpg`, etc. All common MIME types can be found [here](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/MIME_types/Common_types).

```py
import base64
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    obj = base64.b64decode("<your-image-encoded-with-base64>")
    response = DkuCustomHttpResponse.create_binary_response(obj, content_type="image/png")
    return response
```

### Extra headers
```py
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    response = DkuCustomHttpResponse.create_text_response("Hello, World!")
    # Add headers after instantiation
    response.headers["Machin"] = "Truc"
    # Using the add_header method, define multiple headers with the same key. Valid in a limited set of cases, such as Set-Cookie
    response.add_header("Set-Cookie", "chocolate")
    response.add_header("Set-Cookie", "pecan")
    return response
```

### Using the direct initialization of `DkuCustomHttpResponse`
```py
from dataiku.apinode import DkuCustomHttpResponse

def api_py_function():
    response = DkuCustomHttpResponse(
        200,
        "Hello No Helper World", {
        "Content-Type": "text/plain",
        "Content-Encoding": "utf-8"
        }
    )
    return response
```