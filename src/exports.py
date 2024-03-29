from dotenv import load_dotenv
load_dotenv()

import os

slack_bot_token     = os.getenv("SLACK_BOT_TOKEN")
slack_channel_id    = os.getenv("SLACK_CHANNEL_ID")
slack_channel_name  = os.getenv("SLACK_CHANNEL_NAME")

aws_log_group_name  = os.getenv("AWS_LOG_GROUP_NAME")
aws_log_stream_name = os.getenv("AWS_LOG_STREAM_NAME")
aws_region_name     = os.getenv("AWS_REGION_NAME")

notion_token        = os.getenv("NOTION_TOKEN")
notion_db_id        = os.getenv("NOTION_TABLE_ID")
notion_view_url     = os.getenv("NOTION_VIEW_URL")

s3_bucket_name      = os.getenv("S3_BUCKET_NAME")
