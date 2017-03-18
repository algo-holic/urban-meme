import os

# from app import app

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
import time

import sys

import ABBYY

abbyycli = ABBYY.AbbyyOnlineSdk(
    serverUrl='http://cloud.ocrsdk.com/',
    applicationId='Split with bot',
    password='0yvuAiBJJlVal9NEL5ks2O+5',
    settings={'country': 'russia'})

task = abbyycli.ProcessReceipt('test2.jpg', settings=abbyycli.settings)

if task is None:
    print "Error"
    exit(1)
if task.Status == "NotEnoughCredits":
    print "Not enough credits to process the document. Please add more pages to your application's account."
    exit(2)

sys.stdout.write("Waiting..")
while task.IsActive() == True:
    time.sleep(5)
    sys.stdout.write(".")
    task = abbyycli.GetTaskStatus(task)


    if task.Status == "Completed":
        if task.DownloadUrl != None:
            abbyycli.DownloadResult(task, 'result')
            print "Result was written to %s" % 'result'
    else:
        print "Error processing task"

