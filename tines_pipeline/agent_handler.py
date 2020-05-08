import sys
import json
import urllib.request
import re
import argparse

#Steps:
#Accept tiny-tines json as cmd line arg input
#Get agents from array
#Pipeline Starts
#Get agent type
#HTTP req to appropriate service
#Get response
#Build output based on Input Agent - type, name and options
#Perform next action as required(Print, Email, etc,.)
#Pipeline Ends
#

#Utility class to convert json to python dict
class dotdict(dict):
    #dot.notation access to dictionary attributes
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

#Main pipeline class
class Pipeline(object):
    def __init__(self, items):
        #Function man, function man. Does whatever a function can.
        self.items = items
        # self.internalJson = {}
        self.internalJson = dotdict({})

    def start(self):
        for item in self.items:
            getattr(self, item['type'])(item)

    def HTTPRequestAgent(self, input):
        try:
            #Handles HTTP requests
            URL = self.buildMacro(input['options']['url'])
            req = urllib.request.Request(URL)
            #parsing response
            response = urllib.request.urlopen(req)
            if(response.getcode() == 200):
                jsonResponse = json.loads(response.read().decode('utf-8'))
                jsonResponse['httpcode'] = response.getcode()   #Store http status code for each request to keep track response status
                self.internalJson[input['name']] = jsonResponse
            else:
                print('Network request failed. Terminating process.', response.read())
                sys.exit()
        except urllib.error.HTTPError as e:
                print('Network request failed. Terminating process.', e)
                sys.exit()

    def PrintAgent(self, input):
        #Handles print actions
        print(self.buildMacro(input['options']['message']))

    '''
    Any number of additional functions can be added here(EmailAgent, etc.,) and they will automatically processed from the list of agents.
    Reference function below.
    '''
    def EmailAgent(self, input):
        print('Send email based on agent options')
        # Email functionality goes here

    #Utility functions to update the {{ ITEMTOUPDATE }} values in options.url and options.message
    def buildMacro(self, input):
        #Check and handle macros
        pattern = re.compile(r"(\{\{[^}]+}\})")
        inputString = input
        for item in re.findall(pattern, inputString):
            replaceOp = item.replace('{{', '').replace('}}', '')
            referencedItem = replaceOp.strip().split('.')
            finalVal = self.internalJson
            try:
                for i in referencedItem:
                    finalVal = finalVal[i]

                inputString = inputString.replace(item, str(finalVal))
            except KeyError as e:
                print('Could not find relevant item in dictionary', e)
                inputString = inputString.replace(item, '')
        # if no macros are to be replaced return the input
        return inputString
