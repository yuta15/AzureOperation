from dateutil.parser import parser

from typing import Annotated
from pydantic import BeforeValidator


def datetime_validator(datetime_str: str) -> str:
    """
    str型の日付データをdatetime型に変換しチェックを行う。
    受け取るstrは以下の値を取れるようにする。
    
    1. 2025/05/10 00:00:00
    2. 2025/05/10 00:00
    3. 2025/05/10
    4. 2025-05-10 00:00:00
    5. 2025-05-10 00:00
    6. 2025-05-10
    7. 2025-05-10T00:00:00.000000+09:00 #ISO8601
    
    Args:
        datetime_str: str
            未validationのdatetime_strデータ
    Returns:
        valied_datetime :datetime
    Raises:
        ValueError: 
            datetime型へ変換できない場合にraise
    """
    try:
        valied_datetime = parser(datetime_str)
        return valied_datetime
    except Exception:
        raise ValueError(f"""
                         {datetime_str}は指定できません。
                         以下のフォーマットから指定して下しさい。
                         YYYY/MM/DD hh:mm
                         YYYY/MM/DD hh:mm:ss
                         YYYY-MM-DD hh:mm
                         YYYY-MM-DD hh:mm:ss
                         もしくはISO8601フォーマットも使用可能です。
                         """)
        
    