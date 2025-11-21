# Scanning Models with Protect AI Guardian Using Python

In today's rapidly evolving AI landscape, ensuring the security and integrity of machine learning models has become paramount. **Protect AI Guardian** is a comprehensive AI model security platform that helps developers and organizations defend against unseen threats while innovating securely. Guardian offers cutting-edge scanners that can identify deserialization attacks, architectural backdoors, and runtime threats across **35+ different model formats**, including PyTorch, TensorFlow, ONNX, and LLM-specific formats.

This tutorial will guide you through the process of scanning a model for vulnerabilities, biases, and security concerns using Protect AI Guardian's Python SDK. By the end of this guide, you'll understand how to:

- Set up Guardian in your Dataiku Python environment
- Load a model for scanning
- Review the results of a model scan

## Prerequisites

Before starting this tutorial, ensure you have:
* **Protect AI Guardian account** with API credentials
* Python 3.9 or higher
* A model ready for scanning (can be a 1st party or 3rd party model)
* A {doc}`code environment <refdoc:code-envs/index>` with the following packages:

    ```python
    guardian-client
    ```

## Step 1: Setting up the environment and session

Let's start by importing the necessary libraries and configuring our environment:

```python
from guardian_client import GuardianAPIClient
import requests
import json
import time

# Initialize Guardian with your credentials
# Note: Store these securely, preferably as environment variables
CLIENT_ID = 'your-client-id-here'
CLIENT_SECRET = 'your-client-secret-here'
SCANNER_ENDPOINT = 'your-guardian-endpoint-here'

def get_auth_token():
    """
    Obtains an authentication token from the Guardian API.
    """
    print("🔑 Obtaining authentication token...")
    url = f"{SCANNER_ENDPOINT}/v1/auth/client_auth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
    }
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Raises an exception for bad status codes (4xx or 5xx)
        token = response.json().get("access_token")
        if not token:
            raise ValueError("Access token not found in the response.")
        print("✅ Authentication successful.")
        return token
    except (requests.RequestException, ValueError) as e:
        print(f"❌ Failed to obtain authentication token: {e}")
        exit(1)    

auth_token = get_auth_token()
```

## Step 2: Submit the model to scan

Now, we will submit the model to be scanned:

```python
scan_url = f"{SCANNER_ENDPOINT}/v1/scans"
scan_headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": f"Bearer {auth_token}"
}
scan_data = {
    "scope": "PRIVATE",
    "model_uri": "your-model-location"
}

try:
    print("🔄 Submitting scan request...")
    scan_response = requests.post(scan_url, headers=scan_headers, json=scan_data, timeout=30)
    scan_response.raise_for_status()
    scan_result = scan_response.json()
    print("Scan submission response:")
    print(json.dumps(scan_result, indent=4))

    scan_id = scan_result.get("uuid")
    if not scan_id:
        print("❌ Failed to extract scan ID from submission response.")
        exit(1)    

    print(f"✅ Scan submitted successfully with ID: {scan_id}")

except requests.exceptions.RequestException as e:
    print(f"❌ Failed to submit scan request: {e}")
    exit(1)    
```

You can expect a response similar to this:
```{figure} ./assets/scan-submission.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 1 -- Model scan submission response

Figure 1 -- Model scan submission response
```

## Step 3: Poll for status and return the scan results

After you submit the model for scanning, there will be a short delay while the results are processed. We use polling to check for and retrieve the results once they are available:

```python
print("⏳ Polling scan status...")
status_url = f"{scan_url}/{scan_id}"
final_status_response = {}

while True:
    try:
        status_response = requests.get(status_url, headers=scan_headers, timeout=30)
        status_response.raise_for_status()
        status_data = status_response.json()
        status = status_data.get("aggregate_eval_outcome")

        if status and status != "PENDING":
            print(f"🏁 Scan completed with status: {status}")
            final_status_response = status_data
            break

        print("Scan Running...")
        time.sleep(5)  # Wait for 5 seconds before the next check

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to get status update: {e}")
        exit(1)

print("\nFinal Scan Results")
print(json.dumps(final_status_response, indent=4))
```

You can expect results in a similar format. The model we used is flagged as a FAIL because it does not use an approved file format:
```{figure} ./assets/scan-results.png
:align: center
:class: with-shadow image-popup w500
:alt: Figure 2 -- Model scan results

Figure 2 -- Model scan results
```

## Conclusion

Based on Guardian's findings, you will want to implement mitigation strategies (beyond the scope of this tutorial).
This tutorial demonstrated how to integrate **Protect AI Guardian** into your ML workflow to scan models
for security vulnerabilities, biases, and other concerns.
Guardian's comprehensive scanning capabilities help identify threats across deserialization attacks,
architectural backdoors, and runtime vulnerabilities.