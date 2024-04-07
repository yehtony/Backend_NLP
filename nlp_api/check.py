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
        "temperature": 0,
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


# # System Background
# message_system = [
#     {
#         "role": "system",
#         "content": f"你要依序檢查學生輸入的訊息是否包含以下三種情況，並依編號順序輸出三種檢查結果：1.訊息是否包含冒犯性言論，如果包含冒犯性言論請回覆「是」，並加上訊息中偵測到的冒犯性詞語；如果無包含冒犯性言論請回覆「否」。2.訊息是否包含負面情緒，如果包含負面情緒請回覆「是」，並用加上可修正成的相似正面訊息；如果無包含負面情緒請回覆「否」。3.學生回覆內容與提問內容是否有關聯性，如果有關聯性請回覆「是」，如果無關聯性請回覆「否」。回覆僅包含以上三種檢查結果，除此之外不回覆其他訊息。",
#     }
# ]


# System Background
message_system = [
    {
        "role": "system",
        "content": "你要依序檢查學生輸入的訊息是否包含以下三種情況，並依編號順序輸出三種檢查結果：1.訊息是否包含冒犯性言論，如果包含冒犯性言論請回覆「是」，並用'：'加上訊息中偵測到的冒犯性詞語；如果無包含冒犯性言論請回覆「否」。2.訊息是否包含負面情緒，如果包含負面情緒請回覆「是」，並用'：'加上建議修正負面情緒後的訊息；如果無包含負面情緒請回覆「否」。3.學生回覆內容與提問內容是否有關聯性，如果有關聯性請回覆「是」，如果無關聯性請回覆「否」。回覆僅包含以上三種檢查結果，三種結果用'\\n'分隔，除此之外不回覆其他訊息。\n以下是提問內容：「哈囉各位同學，你們討論過程中有遇到什麼問題需要進行 Meta-Talk 嗎？如果有，你們可以先進行討論，並把目前的想法或遇到的問題在聊天室提出來！或是老師有指定需要你們進行哪一種 Meta-Talk呢？（想法收斂、小組合作）。」",
    },
    {
        "role": "user",
        "content": "學生回覆內容：「我有點失望，感覺我們這組就是在浪費時間，討論根本就是一團糟。一群廢物都沒在做事情，好像討論都不關他們的事情一樣！ 」",
    },
    {
        "role": "assistant",
        "content": "是：廢物。\n是：我有些感到挫折，因為我們這組的討論進展得很緩慢，我們似乎無法有效地達成共識。\n是",
    },
]

message_list = message_system

# message_assistant = [
#     {
#         "role": "assistant",
#         "content": f"哈囉各位同學，你們討論過程中有遇到什麼問題需要進行 Meta-Talk 嗎？如果有，你們可以先進行討論，並把目前的想法或遇到的問題在聊天室提出來！或是老師有指定需要你們進行哪一種 Meta-Talk呢？（想法收斂、小組合作）",
#     }
# ]
# message_question_00 = "提問內容：「哈囉各位同學，你們討論過程中有遇到什麼問題需要進行 Meta-Talk 嗎？如果有，你們可以先進行討論，並把目前的想法或遇到的問題在聊天室提出來！或是老師有指定需要你們進行哪一種 Meta-Talk呢？（想法收斂、小組合作）。」\n"


class Message(BaseModel):
    message: str


# Check Message
@app.post("/message/check")
def receive_message_from_chatroom(message: Message):
    messages = message_system
    messages.append({"role": "user", "content": message.message})
    response_message = call_api_check(messages)
    # print(response_message)

    # # Return Message to Frontend
    # if response_message == "是":
    #     return False
    # else:
    #     return True

    lines = response_message.strip().split("\n")

    # 创建一个空列表，用于存储字典
    records = []
    # 遍历每一行数据
    for line in lines:
        # 使用冒号（：）分割每一行数据
        parts = line.split("：")
        if len(parts) == 2:
            records.append({"result": parts[0], "content": parts[1]})
        else:
            records.append({"result": line, "content": ""})

    # 输出记录
    print(records)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
