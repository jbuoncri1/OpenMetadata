#!/bin/bash
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

cd /

while ! curl -o - 172.16.239.10:3306; do sleep 1; done

unzip -o catalog*.zip
cp /catalog.yaml /catalog-1.0.0-SNAPSHOT/conf/

cd /catalog-1.0.0-SNAPSHOT
./bootstrap/bootstrap_storage.sh migrate

./bin/catalog-server-start.sh conf/catalog.yaml
