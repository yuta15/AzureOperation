from pydantic import Field, BaseModel

from annotations.SubnetPrefixAnnotation import Prefix29Annotation


class SubnetModel(BaseModel):
    name: str = Field(min_length=3, max_length=80, pattern='^[a-zA-Z0-9][a-zA-Z0-9\-_\.]*[a-zA-Z0-9\-_]$')
    address_prefix: Prefix29Annotation

    def gen_params(self) -> dict:
        """subnetのパラメータを生成"""
        return {
            'name': self.name,
            'address_prefix': self.address_prefix
        }