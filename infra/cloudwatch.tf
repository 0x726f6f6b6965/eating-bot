resource "aws_cloudwatch_log_group" "api_gateway_log" {
  name              = var.log_path
  retention_in_days = var.log_keep_day
}
