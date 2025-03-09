# Configure the TencentCloud Provider
provider "tencentcloud" {
  region     = var.regoin
  secret_id  = var.secret_id
  secret_key = var.secret_key
}

data "tencentcloud_redis_zone_config" "zone" {
  type_id = 7
}

resource "tencentcloud_vpc" "vpc" {
  cidr_block = "10.0.0.0/16"
  name       = "tf_redis_vpc"
}

resource "tencentcloud_subnet" "subnet" {
  vpc_id            = tencentcloud_vpc.vpc.id
  availability_zone = data.tencentcloud_redis_zone_config.zone.list[0].zone
  name              = "tf_redis_subnet"
  cidr_block        = "10.0.1.0/24"
}

resource "tencentcloud_redis_instance" "example" {
  availability_zone  = data.tencentcloud_redis_zone_config.zone.list[0].zone
  type_id            = 8
  password           = "Password@123"
  mem_size           = 512
  redis_shard_num    = 1
  redis_replicas_num = 1
  name               = "tf-example"
  port               = 6379
  vpc_id             = tencentcloud_vpc.vpc.id
  subnet_id          = tencentcloud_subnet.subnet.id  
}