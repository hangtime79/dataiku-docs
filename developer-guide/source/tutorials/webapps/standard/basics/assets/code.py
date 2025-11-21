import dataiku
import pandas as pd
import json
from flask import request

sfpd = dataiku.Dataset("sfpd_enriched").get_dataframe()
# Only keep valid locations and criminial incidents
sfpd = sfpd[(sfpd.longitude != 0) & (sfpd.latitude != 0) & (sfpd.Category != "NON-CRIMINAL")]


# The Python backend is implemented with Flask. It reuses the concept of routes to map the data exchanges with the frontend.

@app.route('/Count_crime')
def count_crime():
    year = int(request.args.get("year"))
    # Filter data for the chosen year
    tab = sfpd[["longitude", "latitude"]][(sfpd.year == year)]

    # Group incident locations into bins
    x_bin = pd.cut(tab.longitude, 25, retbins=True, labels=False)
    y_bin = pd.cut(tab.latitude, 25, retbins=True, labels=False)
    tab["longitude"] = x_bin[0]
    tab["latitude"] = y_bin[0]
    tab["C"] = 1

    # Group incidents by binned locations and count them
    gp = tab.groupby(["longitude", "latitude"])
    df = gp["C"].count().reset_index()
    max_cr = max(df.C)
    min_cr = min(df.C)
    gp_js = df.to_json(orient="records")

    # Return a JSON-formatted string containing incident counts by location and location limits
    return json.dumps({
        "bin_x": list(x_bin[1]),
        "bin_y": list(y_bin[1]),
        "nb_crimes": eval(gp_js),
        "min_nb": min_cr,
        "max_nb": max_cr
    })
