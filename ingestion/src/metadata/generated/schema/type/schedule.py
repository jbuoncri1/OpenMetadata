# generated by datamodel-codegen:
#   filename:  schema/type/schedule.json
#   timestamp: 2021-10-01T19:50:55+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from . import basic


class Schedule(BaseModel):
    startDate: Optional[basic.DateTime] = Field(
        None, description='Start date and time of the schedule.'
    )
    repeatFrequency: Optional[basic.Duration] = Field(
        None,
        description="Repeat frequency in ISO 8601 duration format. Example - 'P23DT23H'.",
    )
