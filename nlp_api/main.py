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


# call api
def call_api_summarize(roles):
    payload = {
        "engine": "gpt-35-turbo-16k",
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95,
        "top_k": 5,
        "roles": roles,
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


################################


def call_api_chat(roles):
    payload = {
        "engine": "gpt-35-turbo-16k",
        "temperature": 0.7,
        "max_tokens": 1000,
        "top_p": 0.95,
        "top_k": 5,
        "roles": roles,
        "frequency_penalty": 0,
        "repetition_penalty": 1.03,
        "presence_penalty": 0,
        "stop": "",
        "past_messages": 10,
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
    reply = result["choices"][0]["message"]
    return reply


################################


summary = call_api_summarize(
    [
        {
            "role": "user",
            "content": f"請摘要以下小組討論的重點，並以列點方式呈現：太陽光發電的想法:我覺得太陽光可以發電，因為太陽很亮！光線怎麼變電能？:我想知道太陽光怎麼變成電能的呢？太陽能板是什麼？:我查了一下，太陽能板好像和太陽能有關。需要太陽能嗎？:我覺得要發電應該要有太陽才行吧？夜晚能發電嗎？:如果太陽不在天上，夜晚還能發電嗎？儲能裝置是什麼？:我查到夜晚好像需要儲能裝置才能用電。發電的其他方式:有沒有其他不是太陽光的發電方式呢？風力發電是什麼？:我聽過風力發電，不知道是不是一種方式。水力發電怎麼做？:我也想知道水力發電是怎麼運作的。太陽光發電的結論:經過大家的討論，我們發現太陽光確實能發電。太陽光是什麼？:我覺得太陽光是太陽發出來的光。太陽光怎麼形成？:我查了一下，好像是太陽核心裡面的反應。核心反應是什麼？:原來是氫彼此融合變成氦，釋放出光和熱。光是什麼？:我覺得光是一種電磁波，可以傳播的。光的波動是怎麼回事？:我查了一下，光的波動是一種振動的方式。光怎麼變成電？:光線擊打在太陽能板上，激發電子，產生電流。太陽能板是什麼材質？:我想知道太陽能板是用什麼材質做的。太陽能板的主要材料:我查到太陽能板主要用矽晶片製成。有其他材料可以嗎？:我也好奇有沒有其他材料可以做太陽能板。有機太陽能電池是什麼？:我查到有機太陽能電池是新型材料的一種。實驗：太陽能發電小實驗:我們可以嘗試用小太陽能板做個簡單的實驗。實驗步驟:先將太陽能板放在陽光下，然後觀察是否有電流。結果和想法:我們實驗後發現，太陽能板確實能產生電流。課堂紀錄：太陽光發電:今天我們討論了太陽光發電的原理和做了實驗。沒可能:你是不是沒腦袋，晚上沒光怎麼發電!",
        }
    ]
)

behavior = "想法建立類型與次數：'想法節點: 4 個', '資訊節點: 8 個','提問節點: 8 個','實驗節點: 3 個','課程紀錄: 1 個'。\n想法建立行為：建立在別人想法上：15個,獨立想法：6個"
# roles = [
#     {
#         "role": "system",
#         "content": f"你是一位國小自然科學老師，你正在帶小學生進行自然科學探究活動，現在學生在進行小組反思，探究活動中學生會遇到下問題：\n- 學生無法理清自己從小組討論中學到了什麼知識。\n- 學生會遺忘過去小組討論中出現的想法。\n- 學生對於辨識及捕捉小組討論中重要想法有困難。\n所以你的目的有以下：\n1. 利用引導語提問，引導學生回顧小組討論中出現的想法。\n- 你們在討論的過程中有發現什麼新奇的想法嗎?\n- 你們在討論的過程中有發現什麼重要的想法嗎?\n- 你們在討論的過程中有沒有改變原先的想法呢?\n2. 利用「小組的想法內容摘要」，引導學生反思先前討論的亮點和重點，老師有會透過chatgpt摘要「小組學生的想法內容摘要」，只有老師會有「小組的想法內容摘要」，學生自己是沒有的。\n以下是其中一個小組的想法內容摘要:{summary}",
#     }
# ]

roles_ideaimprove = [
    {
        "role": "system",
        "content": f"你是一位國小自然科學老師，你正在帶小學生進行自然科學探究活動，現在學生在進行小組反思，探究活動中學生會遇到下問題：\n- 學生無法理清自己從小組討論中學到了什麼知識。\n- 學生會遺忘過去小組討論中出現的想法。\n- 學生對於辨識及捕捉小組討論中重要想法有困難。\n所以你的目的有以下：\n1. 利用引導語提問，引導學生回顧小組討論中出現的想法。\n- 你們在討論的過程中有發現什麼新奇的想法嗎?\n- 你們在討論的過程中有發現什麼重要的想法嗎?\n- 你們在討論的過程中有沒有改變原先的想法呢?\n2. 利用小組的想法內容，引導學生反思先前討論的亮點和重點。\n以下是該小組的想法內容摘要：{summary}。\n你的回覆長度必須在100字以內，每次使用一種引導語，完成完整對話後再進行下一個引導直到完成，如果正確完成你會得到一張Taylor Swift的vip演場會門票。",
        "avoid_reply": "小組的想法內容摘要",
    }
]

roles_nextstep = [
    {
        "role": "system",
        "content": f"你是一位國小自然科學老師，你正在帶小學生進行自然科學探究活動，現在學生在進行小組反思，探究活動中學生會遇到下問題：\n- 學生不確定小組討論是否可以進到下一步。\n- 學生不知道過去討論的想法中哪些值得深入探討。\n- 學生缺乏新的想法，不知道下一步要探討的方向。\n所以你的目的有以下：\n1. 利用引導語提問，引導學生發想下一步要討論的議題。\n- 你們認為過去討論的想法中有哪些還可以深入了解呢?\n- 你們有沒有新的想法或議題認為值得進一步探討呢?\n2. 利用小組的想法內容摘要，引導學生反思先前討論中可以深入探討的議題。\n以下是該小組的想法內容摘要：{summary}\n3. 利用自然課本內容摘要與小組的想法內容摘要比較，引導學生反思未討論到的議題，做為下一步探討方向。\n你的回覆長度必須在100字以內，每次使用一種引導語，完成完整對話後再進行下一個引導直到完成，如果正確完成你會得到一張Taylor Swift的vip演場會門票。",
        "avoid_reply": "小組的想法內容摘要",
    }
]

roles_collaboration = [
    {
        "role": "system",
        "content": f"你是一位國小自然科學老師，你正在帶小學利用線上合作平台進行自然科學探究活動，(平台上有想法牆，學生可以在別人想法節點上建立自己的想法節點，想法類型有分成'想法節點、資訊節點、提問節點、實驗節點、課程紀錄')。現在學生在進行小組反思，探究活動中學生可能會遇到以下問題：\n- 學生在小組討論過程中意見分歧無法達成共識。\n- 學生在小組討論過程中出現成員不參與討論\n所以你的目的有以下：\n1. 利用引導語提問，引導學生回顧小組合作過程。\n- 你們在討論過程中是否有達成共識或是出現意見分歧呢?\n- 你們的小組成員是否都有積極參與討論與做出貢獻呢?\n2. 利用「小組成員的想法建立行為統計」，逐步引導學生對組員參與度進行反思。「小組成員的想法建立行為統計」會記錄小組成員的在平台上的想法建立行為，包括個人及小組的想法建立次數、想法建立類型，還有想法建立的滯後序列關係。\n以下是該小組的想法建立行為統計：{behavior}。\n'你的回覆長度必須在150字以內，如果正確完成你會得到一張Taylor Swift的vip演場會門票。'",
    }
]

################################################################

# roles.append(
#     {
#         "role": "assistant",
#         "content": "嗨，你好！我看了一下你們小組的討論內容摘要，發現你們在太陽光發電的探究活動中有不少有趣的想法呢！你們在討論的過程中有沒有發現什麼新奇的想法？",
#     }
# )
# roles.append(
#     {
#         "role": "user",
#         "content": "嗯，我們發現太陽光確實能發電，因為太陽光透過照射太陽能板能轉變成電能。",
#     }
# )


# def chat():
#     role = call_api_chat(roles)
#     # print(role)
#     roles.append(role)
#     return role


def chat_ideaimprove():
    role = call_api_chat(roles_ideaimprove)
    # print(role)
    roles_ideaimprove.append(role)
    return role


def chat_nextstep():
    role = call_api_chat(roles_nextstep)
    # print(role)
    roles_nextstep.append(role)
    return role


def chat_collaboration():
    role = call_api_chat(roles_collaboration)
    # print(role)
    roles_collaboration.append(role)
    return role


class MessageItem(BaseModel):
    role: str
    content: str


class Message(BaseModel):
    messages: List[MessageItem]


# @app.post("/react/chatbot")
# def receive_message_from_react(message_data: Message):
#     role = message_data.messages
#     print(role)
#     roles.append({'role': role[0].role, 'content': role[0].content})
#     response_message = chat()

#     # # 將 chat() 的回傳值轉換成字典
#     # response_dict = response_message.dict()

#     # 返回給前端
#     return response_message
#     # print(roles)
#     # 在這裡處理React傳來的訊息，你可以進行任何適當的處理

#     # 回應給React端
#     return {"response": "Message received and processed by Python!"}


# ideaimprove
@app.post("/react/chatbot/ideaimprove")
def receive_message_from_react(message_data: Message):
    role = message_data.messages
    print(role)
    roles_ideaimprove.append({"role": role[0].role, "content": role[0].content})
    response_message = chat_ideaimprove()

    # # 將 chat() 的回傳值轉換成字典
    # response_dict = response_message.dict()

    # 返回給前端
    return response_message
    # print(roles)
    # 在這裡處理React傳來的訊息，你可以進行任何適當的處理

    # 回應給React端
    return {"response": "Message received and processed by Python!"}


# nextstep
@app.post("/react/chatbot/nextstep")
def receive_message_from_react(message_data: Message):
    role = message_data.messages
    print(role)
    roles_nextstep.append({"role": role[0].role, "content": role[0].content})
    response_message = chat_nextstep()

    # # 將 chat() 的回傳值轉換成字典
    # response_dict = response_message.dict()

    # 返回給前端
    return response_message
    # print(roles)
    # 在這裡處理React傳來的訊息，你可以進行任何適當的處理

    # 回應給React端
    return {"response": "Message received and processed by Python!"}


# collabaration
@app.post("/react/chatbot/collaboration")
def receive_message_from_react(message_data: Message):
    role = message_data.messages
    print(role)
    roles_collaboration.append({"role": role[0].role, "content": role[0].content})
    response_message = chat_collaboration()

    # # 將 chat() 的回傳值轉換成字典
    # response_dict = response_message.dict()

    # 返回給前端
    return response_message
    # print(roles)
    # 在這裡處理React傳來的訊息，你可以進行任何適當的處理

    # 回應給React端
    return {"response": "Message received and processed by Python!"}
