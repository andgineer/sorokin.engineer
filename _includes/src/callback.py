import asyncio


async def f(name, timeout, on_result):
    await asyncio.sleep(timeout)
    print('hello', name)
    on_result(name + ' done!')


def on_result(msg):
    print(msg)


async def main():
    bob = asyncio.create_task(f('bob', 0.3, on_result))  # start the coroutine
    alice = asyncio.create_task(f('alice', 0.1, on_result))  # start the coroutine

    # wait for coroutines to complete
    await bob
    await alice

asyncio.run(main())  # implicitly starts the loop

