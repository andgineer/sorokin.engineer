---
layout: post
lang: ru
ref: terraform_aws_rds_cluster_serverless_v2
title: "Terraform для AWS serverless v2 кластера RDS Postgres"
comments: true
tags: [aws, postgres, database, serverless, terraform]
---

![](/images/steampunk_db.png){:.post-title}

## AWS RDS Cluster serverless V2

### Зачем нам serverless V2

К чему нам вообще AWS RDS serverless v2?
Он даже двое дороже чем V1 из расчета за один вычислительный юнит.

Ну, например если вам понадобился RDS Proxy (AWS вариант pg_bouncer) то у вас просто нет выхода. 
RDS proxy не поддерживается для serverless V1.

Еще более сильный аргумент в том, что V2 тупо более продвинутая и современная версия с повышенной надежностью
и масштабированием.

### Terraform

Удивительно, но хотя RDS serveless v2 существует с 2020 года, внятной документации найти не удалось и поэтому и родился этот текст.

#### RDS Cluster

```hcl
resource "aws_db_subnet_group" "this" {
  name       = "my-serveless-v2-rds-cluster"
  subnet_ids = var.subnets  # your subnets
}


resource "aws_rds_cluster" "this" {
  #checkov:skip=CKV_AWS_139: Deletion protection does not play well with terraform
  #checkov:skip=CKV_AWS_327: Just encryption without KMS is ok
  #checkov:skip=CKV_AWS_162: plain password is ok for PACS Server, we do not need IAM auth
  #checkov:skip=CKV_AWS_324: we do not need DB logs
  cluster_identifier              = "my-serveless-v2-rds-cluster"
  engine                          = "aurora-postgresql"
  engine_mode                     = "provisioned"
  engine_version                  = "13.6"        
  master_username                 = jsondecode(aws_secretsmanager_secret_version.database.secret_string)["username"]
  master_password                 = jsondecode(aws_secretsmanager_secret_version.database.secret_string)["password"]
  db_subnet_group_name            = aws_db_subnet_group.this.name
  vpc_security_group_ids          = var.ecs_security_groups # your security groups
  skip_final_snapshot             = true
  deletion_protection             = false
  storage_encrypted               = true
  backup_retention_period         = 7
  copy_tags_to_snapshot           = true
  db_cluster_parameter_group_name = "default.aurora-postgresql13"
  database_name                   = "mydb"

  serverlessv2_scaling_configuration {
    min_capacity = 0.5
    max_capacity = var.db_max_units  # your setting for max ACUs
  }
}
```

Первый сюрприз - `provisioned` режим. Для serverless V1 использовался более логичный `serverless`.
 
Немаловажна и версия Postgres. Serverless V2 работает только для версий после 13.6.

И еще неожиданность - сбросить вычислительные юниты до 0, как это позволял serverless V1, невозможно. Минимум 0.5 ACU.
Это примерно $45 в месяц.

Магию с `jsondecode` я объясню позднее, пока воспринимайте это просто как некие секреты для авторизации в БД.

Важный момент - использование `serverlessv2_scaling_configuration`, только он подходит для serverless V2.

#### RDS instance

И снова неожиданность - для RDS serverless V2 вам нужен instance.

Если для serverless V1 достаточно было описать RDS cluster, здесь это не работает.

Без этого в serverless v2 создание endpoints навсегда застрянет в статусе `creating`.

```hcl
resource "aws_rds_cluster_instance" "this" {
  identifier                 = "my-serveless-v2-rds"
  cluster_identifier         = aws_rds_cluster.this.id
  instance_class             = "db.serverless"
  engine                     = aws_rds_cluster.this.engine
  engine_version             = aws_rds_cluster.this.engine_version
  auto_minor_version_upgrade = true
  monitoring_interval        = 5

  tags = var.tags
}
```

Обратите внимание на специальный класс `db.serverless`.

Чтобы оставаться сухими [(DRY)](https://ru.wikipedia.org/wiki/Don%E2%80%99t_repeat_yourself) мы ссылаемся на значения
для `engine` и `engine_version` в кластере.

Кластер будет создаваться неспешно, дождитесь когда он будет готов к работе.

#### Secrets

Я обещал объяснить про `jsondecode`.

Мы создаем случайный пароль и сохраняем его в AWS Secrets Manager.
Далее создаем RDS Cluster указывая этот пароль.

А после создания DB Cluster добавляем endpoint и название database в тот же самый секрет.
Это уже не секреты, конечно, но удобно, когда все в одном месте.

Вся эта магия происходит автоматически благодаря следующему коду:

```hcl
resource "random_password" "db" {
  length  = 16
  special = false
}

resource "aws_secretsmanager_secret" "database" {
  #checkov:skip=CKV_AWS_149: do not need KMS encryption here
  name                    = "database"
  description             = "Master username and password for the database"
  recovery_window_in_days = 0 # it's perfectly safe to delete and we do not need AWS delete protection
}

resource "aws_secretsmanager_secret_version" "database" {
  # Store credentials before RDS cluster created
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    username = "myuser"
    password = random_password.db.result
  })
}

resource "aws_secretsmanager_secret_version" "database_endpoint" {
  # Store endpoint after RDS cluster created
  secret_id = aws_secretsmanager_secret.database.id
  secret_string = jsonencode({
    database = jsondecode(aws_secretsmanager_secret_version.database.secret_string)["database"]
    username = jsondecode(aws_secretsmanager_secret_version.database.secret_string)["username"]
    password = jsondecode(aws_secretsmanager_secret_version.database.secret_string)["password"]

    endpoint = aws_rds_cluster.this.endpoint
    databse = aws_rds_cluster.this.database_name
  })
  depends_on = [aws_rds_cluster.this]
}
```

Поскольку все манипуляции с секретами выполняет terraform нет необходимости в специальных IAM.
Но конечно сам terraform надо запускать так, чтобы он имел доступ к AWS Secrets Manager.
