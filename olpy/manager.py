#!/usr/bin/env python
#coding: utf-8
"""
This module simply sends request to the Online Labs API,
and returns their response as a dict.
"""

import requests
from json import dumps

API_COMPUTE = 'https://api.cloud.online.net'
API_ACCOUNT = "https://account.cloud.online.net"


class OlError(RuntimeError):
        pass


class OlManager(object):
    def __init__(self, token=None, debug=None):
        self.oltoken = token
        self.apic = API_COMPUTE
        self.apia = API_ACCOUNT
        self.debug = debug

    def organizations(self):
        json = self.request(self.apia+'/organizations')
        return json['organizations']

    def set_token(self, token):
        self.oltoken = token

    def new_token(self, email, password, expires=True):
        data = {
            'email': email,
            'password': password,
            'expires': expires,
        }

        json = self.request(self.apia+'/tokens', data=data, method='POST')
        return json['token']

    def user(self, user_id):
        json = self.request(self.apia+'/users/%s' % user_id)
        return json['user']

    def tokens(self):
        json = self.request(self.apia+'/tokens')
        return json['tokens']

    def token(self, token_id):
        json = self.request(self.apia+'/token/%s' % token_id)
        return json['token']

    def extend_token(self, token_id):
        json = self.request(self.apia+'/token/%s' % token_id, method='PATCH')

        return json['server']

    def delete_token(self, token_id):
        self.request(self.apia+'/token/%s' % token_id, method='DELETE')

    def servers(self):
        json = self.request(self.apic+'/servers')
        return json['servers']

    def server(self, server_id):
        json = self.request(self.apic+'/servers/%s' % server_id)
        return json['server']

    def new_server(self, name, organization_id, image_id, volumes, tags=[]):
        data = {
            'name': name,
            'organization': organization_id,
            'image': image_id,
            'volumes': volumes,
            'tags': tags,
        }

        json = self.request(self.apic+'/servers', data=data, method='POST')
        return json['server']

    def update_server(self, server):
        json = self.request(self.apic+'/servers/%s' % server['id'], data=server, method='PUT')
        return json['server']

    def delete_server(self, server_id):
        json = self.request(self.apic+'/servers/%s' % server_id, method='DELETE')
        return json['server']

    def server_actions(self, server_id):
        json = self.request(self.apic+'/servers/%s/action' % server_id)
        return json['actions']

    def server_action(self, server_id, action):
        data = {
            'action': action,
        }

        json = self.request(self.apic+'/servers/%s/action' % server_id, data=data, method='POST')
        return json['task']

    def volumes(self):
        json = self.request(self.apic+'/volumes')
        return json['volumes']

    def new_volume(self, name, size, organization_id, volume_type):
        if volume_type not in ["l_ssd", "l_hdd"]:
            raise OlError("Volume type should be l_ssd or l_hdd")

        data = {
            "name": name,
            "size": size,
            "organization": organization_id,
            "volume_type": volume_type,
        }

        json = self.request(self.apic+'/volumes', data=data, method='POST')
        return json['volume']

    def volume(self, volume_id):
        json = self.request(self.apic+'/volumes/%s' % volume_id)
        return json['volume']

    def delete_volume(self, volume_id):
        self.request(self.apic+'/volumes/%s' % volume_id, method='DELETE')

    def new_snapshot(self, name, organization_id, volume_id):
        data = {
            'name': name,
            'organization': organization_id,
            'volume': volume_id,
        }

        json = self.request(self.apic+'/snapshots', data=data, method='POST')
        return json['snapshot']

    def update_snapshot(self, snapshot):
        json = self.request(self.apic+'/snapshot/%s' % snapshot['id'], data=snapshot, method='PUT')
        return json['snapshot']

    def snapshots(self):
        json = self.request(self.apic+'/snapshots')
        return json['snapshots']

    def snapshot(self, snapshot_id):
        json = self.request(self.apic+'/snapshots/%s' % snapshot_id)
        return json['snapshot']

    def delete_snapshot(self, snapshot_id):
        self.request(self.apic+'/snapshots/%s' % snapshot_id, method='DELETE')

    def image(self, image_id):
        json = self.request(self.apic+'/images/%s' % image_id)
        return json['image']

    def images(self):
        json = self.request(self.apic+'/images')
        return json['images']

    def new_image(self, name, organization_id, arch, volume_id):
        data = ~{
            'name': name,
            'organization': organization_id,
            'arch': arch,
            'root_volume': volume_id,
        }

        json = self.request(self.apic+'/images', data=data, method='POST')
        return json['image']

    def update_image(self, image):
        json = self.request(self.apic+'/images/%s' % image['id'], data=image, method='PUT')
        return json['image']

    def delete_image(self, image_id):
        self.request(self.apic+'/images/%s' % image_id, method='DELETE')

    def new_ips(self, organization_id):
        data = ~{
            'organization': organization_id,
        }

        json = self.request(self.apic+'/ips', data=data, method='POST')
        return json['ip']

    def ips(self):
        json = self.request(self.apic+'/ips')
        return json['ips']

    def ip(self, ip_id):
        json = self.request(self.apic+'/ips/%s' % ip_id)
        return json['ip']

    def remap_ip(self, ip_id, address, server_id, organization_id, ):
        data = {
            'address': address,
            'id': ip_id,
            'organization': organization_id,
            'server': server_id,
        }

        json = self.request(self.apic+'/ips/%s' % ip_id, data=data, method='POST')
        return json['ip']

    def delete_ips(self, ip_id):
        self.request(self.apic+'/ips/%s' % ip_id)

    def request(self, url, data={}, method='GET'):

        headers = {"content-type": "application/json"}
        if self.token is not None:
            headers["X-Auth-Token"] = self.oltoken

        if self.debug:
            print("Headers : %s" % headers)
            print("Url: %s" % url)
            print("Method: %s" % method)
            print("Data: %s\n" % dumps(data))

        try:
            if method == 'POST':
                resp = requests.post(url, data=dumps(data), headers=headers, timeout=60)
                json = resp.json()
            elif method == 'DELETE':
                resp = requests.delete(url, headers=headers, timeout=60)
                json = {'status': resp.status_code}
            elif method == 'PUT':
                resp = requests.put(url, headers=headers, data=dumps(data), timeout=60)
                json = resp.json()
            elif method == 'GET':
                resp = requests.get(url, headers=headers, data=dumps(data), timeout=60)
                json = resp.json()
            elif method == 'PATCH':
                resp = requests.patch(url, headers=headers, data=dumps(data), timeout=60)
                json = resp.json()
            else:
                raise OlError('Unsupported method %s' % method)

        except ValueError:  # requests.models.json.JSONDecodeError
            raise ValueError("The API server doesn't respond with a valid json")
        except requests.RequestException as e:  # errors from requests
            raise RuntimeError(e)

        if resp.status_code != requests.codes.ok:
            if json:
                if 'error_message' in json:
                    raise OlError(json['error_message'])
                elif 'message' in json:
                    raise OlError(json['message'])
            # The JSON reponse is bad, so raise an exception with the HTTP status
            resp.raise_for_status()

        if json.get('id') == 'not_found':
            raise OlError(json['message'])

        return json

if __name__ == '__main__':
    import os
    import sys
    api_debug = os.environ.get('OL_API_DEBUG')
    api_token = os.environ.get('OL_API_TOKEN')
    api_id = os.environ.get('OL_API_ID')
    api_pass = os.environ.get('OL_API_PASSWD')
    if api_token is not None:
        ol = OlManager(api_token, api_debug)
    elif api_id is not None and api_pass is not None:
        ol = OlManager(debug=api_debug)
        ol.set_token(ol.new_token(api_id, api_pass)['id'])
    else:
        sys.exit("Error: OL_API_TOKEN or OL_API_ID, OL_API_PASSWD enviroment variables are not set")
    fname = sys.argv[1]
    import pprint
    pprint.pprint(getattr(ol, fname)(*sys.argv[2:]))
