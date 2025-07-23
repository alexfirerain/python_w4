import asyncio
import time


# эвэйт приостанавливает выполнение корутины (т.е асинхронные функции)
# гэзэ собирает все корутины в один поток и выполняет их в порядке очереди


async def say_hello():
    await asyncio.sleep(1)
    print("Hello")

async def say_goodby():
    await asyncio.sleep(2)
    print('Goodby')


async def main():
    await asyncio.gather(say_hello(), say_goodby())


asyncio.run(main())

# ботов писать — сразу асинхронно давай (см. ссылку)