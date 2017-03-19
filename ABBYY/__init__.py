#!/usr/bin/python

import argparse
import base64
import getopt
import MultipartPostHandler
import os
import re
import sys
import time
import urllib2
import urllib
import xml.dom.minidom

from json import dumps
from xmljson import gdata as bf
from xml.etree.ElementTree import fromstring


class Task:
    Status = "Unknown"
    Id = None
    DownloadUrl = None

    def IsActive(self):
        if self.Status == "InProgress" or self.Status == "Queued":
            return True
        else:
            return False


class AbbyyOnlineSdk:
    def __init__(self,
                 serverUrl='http://cloud.ocrsdk.com/',
                 applicationId='applicationId',
                 password='password',
                 settings={},
                 proxy=None,
                 debuglevel=0):
        self.serverUrl = serverUrl
        self.applicationId = applicationId
        self.password = password
        self.settings = settings
        self.proxy = proxy
        self.debuglevel = debuglevel

    def ProcessReceipt(self, filePath, settings):
        urlParams = urllib.urlencode(settings)
        requestUrl = self.serverUrl + "processReceipt?" + urlParams

        bodyParams = {"file": open(filePath, "rb")}
        request = urllib2.Request(requestUrl, None, self.buildAuthInfo())
        response = self.getOpener().open(request, bodyParams).read()
        if response.find('<Error>') != -1:
            return None
        task = self.DecodeResponse(response)
        return task

    def GetTaskStatus(self, task):
        if task.Id.find('00000000-0') != -1:
            print "Null task id passed"
            return None

        urlParams = urllib.urlencode({"taskId": task.Id})
        statusUrl = self.serverUrl + "getTaskStatus?" + urlParams
        request = urllib2.Request(statusUrl, None, self.buildAuthInfo())
        response = self.getOpener().open(request).read()
        task = self.DecodeResponse(response)
        return task

    def DownloadResult(self, task, outputPath):
        getResultUrl = task.DownloadUrl
        if getResultUrl is None:
            print "No download URL found"
            return
        request = urllib2.Request(getResultUrl)
        fileResponse = self.getOpener().open(request).read()
        resultFile = open(outputPath, "wb")
        resultFile.write(fileResponse)
        # return dumps(bf.data(fromstring(fileResponse)))
        # print fileResponse
        print convert(fileResponse)
        return convert(fileResponse)

        return fileResponse

    def DecodeResponse(self, xmlResponse):
        dom = xml.dom.minidom.parseString(xmlResponse)
        taskNode = dom.getElementsByTagName("task")[0]
        task = Task()
        task.Id = taskNode.getAttribute("id")
        task.Status = taskNode.getAttribute("status")
        if task.Status == "Completed":
            task.DownloadUrl = taskNode.getAttribute("resultUrl")
        return task

    def buildAuthInfo(self):
        return {"Authorization": "Basic %s" % base64.b64encode("%s:%s" % (self.applicationId, self.password))}

    def getOpener(self):
        if self.proxy is None:
            self.opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler,
                                               urllib2.HTTPHandler(debuglevel=self.debuglevel))
        else:
            self.opener = urllib2.build_opener(
                self.proxy,
                MultipartPostHandler.MultipartPostHandler,
                urllib2.HTTPHandler(debuglevel=self.debuglevel))
        return self.opener


import xmltodict


def convert(xml_file, xml_attribs=True):
    d = xmltodict.parse(xml_file, xml_attribs=xml_attribs)
    item = d['receipts']['receipt']['recognizedItems']['item']
    l = [(x['name']['text'], x['total']['normalizedValue']) for x in item]
    return list(l)
