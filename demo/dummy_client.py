import asyncio
import json
import pickle
import time

import websockets

URL = "ws://localhost:8848/ws"
OUTPUT_FILE = "output.pkl"


async def websocket_client():
    uri = URL
    output_list = []

    async with websockets.connect(uri) as websocket:
        # 接收服务器的初始化消息
        init_response = await websocket.recv()
        print(f"Received initial message: {init_response}")
        init_response = json.loads(init_response)

        # 发送初始化响应
        await websocket.send(
            json.dumps(
                {
                    "type": "query",
                    "query": init_response["data"]["query"],
                }
            )
        )

        while True:
            response = await websocket.recv()
            timestamp = time.time()

            try:
                content = json.loads(response)
                recorded_data = {"time": timestamp, "content": content}
                if content.get("type") == "finish":
                    break
                output_list.append(recorded_data)
            except json.JSONDecodeError:
                print("Received message is not a valid JSON")

    with open(OUTPUT_FILE, "wb") as f:
        pickle.dump(output_list, f)


asyncio.run(websocket_client())
