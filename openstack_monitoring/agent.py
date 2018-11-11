#!/usr/bin/python3.5
import time

import aiohttp
import asyncio
import requests
from pyzabbix import ZabbixMetric, ZabbixSender

from openstack_monitoring import utils
from openstack_monitoring.utils import CreateToken


async def send_metric(zserver, port, packet_item):
    """
    send metric to zserver
    :param packet_item: list
    :return: dict
    """
    result = ZabbixSender(zserver, port).send(packet_item)
    return result


async def collect_item_volumes(
        data,
        config_dict,
        zserver=None,
        hostId=None,
        port=None,
        key_volumes_total=None,
        key_volumes_available=None,
        key_volumes_in_use=None,
        key_volumes_error=None
):
    zserver = zserver or config_dict['zabbix-zserver']
    hostId = hostId or config_dict['zabbix-hostid']
    port = port or config_dict['zabbix-port']
    key_volumes_total = key_volumes_total or config_dict[
        'key-volumes_total'
    ]
    key_volumes_available = key_volumes_available or config_dict[
        'key-volumes_available'
    ]
    key_volumes_other = key_volumes_other or config_dict['key-volumes_other']
    key_volumes_in_use = key_volumes_in_use or config_dict['key-volumes_in_use']
    key_volumes_error = key_volumes_error or config_dict['key-volumes_error']
    total_volumes_available = 0
    total_volumes_other = 0
    total_volumes_in_use = 0
    total_volumes_error = 0
    total_volumes = str(len(data['volumes']))
    for volume in data['volumes']:
        if volume['status'] == 'available':
            total_volumes_available += 1
        elif volume['status'] == 'in-use':
            total_volumes_in_use += 1
        elif volume['status'] == 'error':
            total_volumes_error += 1
        else:
            total_volumes_other += 1
    packet_volumes = [ZabbixMetric(hostId,
                                   key_volumes_total,
                                   total_volumes),
                      ZabbixMetric(hostId,
                                   key_volumes_available,
                                   total_volumes_available),
                      ZabbixMetric(hostId,
                                   key_volumes_in_use,
                                   total_volumes_in_use),
                      ZabbixMetric(hostId,
                                   key_volumes_error,
                                   total_volumes_error)]
    result = await send_metric(zserver=zserver,
                               port=int(port),
                               packet_item=packet_volumes)
    return result


async def collect_item_vms(
        data,
        config_dict,
        zserver=None,
        hostId=None,
        port=None,
        key_vms_total=None,
        key_vms_running=None,
        key_vms_stop=None
):
    zserver = zserver or config_dict['zabbix-zserver']
    hostId = hostId or config_dict['zabbix-hostid']
    port = port or config_dict['zabbix-port']
    key_vms_total = key_vms_total or config_dict['key-vms_total']
    key_vms_running = key_vms_running or config_dict['key-vms_running']
    key_vms_stop = key_vms_stop or config_dict['key-vms_stop']
    total_vms = str(len(data['servers']))
    total_vms_running = 0
    total_vms_stop = 0
    for vm in data['servers']:
        if vm['status'] == 'ACTIVE':
            total_vms_running += 1
        else:
            total_vms_stop += 1
    packet_vms = [ZabbixMetric(hostId, key_vms_total, total_vms),
                  ZabbixMetric(hostId, key_vms_running, total_vms_running),
                  ZabbixMetric(hostId, key_vms_stop, total_vms_stop)]
    result = await send_metric(zserver=zserver,
                               port=int(port),
                               packet_item=packet_vms)
    return result


async def collect_item_projects(
        data,
        config_dict,
        zserver=None,
        hostId=None,
        port=None,
        key_projects_total=None
):
    zserver = zserver or config_dict['zabbix-zserver']
    hostId = hostId or config_dict['zabbix-hostid']
    port = port or config_dict['zabbix-port']
    key_projects_total = key_projects_total or config_dict['key-projects_total']
    total_projects = str(len(data['projects']))
    packet_projects = [ZabbixMetric(hostId, key_projects_total, total_projects)]
    result = await send_metric(zserver=zserver,
                               port=int(port),
                               packet_item=packet_projects)
    return result


async def collect_item_users(
        data,
        config_dict,
        zserver=None,
        hostId=None,
        port=None,
        key_users_total=None
):
    key_users_total = key_users_total or config_dict['key-users_total']
    zserver = zserver or config_dict['zabbix-zserver']
    hostId = hostId or config_dict['zabbix-hostid']
    port = port or config_dict['zabbix-port']
    total_users = str(len(data['users']))
    packet_users = [ZabbixMetric(hostId, key_users_total, total_users)]
    result = await send_metric(zserver=zserver,
                               port=int(port),
                               packet_item=packet_users)
    return result

