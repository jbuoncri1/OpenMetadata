# generated by datamodel-codegen:
#   filename:  schema/entity/data/table.json
#   timestamp: 2021-10-01T19:50:55+00:00

from __future__ import annotations

from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Extra, Field, constr

from ...type import basic, entityReference, tagLabel, usageDetails


class TableType(Enum):
    Regular = 'Regular'
    External = 'External'
    View = 'View'
    SecureView = 'SecureView'
    MaterializedView = 'MaterializedView'


class DataType(Enum):
    NUMBER = 'NUMBER'
    TINYINT = 'TINYINT'
    SMALLINT = 'SMALLINT'
    INT = 'INT'
    BIGINT = 'BIGINT'
    BYTEINT = 'BYTEINT'
    FLOAT = 'FLOAT'
    DOUBLE = 'DOUBLE'
    DECIMAL = 'DECIMAL'
    NUMERIC = 'NUMERIC'
    TIMESTAMP = 'TIMESTAMP'
    TIME = 'TIME'
    DATE = 'DATE'
    DATETIME = 'DATETIME'
    INTERVAL = 'INTERVAL'
    STRING = 'STRING'
    MEDIUMTEXT = 'MEDIUMTEXT'
    TEXT = 'TEXT'
    CHAR = 'CHAR'
    VARCHAR = 'VARCHAR'
    BOOLEAN = 'BOOLEAN'
    BINARY = 'BINARY'
    VARBINARY = 'VARBINARY'
    ARRAY = 'ARRAY'
    BLOB = 'BLOB'
    LONGBLOB = 'LONGBLOB'
    MEDIUMBLOB = 'MEDIUMBLOB'
    MAP = 'MAP'
    STRUCT = 'STRUCT'
    UNION = 'UNION'
    SET = 'SET'
    GEOGRAPHY = 'GEOGRAPHY'
    ENUM = 'ENUM'
    JSON = 'JSON'


class Constraint(Enum):
    NULL = 'NULL'
    NOT_NULL = 'NOT_NULL'
    UNIQUE = 'UNIQUE'
    PRIMARY_KEY = 'PRIMARY_KEY'


class ConstraintType(Enum):
    UNIQUE = 'UNIQUE'
    PRIMARY_KEY = 'PRIMARY_KEY'
    FOREIGN_KEY = 'FOREIGN_KEY'


class TableConstraint(BaseModel):
    constraintType: Optional[ConstraintType] = None
    columns: Optional[List[str]] = Field(
        None, description='List of column names corresponding to the constraint.'
    )


class ColumnName(BaseModel):
    __root__: constr(regex=r'^[^.]*$', min_length=1, max_length=64) = Field(
        ...,
        description='Local name (not fully qualified name) of the column. ColumnName is `-` when the column is not named in struct dataType. For example, BigQuery supports struct with unnamed fields',
    )


class TableName(BaseModel):
    __root__: constr(regex=r'^[^.]*$', min_length=1, max_length=64) = Field(
        ..., description='Local name (not fully qualified name) of a table.'
    )


class FullyQualifiedColumnName(BaseModel):
    __root__: constr(min_length=1, max_length=256) = Field(
        ...,
        description='Fully qualified name of the column that includes `serviceName.databaseName.tableName.columnName[.nestedColumnName]`. When columnName is null for dataType struct fields, `field_#` where `#` is field index is used. For map dataType, for key the field name `key` is used and for the value field `value` is used.',
    )


class JoinedWithItem(BaseModel):
    fullyQualifiedName: Optional[FullyQualifiedColumnName] = None
    joinCount: Optional[int] = None


class ColumnJoins(BaseModel):
    class Config:
        extra = Extra.forbid

    columnName: Optional[ColumnName] = None
    joinedWith: Optional[List[JoinedWithItem]] = Field(
        None,
        description='Fully qualified names of the columns that this column is joined with.',
    )


class TableData(BaseModel):
    class Config:
        extra = Extra.forbid

    columns: Optional[List[ColumnName]] = Field(
        None,
        description='List of local column names (not fully qualified column names) of the table.',
    )
    rows: Optional[List[List]] = Field(
        None, description='Data for multiple rows of the table.'
    )


