import os
import json
from pydantic import BaseModel, field_validator


class ResourceBaseModel(BaseModel):
    location: str | None = None
    tags: dict | None = None
    
    @field_validator('location', mode='before')
    @classmethod
    def _validate_location(cls, location) -> str:
        """
        regions.jsonを元を参照し、指定された値がリージョンに含まれているか判定する。
        また整形も行う。
        example)
            japan east -> japaneast
            japan-east -> japaneast
            japan_east -> japaneast
            JPANAEAST -> japaneast
        raises: 
            ValueError()
        return:
            formattd_location: str
        """
        path = f'{os.path.dirname(__file__)}/{os.path.pardir}/{os.path.pardir}/regions.json'
        # lower caseへ統一
        formattd_location = location.lower()
        if ' ' in location:
            # spaceが含まれる場合の処理
            formattd_location = formattd_location.replace(' ', '')
        elif '-' in location:
            # ハイフンが含まれる場合の処理
            formattd_location = formattd_location.replace('-', '')
        elif '_' in location:
            # アンダースコアが含まれる場合の処理
            formattd_location = formattd_location.replace('_', '')
        
        # jsonファイルの読み込み
        with open(path, mode='r') as f:
            regions = json.load(f)

        # 判定
        if formattd_location in regions:
            return formattd_location
        else:
            raise ValueError(f'location: "{location}" is not in Azure Locations')