async def collect_item_ips(
        data,
        config_dict,
        id_token,
        zserver=None,
        hostId=None,
        port=None,
        network_name=None,
        key_ips_total=None,
        key_ips_used=None,
        key_ips_availabity=None
):
    zserver = zserver or config_dict['zabbix-zserver']
    hostId = hostId or config_dict['zabbix-hostid']
    port = port or config_dict['zabbix-port']
    network_name = network_name or config_dict['key-network_name']
    key_ips_total = key_ips_total or config_dict['key-ips_total']
    key_ips_used = key_ips_used or config_dict['key-ips_used']
    key_ips_availabity = key_ips_availabity or config_dict['key-ips_availabity']
    for network in data['networks']:
        if network['name'] == network_name:
            id_network = network['id']
            url_api_detail_network = config_dict[
                'openstack_api-detail_ips_of_network'
            ] + id_network
            detail_network = requests.get(
                url=url_api_detail_network,
                headers={"X-Auth-Token": id_token}
            ).json()['network_ip_availability']
            total_ips = detail_network['total_ips']
            total_ips_used = detail_network['used_ips']
            total_ips_availabity = total_ips - total_ips_used
            packet_ips = [ZabbixMetric(hostId,
                                       key_ips_total,
                                       total_ips),
                          ZabbixMetric(hostId,
                                       key_ips_used,
                                       total_ips_used),
                          ZabbixMetric(hostId,
                                       key_ips_availabity,
                                       total_ips_availabity)]
            result = await send_metric(zserver=zserver,
                                       port=int(port),
                                       packet_item=packet_ips)
            return result


async def get_vms(url, id_token, config_dict):
    while True:
        print('collect vms at {}'.format(time.strftime('%d/%m/%Y %H:%M:%S')))
        async with aiohttp.ClientSession(
            headers={"X-Auth-Token": id_token}
        ) as session:
            async with session.get(url) as r:
                json_body = await r.json()
                result = await collect_item_vms(data=json_body,
                                                config_dict=config_dict)
                # print(result)
                print('collect vms finish at {}'.format(
                    time.strftime('%d/%m/%Y %H:%M:%S')))
        await asyncio.sleep(30)


async def get_volumes(url, id_token, config_dict):
    while True:
        print('collect volumes at {}'.format(
            time.strftime('%d/%m/%Y %H:%M:%S'))
        )
        async with aiohttp.ClientSession(
            headers={"X-Auth-Token": id_token}
        ) as session:
            async with session.get(url) as r:
                json_body = await r.json()
                result = await collect_item_volumes(data=json_body,
                                                    config_dict=config_dict)
                # print(result)
                print('collect volumes finish at {}'.format(
                    time.strftime('%d/%m/%Y %H:%M:%S')))
                await asyncio.sleep(30)


async def get_projects(url, id_token, config_dict):
    while True:
        print('collect projects at {}'.format(
            time.strftime('%d/%m/%Y %H:%M:%S'))
        )
        async with aiohttp.ClientSession(
            headers={"X-Auth-Token": id_token}
        ) as session:
            async with session.get(url) as r:
                json_body = await r.json()
                result = await collect_item_projects(data=json_body,
                                                     config_dict=config_dict)
                # print(result)
                print('collect projects finish at {}'.format(
                    time.strftime('%d/%m/%Y %H:%M:%S')))
                await asyncio.sleep(30)


async def get_users(url, id_token, config_dict):
    while True:
        print('collect users at {}'.format(time.strftime('%d/%m/%Y %H:%M:%S')))
        async with aiohttp.ClientSession(
            headers={"X-Auth-Token": id_token}
        ) as session:
            async with session.get(url) as r:
                json_body = await r.json()
                result = await collect_item_users(data=json_body,
                                                  config_dict=config_dict)
                # print(result)
                print('collect users finish at {}'.format(
                    time.strftime('%d/%m/%Y %H:%M:%S')))
                await asyncio.sleep(30)


async def get_ips(url, id_token, config_dict):
    while True:
        print('collect ips at {}'.format(time.strftime('%d/%m/%Y %H:%M:%S')))
        async with aiohttp.ClientSession(
            headers={"X-Auth-Token": id_token}
        ) as session:
            async with session.get(url) as r:
                json_body = await r.json()
                result = await collect_item_ips(data=json_body,
                                                config_dict=config_dict,
                                                id_token=id_token)
                # print(result)
                print('collect ips finish at {}'.format(
                    time.strftime('%d/%m/%Y %H:%M:%S')))
                await asyncio.sleep(30)


class Agent(object):

    def __init__(self):
        self.token = CreateToken()
        self.id_token = self.token.get_token()
        self.config_dict = utils.ini_file_loader()

    def collect_and_send_metric(self):
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(
                get_vms(
                    url=self.config_dict['openstack_api-list_vms'],
                    id_token=self.id_token,
                    config_dict=self.config_dict
                )
            ),
            asyncio.ensure_future(
                get_volumes(
                    url=self.config_dict['openstack_api-list_volumes'],
                    id_token=self.id_token,
                    config_dict=self.config_dict
                )
            ),
            asyncio.ensure_future(
                get_projects(
                    url=self.config_dict['openstack_api-list_projects'],
                    id_token=self.id_token,
                    config_dict=self.config_dict
                )
            ),
            asyncio.ensure_future(
                get_users(
                    url=self.config_dict['openstack_api-list_users'],
                    id_token=self.id_token,
                    config_dict=self.config_dict
                )
            ),
            asyncio.ensure_future(
                get_ips(
                    url=self.config_dict['openstack_api-list_networks'],
                    id_token=self.id_token,
                    config_dict=self.config_dict
                )
            )
        ]
        loop.run_until_complete(asyncio.wait(tasks))
