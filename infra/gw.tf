resource "aws_apigatewayv2_api" "eating_bot_api" {
  name          = "eating-bot-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "eating_bot_integration" {
  api_id           = aws_apigatewayv2_api.eating_bot_api.id
  integration_type = "AWS_PROXY"

  connection_type      = "INTERNET"
  description          = "Get recommend food"
  integration_method   = "POST"
  integration_uri      = aws_lambda_function.lambda.invoke_arn
  passthrough_behavior = "WHEN_NO_MATCH"
  depends_on           = [aws_apigatewayv2_api.eating_bot_api]
}


resource "aws_apigatewayv2_route" "callback_handler" {
  api_id    = aws_apigatewayv2_api.eating_bot_api.id
  route_key = "POST /callback"

  target = "integrations/${aws_apigatewayv2_integration.eating_bot_integration.id}"

}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.eating_bot_api.id
  name        = "$default"
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_log.arn
    format          = jsonencode({ "requestId" : "$context.requestId", "ip" : "$context.identity.sourceIp", "requestTime" : "$context.requestTime", "httpMethod" : "$context.httpMethod", "routeKey" : "$context.routeKey", "status" : "$context.status", "protocol" : "$context.protocol", "responseLength" : "$context.responseLength" })
  }
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.eating_bot_api.execution_arn}/*/*"
}
