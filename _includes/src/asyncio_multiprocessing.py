import asyncio
import subprocess
import random

semaphore = asyncio.Queue(maxsize=3-1)  # Max 3 processes

async def worker(id):
    delay = random.random()
    print('>'*5, f'task {id} starts with delay {delay:.1} seconds')
    process = await asyncio.create_subprocess_exec(
        'sleep', str(delay),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (output, err) = await process.communicate()
    status = await process.wait()

    print('<'*5, f'task {id} finished with status {status}')
    print(f'Stdout: {output}, Stderr: {err}')
    await semaphore.get()

async def main():
    for task_id in range(6):
        await semaphore.put(loop.create_task(worker(task_id)))

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
# wait for all tasks in the loop
loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
