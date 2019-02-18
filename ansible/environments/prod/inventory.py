#!/usr/bin/env python

import argparse
import json


class Inventory(object):
    def __init__(self, tfstate_path):
        tfstate = json.load(open(tfstate_path))
        self.json_inventory = {
            "app": {
                "hosts": ["appserver"],
                "vars": {
                    "ansible_host": tfstate['modules'][0]['outputs']['app_external_ip']['value'],
                    "db_host": tfstate['modules'][0]['outputs']['db_internal_ip']['value'],
                    "env": "prod",
                    "nginx_sites": {
                    "default": [
                        "listen 80",
                        "server_name \"reddit\"",
                        "location / { proxy_pass http://127.0.0.1:9292; }"
                    ]
                    }
                }
            },
            "db": {
                "hosts": ["dbserver"],
                "vars": {
                    "ansible_host": tfstate['modules'][0]['outputs']['db_external_ip']['value'],
                    "mongo_bind_ip": "0.0.0.0",
                    "env": "prod"
                }
            }
        }

    def list(self):
        return json.dumps(self.json_inventory)


if __name__ == '__main__':
    inventory = Inventory('../terraform/stage/terraform.tfstate')

    parser = argparse.ArgumentParser(description='Dynamic inventory from terraform.tfstate')
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()

    if args.list:
        print(inventory.list())
