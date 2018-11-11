#!/usr/bin/python3.5

import configparser
import requests
import json


def ini_file_loader():
    """ Load configuration from ini file"""

    parser = configparser.SafeConfigParser()
    parser.read('/etc/openstack_monitoring/config.cfg')
    config_dict = {}
    for section in parser.sections():
        for key, value in parser.items(section, True):
            config_dict['%s-%s' % (section, key)] = value
    return config_dict


class CreateToken(object):

    def __init__(self):
        self.config_dict = ini_file_loader()
        self.data = {'auth':
                         {'identity':
                              {'methods': ['password'],
                               'password':
                                   {'user':
                                        {'domain':
                                             {'id':
                                                  self.config_dict[
                                                      'controller-'
                                                      'user_domain_name'
                                                  ]},
                                         'name': self.config_dict['controller-'
                                                                  'username'],
                                         'password':
                                             self.config_dict[
                                                 'controller-password'
                                             ]}}},
                          "scope": {
                              "project": {
                                  "name": "admin",
                                  "domain": {
                                      "name":
                                          self.config_dict[
                                              'controller-project_domain_name'
                                          ]
                                  }
                              }
                          }
                          }
                     }
        self.url = self.config_dict['openstack_api-auth_token']

    def get_token(self):
        result = requests.post(url=self.url,
                               data=json.dumps(self.data))
        token_id = result.headers['X-Subject-Token']
        return token_id
