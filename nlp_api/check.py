from fastapi import FastAPI, Form
import requests, json

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# 設定CORS中間件，以允許跨來源請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的前端來源
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)

# 替換成你的 API URL
api_url = "http://ml.hsueh.tw/callapi/"


# Call API
def call_api_check(messages):
    payload = {
        "engine": "gpt-35-turbo-16k",
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95,
        "top_k": 5,
        "roles": messages,
        "frequency_penalty": 0,
        "repetition_penalty": 1.03,
        "presence_penalty": 0,
        "stop": "",
        "past_messages": 0,
        "purpose": "dev",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    # 發送 POST 請求
    response = requests.post(api_url, json=payload, headers=headers)

    # 取得回應內容
    result = response.json()
    reply = result["choices"][0]["message"]["content"]
    return reply


# System Background
message_list = [
    {
        "role": "system",
        "content": f"你要判斷使用者輸入的訊息是否為有毒言論，如果是毒言論請回覆「是」，如果非有毒言論請回覆「否」，除此之外不須回覆其他訊息。",
    }
]


class Message(BaseModel):
    message: str


# Check Message
@app.post("/message/check")
def receive_message_from_chatroom(message: Message):
    message_list.append({"role": "user", "content": message.message})
    response_message = call_api_check(message_list)
    print(response_message)

    # Return Message to Frontend
    if response_message == "是":
        return False
    else:
        return True


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
