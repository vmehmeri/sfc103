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

def get_service_nodes_uri():
    return "/restconf/config/service-node:service-nodes"

def get_service_nodes_data():
    return {
    "service-nodes": {
        "service-node": [
            {
                "name": "node0",
                "service-function": [
                ],
                "ip-mgmt-address": "192.168.1.10"
            },
            {
                "name": "node1",
                "service-function": [
                ],
                "ip-mgmt-address": "192.168.1.20"
            },
            {
                "name": "node2",
                "service-function": [
                    "dpi-1"
                ],
                "ip-mgmt-address": "192.168.1.30"
            },
            {
                "name": "node3",
                "service-function": [
                    "firewall-1"
                ],
                "ip-mgmt-address": "192.168.1.40"
            },
            {
                "name": "node4",
                "service-function": [
                ],
                "ip-mgmt-address": "192.168.1.50"
            },
            {
                "name": "node5",
                "service-function": [
                ],
                "ip-mgmt-address": "192.168.1.60"
            }
        ]
    }
}

def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"

def get_service_functions_data():
    return {
    "service-functions": {
        "service-function": [
           {
                "name": "dpi-1",
                "ip-mgmt-address": "192.168.1.30",
                "rest-uri": "http://192.168.1.30:5000",
                "type": "dpi",
                "nsh-aware": "true",
                "sf-data-plane-locator": [
                    {
                        "name": "sf1-dpl",
                        "port": 6633,
                        "ip": "192.168.1.30",
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "SFF1"
                    }
                ]
            },
            {
                "name": "firewall-1",
                "ip-mgmt-address": "192.168.1.40",
                "rest-uri": "http://192.168.1.40:5000",
                "type": "firewall",
                "nsh-aware": "true",
                "sf-data-plane-locator": [
                    {
                        "name": "sf2-dpl",
                        "port": 6633,
                        "ip": "192.168.1.40",
                        "transport": "service-locator:vxlan-gpe",
                        "service-function-forwarder": "SFF2"
                    }
                ]
            }
        ]
    }
}

def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"

