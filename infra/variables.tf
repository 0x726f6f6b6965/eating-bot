variable "region" {
  type    = string
  default = "us-east-1"
}

variable "service_name" {
  type    = string
  default = "eating-bot"
}

variable "lambda_entry_file" {
  type    = string
  default = "lambda_function"
}

variable "log_path" {
  type    = string
  default = "/apigateway/eating-bot"
}

variable "log_keep_day" {
  type    = number
  default = 7
}

variable "lambda_source" {
  type    = string
  default = "package"
}

variable "lambda_function" {
  type    = string
  default = "lambda_handler"
}

variable "line_channel_secret" {
  type    = string
  default = ""
}

variable "line_channel_access_token" {
  type    = string
  default = ""
}

variable "map_api_key" {
  type    = string
  default = ""
}
