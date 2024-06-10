resource "aws_cloudwatch_log_group" "api_gateway_log" {
  name              = var.log_path
  retention_in_days = var.log_keep_day
  lifecycle {
    prevent_destroy = false
  }
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
  retention_in_days = var.log_keep_day
  lifecycle {
    prevent_destroy = false
  }
}
