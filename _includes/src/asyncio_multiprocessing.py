import asyncio
import subprocess
import random

semaphore = asyncio.Queue(maxsize=3-1)  # Max 3 processes


async def worker(id):
    """
    We could use more straightforward consumer-producer pattern:
        * producer puts tasks into the queue
        * worker waits for tasks in the queue

    But for this tiny code sniped that would produce too much boilerplates.
    """
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


async def main(loop):
    for task_id in range(6):
        await semaphore.put(task_id)  # It does'n matter what we put in the queue. We use it as semaphore.
        loop.create_task(worker(task_id))
    # all the tasks are scheduled at the moment but not all done

loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))  # Wait for all tasks in the loop.
