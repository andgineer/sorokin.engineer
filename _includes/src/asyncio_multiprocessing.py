import asyncio
import subprocess
import random


semaphore = asyncio.Queue(maxsize=3)


async def worker(id):
    print('>'*10, id)
    process = await asyncio.create_subprocess_exec(
        'sleep', str(random.random()),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (output, err) = await process.communicate()
    status = await process.wait()

    print('<'*10, f'task {id} finished with status {status}')
    print(f'Stdout: {output}, Stderr: {err}')
    await semaphore.get()


async def main():
    for task_id in range(6):
        await semaphore.put(loop.create_task(worker(task_id)))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
