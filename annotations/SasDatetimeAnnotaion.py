from datetime import datetime

from typing import Annotated
from pydantic import PlainValidator

from annotations.DatetimeAnnotation import datetime_validator


def sas_datetime_validator(sas_datetime: str) -> str:
    """
    sasのフォーマットをDD.HH:MM:SSに変更するための関数
    Args:
        sas_datetime: str
            受け取った文字列
    Return:
        valida_sas_dateitme: str
            DD.HH:MM:SSへparseされた文字列
    """
    return datetime_validator(sas_datetime).strftime('%d.%H:%M:%S')


SasDatetimeAnnotaion = Annotated[str, PlainValidator(sas_datetime_validator)]