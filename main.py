import asyncio
import time
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class TestResponse(BaseModel):
    elapsed: float

# task_queue = asyncio.Queue()
lock = asyncio.Lock()
time_list = []

async def work() -> None:
    await asyncio.sleep(3)

"""В закоментированной части очередь. С ее помощью можно избавиться от глобальной переменнйой time_list.
    Но тогда выводит не верный результат, хотя выполняется последовательно, из-за того что считает время от поступившего запроса до выполнения.
    И если вести отсчет от первого поступившего запроса, результат будет верный. Я высчитывал через вывод переменных ts1 и ts2.
    Покрайней мере на момент сдачи других идей мне в голову не пришло"""

@app.get('/test', response_model=TestResponse)
async def handler():       
    ts1 = time.monotonic()
    global time_list
    time_list.append(ts1) 
    # await task_queue.put((ts1,work))
    async with lock:
        # task = await task_queue.get()
        await work()  
        ts1 = time_list[0]
        time_list.pop(-1)
        ts2 = time.monotonic()
        return TestResponse(elapsed=ts2 - ts1)


