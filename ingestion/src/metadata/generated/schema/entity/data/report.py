# generated by datamodel-codegen:
#   filename:  schema/entity/data/report.json
#   timestamp: 2021-10-01T19:50:55+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, constr

from ...type import basic, entityReference, usageDetails


class Report(BaseModel):
    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies this report.'
    )
    name: constr(min_length=1, max_length=64) = Field(
        ..., description='Name that identifies this report instance uniquely.'
    )
    fullyQualifiedName: Optional[constr(min_length=1, max_length=64)] = Field(
        None,
        description="A unique name that identifies a report in the format 'ServiceName.ReportName'.",
    )
    description: Optional[str] = Field(
        None, description='Description of this report instance.'
    )
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this report.'
    )
    owner: Optional[entityReference.EntityReference] = Field(
        None, description='Owner of this pipeline.'
    )
    service: entityReference.EntityReference = Field(
        ..., description='Link to service where this report is hosted in.'
    )
    usageSummary: Optional[usageDetails.TypeUsedToReturnUsageDetailsOfAnEntity] = Field(
        None, description='Latest usage information for this database.'
    )
