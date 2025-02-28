/*
 *  Licensed to the Apache Software Foundation (ASF) under one or more
 *  contributor license agreements. See the NOTICE file distributed with
 *  this work for additional information regarding copyright ownership.
 *  The ASF licenses this file to You under the Apache License, Version 2.0
 *  (the "License"); you may not use this file except in compliance with
 *  the License. You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

package org.openmetadata.catalog.jdbi3;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.openmetadata.catalog.entity.Bots;
import org.openmetadata.catalog.util.EntityUtil;
import org.openmetadata.catalog.util.JsonUtils;
import org.skife.jdbi.v2.sqlobject.Bind;
import org.skife.jdbi.v2.sqlobject.CreateSqlObject;
import org.skife.jdbi.v2.sqlobject.SqlQuery;
import org.skife.jdbi.v2.sqlobject.SqlUpdate;

import java.io.IOException;
import java.util.List;

public abstract class BotsRepository {
  @CreateSqlObject
  abstract BotsDAO botsDAO();

  public Bots insert(Bots bots) throws JsonProcessingException {
    bots.setHref(null);
    botsDAO().insert(JsonUtils.pojoToJson(bots));
    return bots;
  }

  public Bots findByName(String name) throws IOException {
    return EntityUtil.validate(name, botsDAO().findByName(name), Bots.class);
  }

  public List<Bots> list(String name) throws IOException {
    return JsonUtils.readObjects(botsDAO().list(name), Bots.class);
  }

  public interface BotsDAO {
    @SqlUpdate("INSERT INTO bot_entity(json) VALUES (:json)")
    void insert(@Bind("json") String json);

    @SqlQuery("SELECT json FROM bot_entity WHERE name = :name")
    String findByName(@Bind("name") String name);

    @SqlQuery("SELECT json FROM bot_entity WHERE (name = :name OR :name is NULL)")
    List<String> list(@Bind("name") String name);
  }
}