class ColumnProfile(BaseModel):
    name: Optional[str] = Field(None, description='Column Name.')
    uniqueCount: Optional[float] = Field(
        None, description='No. of unique values in the column.'
    )
    uniqueProportion: Optional[float] = Field(
        None, description='Proportion of number of unique values in a column.'
    )
    nullCount: Optional[float] = Field(
        None, description='No.of null values in a column.'
    )
    nullProportion: Optional[float] = Field(
        None, description='No.of null value proportion in columns.'
    )
    min: Optional[str] = Field(None, description='Minimum value in a column.')
    max: Optional[str] = Field(None, description='Maximum value in a column.')
    mean: Optional[str] = Field(None, description='Avg value in a column.')
    median: Optional[str] = Field(None, description='Median value in a column.')
    stddev: Optional[float] = Field(None, description='Standard deviation of a column.')


class TableJoins(BaseModel):
    class Config:
        extra = Extra.forbid

    startDate: Optional[basic.Date] = Field(
        None, description='Date can be only from today going back to last 29 days.'
    )
    dayCount: Optional[int] = 1
    columnJoins: Optional[List[ColumnJoins]] = None


class TableProfile(BaseModel):
    class Config:
        extra = Extra.forbid

    profileDate: Optional[basic.Date] = Field(
        None, description='Data one which profile is taken.'
    )
    columnCount: Optional[float] = Field(
        None, description='No.of columns in the table.'
    )
    rowCount: Optional[float] = Field(None, description='No.of rows in the table.')
    columnProfile: Optional[List[ColumnProfile]] = Field(
        None, description='List of local column profiles of the table.'
    )


class Column(BaseModel):
    class Config:
        extra = Extra.forbid

    name: ColumnName
    dataType: DataType = Field(
        ..., description='Data type of the column (int, date etc.).'
    )
    arrayDataType: Optional[DataType] = Field(
        None,
        description='Data type used array in dataType. For example, `array<int>` has dataType as `array` and arrayDataType as `int`.',
    )
    dataLength: Optional[int] = Field(
        None,
        description='Length of `char`, `varchar`, `binary`, `varbinary` `dataTypes`, else null. For example, `varchar(20)` has dataType as `varchar` and dataLength as `20`.',
    )
    dataTypeDisplay: Optional[str] = Field(
        None,
        description='Display name used for dataType. This is useful for complex types, such as `array<int>, map<int,string>, struct<>, and union types.',
    )
    description: Optional[str] = Field(None, description='Description of the column.')
    fullyQualifiedName: Optional[FullyQualifiedColumnName] = None
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags associated with the column.'
    )
    constraint: Optional[Constraint] = Field(
        None, description='Column level constraint.'
    )
    ordinalPosition: Optional[int] = Field(
        None, description='Ordinal position of the column.'
    )
    jsonSchema: Optional[str] = Field(
        None, description='Json schema only if the dataType is JSON else null.'
    )
    children: Optional[List[Column]] = Field(
        None,
        description='Child columns if dataType or arrayDataType is `map`, `struct`, or `union` else `null`.',
    )


class Table(BaseModel):
    id: basic.Uuid = Field(..., description='Unique identifier of this table instance.')
    name: TableName = Field(
        ..., description='Name of a table. Expected to be unique within a database.'
    )
    description: Optional[str] = Field(None, description='Description of a table.')
    href: Optional[basic.Href] = Field(None, description='Link to this table resource.')
    tableType: Optional[TableType] = None
    fullyQualifiedName: Optional[str] = Field(
        None,
        description='Fully qualified name of a table in the form `serviceName.databaseName.tableName`.',
    )
    columns: List[Column] = Field(..., description='Columns in this table.')
    tableConstraints: Optional[List[TableConstraint]] = Field(
        None, description='Table constraints.'
    )
    usageSummary: Optional[usageDetails.TypeUsedToReturnUsageDetailsOfAnEntity] = Field(
        None, description='Latest usage information for this table.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this table.'
    )
    followers: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Followers of this table.'
    )
    database: Optional[entityReference.EntityReference] = Field(
        None, description='Reference to Database that contains this table.'
    )
    viewDefinition: Optional[basic.SqlQuery] = Field(
        None, description='View Definition in SQL. Applies to TableType.View only.'
    )
    tags: Optional[List[tagLabel.TagLabel]] = Field(
        None, description='Tags for this table.'
    )
    joins: Optional[TableJoins] = Field(
        None,
        description='Details of other tables this table is frequently joined with.',
    )
    sampleData: Optional[TableData] = Field(
        None, description='Sample data for a table.'
    )
    tableProfile: Optional[List[TableProfile]] = Field(
        None, description='Data profile for a table.'
    )


Column.update_forward_refs()
