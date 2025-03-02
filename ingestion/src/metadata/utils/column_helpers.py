import re
from typing import Any, Dict, Optional, Set, Type
from sqlalchemy.sql import sqltypes as types
from metadata.ingestion.api.source import SourceStatus



def register_custom_type(
        tp: Type[types.TypeEngine], output: str = None
) -> None:
    if output:
        _column_type_mapping[tp] = output
    else:
        _known_unknown_column_types.add(tp)


_column_type_mapping: Dict[Type[types.TypeEngine], str] = {
    types.Integer: "INT",
    types.Numeric: "INT",
    types.Boolean: "BOOLEAN",
    types.Enum: "ENUM",
    types._Binary: "BYTES",
    types.LargeBinary: "BYTES",
    types.PickleType: "BYTES",
    types.ARRAY: "ARRAY",
    types.VARCHAR: "VARCHAR",
    types.String: "STRING",
    types.Date: "DATE",
    types.DATE: "DATE",
    types.Time: "TIME",
    types.DateTime: "DATETIME",
    types.DATETIME: "DATETIME",
    types.TIMESTAMP: "TIMESTAMP",
    types.NullType: "NULL",
    types.JSON: "JSON",
    types.CHAR: "CHAR"
}

_known_unknown_column_types: Set[Type[types.TypeEngine]] = {
    types.Interval,
    types.CLOB,
}



def get_column_type(status: SourceStatus, dataset_name: str, column_type: Any) -> str:
    type_class: Optional[str] = None
    for sql_type in _column_type_mapping.keys():
        if isinstance(column_type, sql_type):
            type_class = _column_type_mapping[sql_type]
            break
    if type_class is None:
        for sql_type in _known_unknown_column_types:
            if isinstance(column_type, sql_type):
                type_class = "NULL"
                break
    if type_class is None and column_type in ['CHARACTER VARYING', 'CHAR']:
        type_class = 'VARCHAR'
    if type_class is None:
        status.warning(
            dataset_name, f"unable to map type {column_type!r} to metadata schema"
        )
        type_class = "NULL"

    return type_class



def get_last_index(nested_str):
    counter = 1
    for index, i in enumerate(nested_str):
        if i == '>':
            counter -= 1
        elif i == '<':
            counter += 1
        if counter == 0:
            break
    index = index - counter
    return index


def get_array_type(col_type):
    col = {}
    col['dataType'] = 'ARRAY'
    col_type = col_type[:get_last_index(col_type)+2]
    col['dataTypeDisplay'] = col_type
    col['arrayDataType'] = re.match(
        r'(?:array<)(\w*)(?:.*)', col_type).groups()[0].upper()
    return col

def _handle_complex_data_types(status,dataset_name,raw_type: str, level=0):
    col = {}
    if re.match(r'([\w\s]*)(:)(.*)',raw_type):
        name, col_type = raw_type.lstrip('<').split(':', 1)
        col['name'] = name
    else:
        col['name'] = f'field_{level}'
        if raw_type.startswith('struct<'):
            col_type = raw_type
        else:
            col_type = raw_type.lstrip('<').split(':', 1)[0]
    if re.match(r'(struct)(.*)', col_type):
        children = []
        col_type = re.match(r'(struct<)(.*)', col_type).groups()[1]
        pluck_index = get_last_index(col_type)
        pluck_nested = col_type[:pluck_index+1]
        while pluck_nested != '':
            col['dataType'] = 'STRUCT'
            plucked = col_type[:get_last_index(col_type)]
            counter = 0
            continue_next = False
            for index,type in enumerate(plucked.split(',')):
                if continue_next:
                    continue_next = False
                    continue
                if re.match(r'(\w*)(:)(struct)(.*)',type):
                    col_name,datatype,rest = re.match(r'(\w*)(?::)(struct)(.*)',','.join(plucked.split(',')[index:])).groups()
                    type = f"{col_name}:{datatype}{rest[:get_last_index(rest)+2]}"
                elif type.startswith('struct'):
                    datatype,rest = re.match(r'(struct)(.*)',','.join(plucked.split(',')[index:])).groups()
                    type = f"{datatype}{rest[:get_last_index(rest)+2]}"
                elif re.match(r'([\w\s]*)(:?)(map)(.*)',type):
                    get_map_type = ','.join(plucked.split(',')[index:])
                    type,col_type = re.match(r'([\w]*:?map<[\w,]*>)(.*)',get_map_type).groups()
                    continue_next = True
                elif re.match(r'([\w\s]*)(:?)(uniontype)(.*)',type):
                    get_union_type = ','.join(plucked.split(',')[index:])
                    type,col_type = re.match(r'([\w\s]*:?uniontype<[\w\s,]*>)(.*)',get_union_type).groups()
                    continue_next = True
                children.append(_handle_complex_data_types(status,dataset_name,type,counter))
                if plucked.endswith(type):
                    break
                counter += 1
            pluck_nested = col_type[get_last_index(col_type)+3:] 
            col['children'] = children
    elif col_type.startswith('array'):
        col.update(get_array_type(col_type))
    elif col_type.startswith('map'):
        col['dataType'] = 'MAP'
        col['dataTypeDisplay'] = col_type
    elif col_type.startswith('uniontype'):
        col['dataType'] = 'UNION'
        col['dataTypeDisplay'] = col_type
    else:
        if re.match(r'(?:[\w\s]*)(?:\()([\d]*)(?:\))', col_type):
            col['dataLength'] = re.match(r'(?:[\w\s]*)(?:\()([\d]*)(?:\))', col_type).groups()[0]
        else:
            col['dataLength'] = 1
        col['dataType'] = get_column_type(status,dataset_name,re.match('([\w\s]*)(?:.*)',col_type).groups()[0].upper())
        col['dataTypeDisplay'] = col_type.rstrip('>')
    return col
 