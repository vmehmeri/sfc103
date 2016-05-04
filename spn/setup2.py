#!/usr/bin/python
import argparse
import requests,json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os

controller='192.168.1.5'
DEFAULT_PORT='8181'


USERNAME='admin'
PASSWORD='admin'

def get(host, port, uri):
    url='http://'+host+":"+port+uri
    r = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    jsondata=json.loads(r.text)
    return jsondata

def put(host, port, uri, data, debug=False):
    '''Perform a PUT rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "PUT %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)

def post(host, port, uri, data, debug=False):
    '''Perform a POST rest operation, using the URL and data provided'''

    url='http://'+host+":"+port+uri
    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "POST %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)



def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    return {
    "service-function-chains": {
        "service-function-chain": [
            {
                "name": "SFC1_2",
                "symmetric": "false",
                "sfc-service-function": [
                    {
                        "name": "dpi-abstract1",
                        "type": "dpi"
                    },
                    {
                        "name": "firewall-abstract1",
                        "type": "firewall"
                    }
                ]
            },
			{
                "name": "SFC1_2-Reverse",
                "symmetric": "false",
                "sfc-service-function": [
                    {
                        "name": "dpi-abstract1",
                        "type": "dpi"
                    },
                    {
                        "name": "firewall-abstract1",
                        "type": "firewall"
                    }
                ]
            }
        ]
    }
}

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    return {
    "service-function-paths": {
        "service-function-path": [
            {
                "name": "SFP1_2",
                "service-chain-name": "SFC1_2",
                "starting-index": 255,
                "symmetric": "false",
                 "context-metadata": "NSH1"
            },
			{
                "name": "SFP1_2-Reverse",
                "service-chain-name": "SFC1_2-Reverse",
                "starting-index": 255,
                "symmetric": "false",
                 "context-metadata": "NSH1"
            }
        ]
    }
}

def get_service_function_metadata_uri():
    return "/restconf/config/service-function-path-metadata:service-function-metadata/"

def get_service_function_metadata_data():
    return {
  "service-function-metadata": {
    "context-metadata": [
      {
        "name": "NSH1",
        "context-header1": "1",
        "context-header2": "2",
        "context-header3": "3",
        "context-header4": "4"
      }
    ]
  }
}

def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"

def get_service_function_paths_data():
    return {
  "service-function-paths": {
    "service-function-path": [
      {
        "name": "SFP1_2",
        "service-chain-name": "SFC1_2",
        "classifier": "Classifier1_2",
        "context-metadata": "NSH1",
        "symmetric": "false"
      },
	  {
        "name": "SFP1_2-Reverse",
        "service-chain-name": "SFC1_2-Reverse",
        "classifier": "Classifier2_2",
        "context-metadata": "NSH1",
        "symmetric": "false"
      }
    ]
  }
}

def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"

def get_rendered_service_path_data():
    return {
    "input": {
        "name": "RSP1_2",
        "parent-service-function-path": "SFP1_2",
        "symmetric": "false"
    }
}

def get_reverse_rendered_service_path_data():
    return {
    "input": {
        "name": "RSP1_2-Reverse",
        "parent-service-function-path": "SFP1_2-Reverse",
        "symmetric": "false"
    }
}

def get_service_function_acl_uri():
    return "/restconf/config/ietf-access-control-list:access-lists/"

def get_service_function_acl_data():
    return  {
  "access-lists": {
    "acl": [
      {
        "acl-name": "ACL1_2",
        "access-list-entries": {
          "ace": [
            {
              "rule-name": "ACE1_2",
              "actions": {
                "service-function-acl:rendered-service-path": "RSP1_2"
              },
              "matches": {
                "destination-ipv4-network": "192.168.3.0/24",
                "source-ipv4-network": "192.168.3.0/24",
                "protocol": "6",
                "source-port-range": {
                    "lower-port": 0
                },
                "destination-port-range": {
                    "lower-port": 80
                }
              }
            }
          ]
        }
      },
      {
        "acl-name": "ACL2_2",
        "access-list-entries": {
          "ace": [
            {
              "rule-name": "ACE2_2",
              "actions": {
                "service-function-acl:rendered-service-path": "RSP1_2-Reverse"
              },
              "matches": {
                "destination-ipv4-network": "192.168.3.0/24",
                "source-ipv4-network": "192.168.3.0/24",
                "protocol": "6",
                "source-port-range": {
                    "lower-port": 80
                },
                "destination-port-range": {
                    "lower-port": 0
                }
              }
            }
          ]
        }
      }
    ]
  }
}

def get_service_function_classifiers_uri():
    return "/restconf/config/service-function-classifier:service-function-classifiers/"

def get_service_function_classifiers_data():
    return  {
  "service-function-classifiers": {
    "service-function-classifier": [
      {
        "name": "Classifier1_2",
        "scl-service-function-forwarder": [
          {
            "name": "SFF0",
            "interface": "veth2-br"
          }
        ],
        "access-list": "ACL1_2"
      },
      {
        "name": "Classifier2_2",
        "scl-service-function-forwarder": [
          {
            "name": "SFF3",
            "interface": "veth2-br"
          }
        ],
        "access-list": "ACL2_2"
      },
    ]
  }
}

if __name__ == "__main__":

    print "sending service function chains"
    put(controller, DEFAULT_PORT, get_service_function_chains_uri(), get_service_function_chains_data(), True)
    print "sending service function metadata"
    put(controller, DEFAULT_PORT, get_service_function_metadata_uri(), get_service_function_metadata_data(), True)
    print "sending service function paths"
    put(controller, DEFAULT_PORT, get_service_function_paths_uri(), get_service_function_paths_data(), True)
    print "sending service function acl"
    put(controller, DEFAULT_PORT, get_service_function_acl_uri(), get_service_function_acl_data(), True)
    print "sending rendered service path"
    post(controller, DEFAULT_PORT, get_rendered_service_path_uri(), get_rendered_service_path_data(), True)
    post(controller, DEFAULT_PORT, get_rendered_service_path_uri(), get_reverse_rendered_service_path_data(), True)
    print "sending service function classifiers"
    put(controller, DEFAULT_PORT, get_service_function_classifiers_uri(), get_service_function_classifiers_data(), True)
