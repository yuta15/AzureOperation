from typing import Annotated
from pydantic import PlainValidator


def port_validator(port_number:str) -> str:
    """
    以下の条件に沿っていることを検証する。
    Args:
        port: str
    Return:
        validated_port: str
            以下のような"int"もしくは"int-int"の値のみ
            なお、range指定の場合でも値はstart-lastの二つのみであり、
            int1-int2-int3のような値はErrorとなる
            ex) "80", "80-443"
    Exception
        ValueError
    """
    to_validate = []
    validated_port = []
    
    # 引数の型チェック
    # int型の場合はstr型に変換
    # str型の場合はそのまま使用
    # それ以外の型の場合はValueErrorを投げる
    if isinstance(port_number, int):
        port_number = str(port_number)
    elif not isinstance(port_number, str):
        raise ValueError(
            f"""
            {port_number}は不正な値です。
            port番号はint型へ変換可能なstr型もしくは, int-intのstr型である必要があります。
            """
        )

    if '-' in port_number:
        # rangeの場合の処理
        port_numbers = port_number.split('-')
        if not len(port_numbers) == 2:
            raise ValueError(
                f"""
                {port_numbers}は不正な値です。
                port範囲を指定する場合は"int-int"の形で指定してください
                """
                )
        to_validate.extend([port_numbers[0], port_numbers[-1]])
    else:
        # 単一ポートの場合の処理
        to_validate.append(port_number)

    for port in to_validate:
        # validation処理
        if not port.isdigit():
            # int型に変換できない場合の処理
            raise ValueError(
                f"""
                {port_number}は不正な値です。
                port番号はint型へ変換可能な値である必要があります。
                """
            )
        if not 0 < int(port) <= 65535:
            # port範囲外の場合の処理
            raise ValueError(
                f"""
                {port_number}は不正な値です。
                portを指定する際には"int" or "int-int"の形で指定して下さい。
                """
                )
        # 正常な値の場合はvalidated_portへ追加
        validated_port.append(int(port))
        
    if len(validated_port) == 2:
        # range指定のポートの処理。小さい順にソート
        validated_port.sort()
        return f'{validated_port[0]}-{validated_port[1]}'
    # 単一ポートの場合は文字列にしてリターン
    return str(validated_port[0])


PortAnnotation = Annotated[str, PlainValidator(port_validator)]