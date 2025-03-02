# generated by datamodel-codegen:
#   filename:  schema/api/tags/createTag.json
#   timestamp: 2021-10-01T19:50:55+00:00

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from ...entity.tags import tagCategory


class CreateTagApiRequest(BaseModel):
    name: tagCategory.TagName
    description: str = Field(..., description='Unique name of the tag category')
    associatedTags: Optional[List[str]] = Field(
        None, description='Fully qualified names of tags associated with this tag'
    )
