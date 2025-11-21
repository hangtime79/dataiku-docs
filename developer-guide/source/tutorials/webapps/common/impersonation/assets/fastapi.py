import dataiku
import pandas as pd
from fastapi import Request
from fastapi.responses import JSONResponse

import logging

logger = logging.getLogger(__name__)


# Example:
# As the Python webapp backend is a FastAPI app, refer to the FastAPI
# documentation for more information about how to adapt this
# example to your needs.
# From JavaScript, you can access the defined endpoints using
# getWebAppBackendUrl('get_user_name')

@app.get("/get_user_name")
async def get_user_name(request: Request):
    logger.info("In it")
    logger.info(request)
    # Get user information from the request (can be done with impersonation)
    headers = dict(request.headers)
    auth_info = dataiku.api_client().get_auth_info_from_browser_headers(headers)
    return JSONResponse(content=auth_info.get("associatedDSSUser"))

    # Example of impersonation usage

#    with dataiku.WebappImpersonationContext() as ctx:
#        logger.info('impersonation')
#        # Using this context, your actions here will be impersonated.
#        client = dataiku.api_client()
#        user = client.get_own_user()
#        settings = user.get_settings()
#        logger.info(settings.get_raw())
#        return json.dumps(settings.get_raw().get('displayName'))


@app.get("/build_dataset")
async def build_dataset(datasetToBuild: str):
    logger.info("Impersonation begins...")
    with dataiku.WebappImpersonationContext() as context:
        # Each time your need to do impersonation, you need to obtain a client.
        # Dash cannot store objects that are not in JSON format.
        local_client = dataiku.api_client()
        project = local_client.get_default_project()
        outdataset = project.get_dataset(datasetToBuild)
        outdataset.build()

    logger.info("Impersonation ends...")
    return JSONResponse(content={"success": True})