data "archive_file" "zip" {
  type        = "zip"
  source_dir  = "${path.cwd}/${var.lambda_source}"
  output_path = "line_bot_package.zip"
}

resource "aws_lambda_function" "lambda" {
  function_name    = "eating-bot"
  description      = "Eating Line bot Lambda Function"
  handler          = "${var.lambda_entry_file}.${var.lambda_function}"
  runtime          = "python3.12"
  role             = aws_iam_role.lambda_role.arn
  filename         = "line_bot_package.zip"
  source_code_hash = data.archive_file.zip.output_base64sha256
  timeout          = 10

  environment {
    variables = {
      CHANNEL_SECRET       = var.line_channel_secret
      CHANNEL_ACCESS_TOKEN = var.line_channel_access_token
      MAP_API_KEY          = var.map_api_key
    }
  }
}

