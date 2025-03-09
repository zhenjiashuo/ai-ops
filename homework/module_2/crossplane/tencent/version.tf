terraform {
  required_version = "> 0.13.0"
  required_providers {
    tencentcloud = {
      source = "tencentcloudstack/tencentcloud"
    }
  }
}

provider "helm" {
  kubernetes {
    config_path = "${path.module}/config.yaml"
  }
}
