import os

import time

import sys
from flask import redirect, jsonify
from flask import request

from app import app
import ABBYY


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        abbyycli = ABBYY.AbbyyOnlineSdk(
            serverUrl='http://cloud.ocrsdk.com/',
            applicationId='Split with bot',
            password='0yvuAiBJJlVal9NEL5ks2O+5',
            settings={'country': 'russia'})
        task = abbyycli.ProcessReceipt(filepath, settings=abbyycli.settings)
        if task is None:
            print "Error"
            return redirect(request.url)
        if task.Status == "NotEnoughCredits":
            print "Not enough credits to process the document. Please add more pages to your application's account."
            return redirect(request.url)
        while task.IsActive():
            time.sleep(5)
            sys.stdout.write(".")
            task = abbyycli.GetTaskStatus(task)
            if task.Status == "Completed":
                if task.DownloadUrl is not None:
                    print 'SUCCESS'
                    return jsonify(abbyycli.DownloadResult(task, 'result'))
                print "Result was written to %s" % 'result'
        else:
            print "Error processing task"
            return redirect(request.url)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
