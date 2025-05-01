import asyncio
import aiofiles
import json
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network.aio import NetworkManagementClient

from settings.settings import Setting
from models.resource.ResourceGroupModel import ResourceGroupModel
from models.network.VirtualNetworkModel import VirtualNetworkModel

credential = Setting(ENV='DEV', _env_file='.dev.env').gen_credentail()


async def create_vnet(vnet_params, sub_id):
    async with NetworkManagementClient(credential=credential, subscription_id=sub_id) as network_client:
        nw_poller = await network_client.virtual_networks.begin_create_or_update(**vnet_params)
    return await nw_poller.result()

async def create_resources():
    async with aiofiles.open('sample/parameters.json', mode='r') as f:
        content = await f.read()

    params = json.loads(content)
    rg_params = ResourceGroupModel(**params['resource_group'][0]).gen_params()
    vnet_params = VirtualNetworkModel(**params['virtual_network'][0]).gen_params()
    sub_id = '6fc8922b-32f6-4ca5-8839-f7a018f3614c'
    rg_client = ResourceManagementClient(credential=credential, subscription_id=sub_id)
    rg_result = rg_client.resource_groups.create_or_update(**rg_params)
    nw_result = await create_vnet(vnet_params=vnet_params, sub_id=sub_id)
    return rg_result, nw_result


a = asyncio.run(create_resources())
print(a)