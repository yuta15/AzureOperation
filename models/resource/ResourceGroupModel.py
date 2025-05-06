from pydantic import Field

from models.common.ResourceBaseModel import ResourceBaseModel


class ResourceGroupModel(ResourceBaseModel):
    """
    ResourceGroupのバリデーション用クラス
    ResourceBaseModelを継承しているため、location, tagsの値が必要となる
    Attributes:
        location: str | None = None
        tags: dict | None = None
        resource_group_name: str | None = None
    """
    resource_group_name: str = Field(
        max_length=64, 
        min_length=3, 
        pattern='^[0-9a-zA-Z][0-9a-zA-Z\-_]*$', 
        )


    def gen_params(self)->dict:
        """resource group作成用のモデルを生成する関数"""
        return {
            "resource_group_name": self.resource_group_name,
            "parameters": {
                "location": self.location,
                "tags": self.tags
            }
        }