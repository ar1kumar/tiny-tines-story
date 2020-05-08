import pytest
from tines_pipeline import agent_handler

class TestClass():
    def setup_class(self):
        self.test_agent_json = {
          "agents": [
            {
              "type": "HTTPRequestAgent",
              "name": "datetime",
              "options": {
                "url": "http://worldtimeapi.org/api/ip"
              }
            },
            {
              "type": "PrintAgent",
              "name": "print_time",
              "options": {
                "message": "Current time:\n\t{{ datetime.datetime }}"
              }
            },
            {
              "type": "HTTPRequestAgent",
              "name": "fact",
              "options": {
                "url": "http://numbersapi.com/{{ datetime.day_of_year }}/date?json"
              }
            },
            {
              "type": "PrintAgent",
              "name": "print_fact",
              "options": {
                "message": "Fact for today:\n\t{{ fact.text }}"
              }
            }
          ]
        }

        # Setup the main pipeline class from agentHandler
        self.test_pipeline = agent_handler.Pipeline(self.test_agent_json)

    # def teardown_class(self):
    #     '''teardown_class called once for the class'''

    def test_direct_http(self):
        test_agent = self.test_agent_json['agents'][0]
        self.test_http_req = self.test_pipeline.HTTPRequestAgent(test_agent)
        assert self.test_pipeline.internalJson[test_agent['name']]['httpcode'] == 200

    def test_dynamic_http(self):
        # Tests the http request for dynamic links with {{itemtoupdate}}
        # This test is based on the previous agent's output.
        # in this case agent[0] outputs the datetime value and agent[2] uses the datetime value to make
        # another test request and assert the response code
        test_agent = self.test_agent_json['agents'][2]
        self.test_http_req = self.test_pipeline.HTTPRequestAgent(test_agent)
        assert self.test_pipeline.internalJson[test_agent['name']]['httpcode'] == 200
