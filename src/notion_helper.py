import exports
import requests
import json
from boto3 import client

headers = {
    "Authorization": f"Bearer {exports.notion_token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def build_page(date: str, log_id: str, file_url: str):
    return {
        "parent": {"database_id": exports.notion_db_id},
        "properties": {
            "Logs": {
                "type": "files",
                "files": [
                    {
                        "type": "external",
                        "name": "Example file",
                        "external": {
                            "url": file_url
                        },
                    }
                ],
            },
            "Date": {
                "type": "rich_text",
                "rich_text": [
                    {
                        "type": "mention",
                        "mention": {
                            "type": "date",
                            "date": {
                                "start": date,
                            },
                        },
                    },
                ],
            },
            "Id": {
                "id": "title",
                "type": "title",
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": log_id,
                            "link": None,
                        },
                    }
                ],
            },
        },
    }


def get_table_data():
    # Get all items from the specified database
    url = f"https://api.notion.com/v1/databases/{exports.notion_db_id}/query"
    response = requests.post(url, headers=headers)
    print(response.status_code)
    with open("notion-response.json", "w") as notion_reponse:
        notion_reponse.write(response.text)


def create_a_page():
    url = "https://api.notion.com/v1/pages"
    s3_client = client('s3',region_name=exports.aws_region_name)
    logs_file_name = "logs.txt"
    with open(logs_file_name, "rb") as logs_file:
      upload_response = s3_client.upload_fileobj(logs_file, exports.s3_bucket_name , logs_file_name)
    
    file_url = f"https://{exports.s3_bucket_name}.s3.{exports.aws_region_name}.amazonaws.com/{logs_file_name}"
    body = build_page("2024-02-14", "some-weird-id",file_url)
    response = requests.post(url, data=json.dumps(body), headers=headers)
    print(response.text)
