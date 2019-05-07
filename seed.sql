
use `inspection`

delete from roles;

insert into roles(id, tag, name) values(uuid(), 0, "管理员");
insert into roles(id, tag, name) values(uuid(), 1, "质检员");




delete from permissions;

insert into permissions(id, role_tags, url, method, description, module) values(uuid(), "0", "/users/view", "GET", "读取所有用户", "UserManagement");

insert into permissions(id, role_tags, url, method, description, module) values(uuid(), "0", "/users/one", "GET", "读取单个用户","UserManagement");

insert into permissions(id, role_tags, url, method, description, module) values(uuid(), "0", "/users/create", "POST", "创建单个用户", "UserManagement");

insert into permissions(id, role_tags, url, method, description, module) values(uuid(), "0", "/users/delete", "DELETE", "删除一个用户", "UserManagement");

insert into permissions(id, role_tags, url, method, description, module) values(uuid(), "0", "/users/update", "PUT", "修改一个用户", "UserManagement");

INSERT INTO `users` VALUES (
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    'admin',
    'Sentinel Tec',
    'admin@sentineltec.com','$6$rounds=656000$DmZR8J1ByA3FFP.F$tzfdB8wFipYmqjZBD.LcoBjHNeizhlAnUOBvHykNCOkEfxtvsOx9/CiVJBLvJywwSS.ijr5y0FMHFWh2bkWNx/',
    0,
    1,
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04'
);

-- Seed Topic Analyzer

INSERT INTO topics(id, name, description, is_valid, user_id, created_at, updated_at) VALUES (
    'a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a',
    '业务1',
    '业务1描述',
    1,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04'
);


-- Seed Patter Analyzer

INSERT INTO pattern_analyzers(id, name, description, target, user_id, created_at, updated_at, is_valid, topic_id) VALUES (
    uuid(), 
    '案例话术分析器1',
    '案例话术分析器描述',
    0,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04',
    1,
    "a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a"
);

INSERT INTO pattern_analyzers(id, name, description, target, user_id, created_at, updated_at, is_valid, topic_id) VALUES (
    uuid(), 
    '案例话术分析器2',
    '案例话术分析器描述',
    0,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04',
    1,
    "a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a"
);

INSERT INTO pattern_analyzers(id, name, description, target, user_id, created_at, updated_at, is_valid, topic_id) VALUES (
    uuid(), 
    '案例话术分析器3',
    '案例话术分析器描述',
    0,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04',
    1,
    "a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a"
);

INSERT INTO pattern_analyzers(id, name, description, target, user_id, created_at, updated_at, is_valid, topic_id) VALUES (
    uuid(), 
    '案例话术分析器4',
    '案例话术分析器描述',
    0,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04',
    1,
    "a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a"
);

INSERT INTO pattern_analyzers(id, name, description, target, user_id, created_at, updated_at, is_valid, topic_id) VALUES (
    uuid(), 
    '案例话术分析器5',
    '案例话术分析器描述',
    0,
    'ce7ffcb4-bd46-11e8-b3e7-784f437148a2',
    '2018-09-20 19:34:04',
    '2018-09-20 19:34:04',
    1,
    "a3fd90ed-d50a-4c9d-a4ea-7683f2b1127a"
);
