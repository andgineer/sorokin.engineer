import asyncio


async def f(name, timeout):
    await asyncio.sleep(timeout)
    print('hello', name)
    return name + ' done!'

async def main():
    bob = asyncio.create_task(f('bob', 0.3))  # start the coroutine
    alice = asyncio.create_task(f('alice', 0.1))  # start the coroutine

    # wait for coroutines to complete
    print(await bob)
    print(await alice)

asyncio.run(main())  # implicitly starts the loop
