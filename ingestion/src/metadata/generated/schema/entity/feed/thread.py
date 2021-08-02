#  Licensed to the Apache Software Foundation (ASF) under one or more
#  contributor license agreements. See the NOTICE file distributed with
#  this work for additional information regarding copyright ownership.
#  The ASF licenses this file to You under the Apache License, Version 2.0
#  (the "License"); you may not use this file except in compliance with
#  the License. You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# generated by datamodel-codegen:
#   filename:  schema/entity/feed/thread.json
#   timestamp: 2021-07-31T17:12:10+00:00

from __future__ import annotations

from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from ...type import basic


class Post(BaseModel):
    message: str = Field(
        ...,
        description='Message in markdown format. See markdown support for more details.',
    )
    postTs: Optional[datetime] = Field(None, description='Timestamp of the post')
    from_: basic.Uuid = Field(
        ...,
        alias='from',
        description='ID of User (regular user or a bot) posting the message',
    )


class FeedEntity(BaseModel):
    id: basic.Uuid = Field(
        ..., description='Unique identifier that identifies an entity instance'
    )
    href: Optional[basic.Href] = Field(
        None, description='Link to the resource corresponding to this entity'
    )
    threadTs: Optional[Any] = Field(
        None, description='Timestamp of the when the first post created the thread'
    )
    about: basic.EntityLink = Field(
        ...,
        description='Data asset about which this thread is created for with format <#E/{enties}/{entityName}/{field}/{fieldValue}',
    )
    addressedTo: Optional[basic.EntityLink] = Field(
        None,
        description='User or team this thread is addressed to in format <#E/{enties}/{entityName}/{field}/{fieldValue}',
    )
    posts: List[Post]
