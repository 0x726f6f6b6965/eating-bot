output "api_arn" {
  value = aws_apigatewayv2_api.eating_bot_api.execution_arn
}

output "api_url" {
  value = aws_apigatewayv2_api.eating_bot_api.api_endpoint
}
