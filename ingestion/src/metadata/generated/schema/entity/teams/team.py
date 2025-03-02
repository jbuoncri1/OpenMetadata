# generated by datamodel-codegen:
#   filename:  schema/entity/teams/team.json
#   timestamp: 2021-10-01T19:50:55+00:00

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, constr

from ...type import basic, entityReference, profile


class TeamName(BaseModel):
    __root__: constr(min_length=1, max_length=64) = Field(
        ...,
        description='A unique name of the team typically the team ID from an identity provider. Example - group Id from LDAP.',
    )


class Team(BaseModel):
    id: basic.Uuid
    name: TeamName
    displayName: Optional[str] = Field(
        None, description="Name used for display purposes. Example 'Data Science team'."
    )
    description: Optional[str] = Field(None, description='Description of the team.')
    href: basic.Href = Field(
        ..., description='Link to the resource corresponding to this entity.'
    )
    profile: Optional[profile.Profile] = Field(
        None, description='Team profile information.'
    )
    deleted: Optional[bool] = Field(
        None, description='When true the team has been deleted.'
    )
    users: Optional[entityReference.EntityReferenceList] = Field(
        None, description='Users that are part of the team.'
    )
    owns: Optional[entityReference.EntityReferenceList] = Field(
        None, description='List of entities owned by the team.'
    )
