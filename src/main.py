import exports
from boto3 import client
from slack_sdk import WebClient

import notion_helper

logs_file_name  = "logs.txt"


def get_cloudwatch_logs():
  logs_client = client(
    'logs',
    region_name   = exports.aws_region_name
  )
  events = logs_client.get_log_events(
    logGroupName  = exports.aws_log_group_name,
    logStreamName = exports.aws_log_stream_name,
    startFromHead = True
  )
  with open(logs_file_name,'w') as log_file:
    if "events" in events:
      log_events = events["events"]
      for log_event_item in log_events:
        log_message = log_event_item["message"].strip()
        if log_message != "":
          log_file.write(log_message + "\n")

def send_message_to_slack():
  slack = WebClient(
    token = exports.slack_bot_token
  )
  response = slack.chat_postMessage(
    channel = exports.slack_channel_name,
    text    = "Hello world"
  )
  print(response)
  
  response_file_upload = slack.files_upload_v2(
    channel = exports.slack_channel_id,
    file    = logs_file_name
  )
  
  print(response_file_upload)

def main():
  print("Hello World")
  get_cloudwatch_logs()
  send_message_to_slack()

if __name__ == "__main__":
  main()
  notion_helper.create_a_page()
