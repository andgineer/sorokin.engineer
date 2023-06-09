---
layout: post
lang: en
ref: terraform_aws_rds_cluster_serverless_v2
title: "Terraform for AWS serverless v2 RDS cluster with Postgres"
comments: true
tags: [aws, postgres, database, serverless, terraform]
---

![](/images/steampunk_db.png){:.post-title}

## AWS RDS Cluster serverless V2

### Motivation to move to serverless V2

Why you would need AWS RDS serverless v2?
Serverless V2 ACUs even are twice as expensive as V1.

If you need RDS Proxy (AWS flavour of pg_bouncer) you have no choice. RDS proxy is not available for serverless V1.

And serverless V2 is really improved in terms of performance, scalability and availability.

### Terraform code

Surprisingly there are no clear documentation so I am going to save you the chase and give ready to use terraform code.

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

The first gotcha here is `provisioned` mode. In serverless V1 it was more intuitive `serverless`.
 
Second important thing - Postgres version. Serverless V2 works with versions 13.6 and higher.

And another unexpected thing - you cannot scale down to 0 like with serverless V1. The minimum is 0.5 ACU.
This is around $45 per month.

What is the magic with `jsondecode` I will explain later, but for the moment that does not matter - this is just credentials for the database.

Important secret ingredient here is `serverlessv2_scaling_configuration` - this is the only way to configure serverless V2.

#### RDS instance

Another gotcha - for RDS serverless V2 you do need instance.

For serverless V1 you just describe your RDS cluster and that's it.

If you do that for serverless v2 endpoints will freeze forever in status `creating`.

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

This is important to use here magic `db.serverless` instance class.

And in `engine` and `engine_version` we just refer to our cluster to be [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) and do not copy values.

It took some time to create so be patient.

#### Secrets

And I promised to explain `jsondecode` magic.

We create random secret and place it to the AWS Secrets Manager.
After that we create RDS Cluster giving this secret as password.

And on the next step from created DB Cluster we add endpoint and database name to the same secret.
Thease are no secrets but it's nice to have them in one place.

All this magic will happen automatically helps to the following code:

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

All manipulations with the secrets performed by terraform so you do not need any additional permissions in IAM.
But of cause user that run terraform should have access to the AWS Secrets Manager.
