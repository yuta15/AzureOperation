from pydantic import Field, BaseModel

from annotations.IPv4NetworkAnnotation import IPv4NetworkAnnotation

class SubnetModel(BaseModel):
    name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9\-_\.]*[a-zA-Z0-9\-_]$')
    address_prefix: IPv4NetworkAnnotation

    def gen_params(self) -> dict:
        """subnetのパラメータを生成"""
        return {
            'name': self.name,
            'address_prefix': self.address_prefix
        }