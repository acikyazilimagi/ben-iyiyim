terraform {
  cloud {
    hostname     = "app.terraform.io"
    organization = "afetyardim"
    workspaces {
      name = "ben-iyiyim"
    }
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 4.52.0"
    }
  }
}

provider "aws" {
  region     = var.region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

data "terraform_remote_state" "infrastructure" {
  backend = "remote"

  config = {
    organization = "afetyardim"
    workspaces = {
      name = "deprem-yardim-cloud-infra"
    }
  }
}

locals {
  app             = "beniyiyim"
  vpc_id          = data.terraform_remote_state.infrastructure.outputs.vpc_id
  ecs_cluster_arn = data.terraform_remote_state.infrastructure.outputs.ecs_cluster_arn
  public_subnets  = data.terraform_remote_state.infrastructure.outputs.public_subnets
  private_subnets = data.terraform_remote_state.infrastructure.outputs.private_subnets
}

data "aws_iam_role" "execution_role" {
  name = "ecsServiceRole"
}

resource "aws_security_group" "this" {
  name        = "${local.app}-sg"
  description = "${local.app} sg"
  vpc_id      = local.vpc_id

  tags = {
    Name = "${local.app}-sg"
  }
}

resource "aws_security_group_rule" "alb_ingress" {
  description              = "HTTP"
  from_port                = 80
  to_port                  = 80
  protocol                 = "tcp"
  source_security_group_id = aws_security_group.alb.id
  type                     = "ingress"
  security_group_id        = aws_security_group.this.id
}

resource "aws_security_group_rule" "outbound_rule" {
  type              = "egress"
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
  ipv6_cidr_blocks  = ["::/0"]
  security_group_id = aws_security_group.this.id
}

resource "aws_ecs_task_definition" "this" {
  family                   = local.app
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = 2048
  memory                   = 4096
  execution_role_arn       = data.aws_iam_role.execution_role.arn
  container_definitions = jsonencode([
    {
      essential = true
      name      = local.app
      image     = "beniyiyim" //bunu düzelticem
      cpu       = 2048
      memory    = 4096
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-create-group  = "true"
          awslogs-group         = "/ecs/${local.app}"
          awslogs-region        = var.region
          awslogs-stream-prefix = "ecs"
        }
      }
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    }
  ])
}

resource "aws_lb_target_group" "this" {
  name        = "${local.app}-tg"
  port        = 80
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = local.vpc_id

  health_check {
    enabled  = true
    path     = "/"
    port     = 80
    protocol = "HTTP"
  }

  tags = {
    Name = "${local.app}-tg"
  }
}

resource "aws_ecs_service" "this" {
  name            = "${local.app}-service"
  cluster         = local.ecs_cluster_arn
  task_definition = aws_ecs_task_definition.this.arn
  launch_type     = "FARGATE"
  desired_count   = 2

  network_configuration {
    subnets          = local.private_subnets
    security_groups  = [aws_security_group.this.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = local.app
    container_port   = 80
  }
}


resource "aws_lb_listener_rule" "http" {
  listener_arn = aws_lb_listener.http.arn
  priority     = 100

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }

  condition {
    path_pattern {
      values = ["*"]
    }
  }
}

resource "aws_security_group" "alb" {
  name        = "${local.app}-alb-sg"
  description = "${local.app} alb sg"
  vpc_id      = local.vpc_id

  ingress {
    description = "Allow IPv4 HTTP traffic from outside"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow IPv4 HTTPS traffic from outside"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description     = ""
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.this.id]
  }

  egress {
    description = ""
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lb" "this" {
  name               = "${local.app}-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb.id]
  subnets            = local.public_subnets

  enable_deletion_protection = true

  tags = {
    Name = "${local.app}-alb"
  }
}

resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.this.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.this.arn
  }
}
