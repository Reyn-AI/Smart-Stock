import websocket
from src.utils.backtrader_constant import DEFAULT_PARAMS

def test_websocket():
    url = "ws://0.0.0.0:38888/backtrade/start/"
    ws = websocket.WebSocket()
    ws.connect(url)
    print("已连接到服务器")
    # 发送消息到服务器
    params = str(DEFAULT_PARAMS)
    ws.send(params)
    res = ws.recv()
    print(res)
    # # 接收服务器发送的消息
    # message = websocket.recv()
    # print(f"接收到消息：{message}")

    # # 关闭连接
    # websocket.close()
    print("连接已关闭")

test_websocket()