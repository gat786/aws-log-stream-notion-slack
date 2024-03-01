import exports
import requests
import json
from boto3 import client
import time
from typing import List

headers = {
    "Authorization": f"Bearer {exports.notion_token}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}


def build_page(date: str, log_id: str, list_page_content_strings: List[str]):
    
    children = []
    for item in list_page_content_strings:
        children.append({
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": item
                            },
                        }
                    ]
                },
            }
        )
    return {
        "parent": {"database_id": exports.notion_db_id},
        "properties": {
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
        "children": children,
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
        
    id = int(time.time())
    log_lines = []
    
    with open("logs.txt", "r") as logs_content:
        log_lines = logs_content.readlines()
    
    body = build_page(
        date = "2024-02-14",
        log_id = f"{id}", 
        list_page_content_strings = log_lines
    )
    response = requests.post(url, data=json.dumps(body), headers=headers)
    print(response.text)
