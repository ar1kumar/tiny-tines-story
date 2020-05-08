import sys
import json
import argparse
from tines_pipeline.agent_handler import Pipeline

#Parse argument from command line
parser = argparse.ArgumentParser(description='Process tiny tines json')
parser.add_argument('inputJsonFile', help='Mention the tiny-tines json file location')
args = parser.parse_args()

try:
    with open(args.inputJsonFile) as json_file:
        agentObject = json.load(json_file)
        pipeline = Pipeline(agentObject['agents'])
        pipeline.start()
except FileNotFoundError as e:
    print('Could not locate tiny-tines json file. Terminating.', e)
    sys.exit()
