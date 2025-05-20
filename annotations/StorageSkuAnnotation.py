from enum import Enum

from typing import Annotated, Dict
from pydantic import PlainValidator


class SkuType(str, Enum):
    """
    SKUの種類を定義するEnumクラス
    """
    STANDARD_LRS = "Standard_LRS"
    STANDARD_GRS = "Standard_GRS"
    STANDARD_RAGRS = "Standard_RAGRS"
    STANDARD_ZRS = "Standard_ZRS"
    PREMIUM_LRS = "Premium_LRS"
    PREMIUM_ZRS = "Premium_ZRS"
    STANDARD_GZRS = "Standard_GZRS"
    STANDARD_RAGZRS = "Standard_RAGZRS"
    STANDARDV2_LRS = "StandardV2_LRS"
    STANDARDV2_GRS = "StandardV2_GRS"
    STANDARDV2_ZRS = "StandardV2_ZRS"
    STANDARDV2_GZRS = "StandardV2_GZRS"
    PREMIUMV2_LRS = "PremiumV2_LRS"
    PREMIUMV2_ZRS = "PremiumV2_ZRS"


def storage_sku_validator(sku: str) -> Dict:
    """
    StorageAccountのskuのバリデーション用関数。
    受け取った文字列がSkuTypeに含まれるか確認。
    含まれる場合には、その値を返す。
    含まれない場合はValueErrorを返す。
    Args:
        sku :str
            SKUの文字列
    Returns:
        SkuType[sku].value: str
            SkuTypeに含まれるSKUの値
    Raises:
        ValueError: SKUがSkuTypeに含まれない場合
    """
    sku = sku.upper()
    if '-' in sku:
        sku = sku.replace('-', '_')
    if sku not in SkuType._member_names_:
        # skuがSkuTypeに存在しない場合の処理
        raise ValueError(f"""
                         {sku}は不正な値です。次のリストから選択してください。
                         {SkuType._member_names_}
                         """)

    if 'PREMIUM' in sku:
        return {
            'name': SkuType[sku].value,
            'tier': 'Premium'
        }
    else:
        return {
            'name': SkuType[sku].value,
            'tier': 'Standard'
        }
        

StorageSkuAnnotation = Annotated[Dict['str', 'str'], PlainValidator(storage_sku_validator)]