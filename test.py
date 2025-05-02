from settings.settings import Setting
from azure.mgmt.network import NetworkManagementClient

from models.network.NetworkSecurityGroupModel import NetworkSecurityGroupModel

credential = Setting(ENV='DEV', _env_file='.dev.env').gen_credentail()
sub_id = '6fc8922b-32f6-4ca5-8839-f7a018f3614c'


nsg_val = {
    "resource_group_name": "test-rg",
    "location": "japaneast",
    "tags": {
        "country": 'japna'
        },
    "network_security_group_name": "nsg1",
    "security_rules": [
        {
            "name": "rule1",
            "priority": "100",
            "direction": "Inbound",
            "protocol": "Tcp",
            "access": "Allow",
            "description": "",
            "source_address_prefix": "",
            "source_address_prefixes": ["192.168.1.1", "192.168.1.2"],
            "destination_address_prefix": "",
            "destination_address_prefixes": ["10.0.0.1", "10.0.0.2"],
            "source_port_range": "*",
            "source_port_ranges": [],
            "destination_port_range": "80-443",
            "destination_port_ranges": []
        }
    ]
}

a = NetworkSecurityGroupModel(**nsg_val).gen_params()
print(a)


client = NetworkManagementClient(credential=credential, subscription_id=sub_id)
result = client.network_security_groups.begin_create_or_update(**a).result()
print(result)