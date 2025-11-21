import dataiku
from flask import request

@app.route('/upload-to-dss', methods = ['POST'])
def upload_to_dss():
    extra_param = request.form.get('extra', '')
    f = request.files.get('file')
    mf = dataiku.Folder('box') # name of the folder in the flow
    target_path = '/%s' % f.filename
    mf.upload_stream(target_path, f)
    return json.dumps({"status":"ok"})