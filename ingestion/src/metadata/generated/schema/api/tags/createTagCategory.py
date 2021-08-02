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
#   filename:  schema/api/tags/createTagCategory.json
#   timestamp: 2021-07-31T17:12:10+00:00

from __future__ import annotations

from pydantic import BaseModel, Field

from ...entity.tags import tagCategory


class CreateTagCategoryRequest(BaseModel):
    name: tagCategory.TagName
    description: str = Field(..., description='Description of the tag category')
    categoryType: tagCategory.TagCategoryType
