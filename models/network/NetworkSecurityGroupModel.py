from typing import List
from pydantic import Field

from models.resource.ResourceGroupModel import ResourceGroupModel
from models.network.NetworkSecurityGroupRuleModel import NetworkSecurityGroupRuleModel


class NetworkSecurityGroupModel(ResourceGroupModel):
    """NSG用モデル"""
    network_security_group_name: str = Field(min_length=2, max_length=64,pattern='^[a-zA-Z0-9][a-zA-Z0-9_.-]*[a-zA-Z0-9_]$')
    security_rules: List[NetworkSecurityGroupRuleModel] | None = None
    
    def gen_params(self) -> dict:
        return {
            'resource_group_name': self.resource_group_name,
            'network_security_group_name': self.network_security_group_name,
            'parameters': {
                'location': self.location,
                'tags': self.tags,
                'security_rules': [rule.model_dump() for rule in self.security_rules]
            }
        }