def get_service_function_forwarders_data():
    return {
    "service-function-forwarders": {
        "service-function-forwarder": [
           {
                "name": "SFF0",
                "service-node": "node0",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "br-sfc",
                },
                "sff-data-plane-locator": [
                    {
                        "name": "sff0-dpl",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.1.10"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ],
            },
            {
                "name": "SFF1",
                "service-node": "node1",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "br-sfc",
                },
                "sff-data-plane-locator": [
                    {
                        "name": "sff1-dpl",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.1.20"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ],
                "service-function-dictionary": [
                    {
                        "name": "dpi-1",
                        "sff-sf-data-plane-locator": {
                             "sf-dpl-name": "sf1-dpl",
                             "sff-dpl-name": "sff1-dpl"
                        }
                    }
                ],
            },
            {
                "name": "SFF2",
                "service-node": "node4",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "br-sfc",
                },
                "sff-data-plane-locator": [
                    {
                        "name": "sff2-dpl",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.1.50"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ],
                "service-function-dictionary": [
                    {
                        "name": "firewall-1",
                        "sff-sf-data-plane-locator": {
                            "sf-dpl-name": "sf2-dpl",
                            "sff-dpl-name": "sff2-dpl"
                        }
                    }
                ]
            },
            {
                "name": "SFF3",
                "service-node": "node5",
                "service-function-forwarder-ovs:ovs-bridge": {
                    "bridge-name": "br-sfc",
                },
                "sff-data-plane-locator": [
                    {
                        "name": "sff3-dpl",
                        "data-plane-locator": {
                            "transport": "service-locator:vxlan-gpe",
                            "port": 6633,
                            "ip": "192.168.1.60"
                        },
                        "service-function-forwarder-ovs:ovs-options": {
                            "remote-ip": "flow",
                            "dst-port": "6633",
                            "key": "flow",
                            "nsp": "flow",
                            "nsi": "flow",
                            "nshc1": "flow",
                            "nshc2": "flow",
                            "nshc3": "flow",
                            "nshc4": "flow"
                        }
                    }
                ],
            }
        ]
    }
}

def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"

def get_service_function_chains_data():
    return {
    "service-function-chains": {
        "service-function-chain": [
            {
                "name": "SFC1",
                "symmetric": "true",
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
			
			{
                "name": "SFC2",
                "symmetric": "true",
                "sfc-service-function": [
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
                "name": "SFP1",
                "service-chain-name": "SFC1",
                "starting-index": 255,
                "symmetric": "true",
                 "context-metadata": "NSH1"
            }
			{
                "name": "SFP2",
                "service-chain-name": "SFC2",
                "starting-index": 255,
                "symmetric": "true",
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
        "name": "SFP1",
        "service-chain-name": "SFC1",
        "classifier": "Classifier1",
        "symmetric-classifier": "Classifier2",
        "context-metadata": "NSH1",
        "symmetric": "true"
      }
	  {
        "name": "SFP2",
        "service-chain-name": "SFC2",
        "classifier": "Classifier1",
        "symmetric-classifier": "Classifier2",
        "context-metadata": "NSH1",
        "symmetric": "true"
      }
    ]
  }
}

def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"

def get_rendered_service_path_data(rsp):
    return {
    "input": {
        "name": rsp,
        "parent-service-function-path": "SFP1",
        "symmetric": "true"
    }
}

def get_service_function_acl_uri():
    return "/restconf/config/ietf-access-control-list:access-lists/"

def get_service_function_acl_data(rsp):
    return  {
  "access-lists": {
    "acl": [
      {
        "acl-name": "ACL1",
        "access-list-entries": {
          "ace": [
            {
              "rule-name": "ACE1",
              "actions": {
                "service-function-acl:rendered-service-path": rsp
              },
              "matches": {
                "destination-ipv4-network": "192.168.2.0/24",
                "source-ipv4-network": "192.168.2.0/24",
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
        "acl-name": "ACL2",
        "access-list-entries": {
          "ace": [
            {
              "rule-name": "ACE2",
              "actions": {
                "service-function-acl:rendered-service-path": "%s-Reverse" % rsp
              },
              "matches": {
                "destination-ipv4-network": "192.168.2.0/24",
                "source-ipv4-network": "192.168.2.0/24",
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
        "name": "Classifier1",
        "scl-service-function-forwarder": [
          {
            "name": "SFF0",
            "interface": "veth-br"
          }
        ],
        "access-list": "ACL1"
      },
      {
        "name": "Classifier2",
        "scl-service-function-forwarder": [
          {
            "name": "SFF3",
            "interface": "veth-br"
          }
        ],
        "access-list": "ACL2"
      }
    ]
  }
}

if __name__ == "__main__":

    print "sending service nodes"
    put(controller, DEFAULT_PORT, get_service_nodes_uri(), get_service_nodes_data(), True)
    print "sending service functions"
    put(controller, DEFAULT_PORT, get_service_functions_uri(), get_service_functions_data(), True)
    print "sending service function forwarders"
    put(controller, DEFAULT_PORT, get_service_function_forwarders_uri(), get_service_function_forwarders_data(), True)
    print "sending service function chains"
    put(controller, DEFAULT_PORT, get_service_function_chains_uri(), get_service_function_chains_data(), True)
    print "sending service function metadata"
    put(controller, DEFAULT_PORT, get_service_function_metadata_uri(), get_service_function_metadata_data(), True)
    print "sending service function paths"
    put(controller, DEFAULT_PORT, get_service_function_paths_uri(), get_service_function_paths_data(), True)
    print "sending service function acl"
    put(controller, DEFAULT_PORT, get_service_function_acl_uri(), get_service_function_acl_data("RSP2"), True)
    print "sending rendered service path"
    post(controller, DEFAULT_PORT, get_rendered_service_path_uri(), get_rendered_service_path_data("RSP2"), True)
    print "sending service function classifiers"
    put(controller, DEFAULT_PORT, get_service_function_classifiers_uri(), get_service_function_classifiers_data(), True)
