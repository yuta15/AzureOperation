
from dateutil.parser import parse
from pydantic import BaseModel, Field

from datetime import datetime, timezone, timedelta

datetime1 = "2025/05/10 00:00:00"
datetime2 = "2025/05/10 00:00"
datetime3 = "2025/05/10"

datetime4 = "2025-05-10 00:00:00"
datetime5 = "2025-05-10 00:00"
datetime6 = "2025-05-10"
datetime7 = "2025-05-10T00:00:00.000000+09:00"

date1 = parse(datetime1)
print(date1.strftime('%d.%H:%M:%S'))
# print(parse(datetime1))
# print(parse(datetime2))
# print(parse(datetime3))
# print(parse(datetime4))
# print(parse(datetime5))
# print(parse(datetime6))
# print(parse(datetime7))