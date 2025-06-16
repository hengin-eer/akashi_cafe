import re


def parse_pg_enum_array(enum_str):
    if enum_str is None:
        return None
    # PostgreSQLのARRAY表記 "{小麦,卵,乳}" 等をリストに変換
    return re.findall(r"[^{},\s]+", enum_str)
