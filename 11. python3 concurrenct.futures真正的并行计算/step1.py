import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def blocking_cpu():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 2))

async def main():
    loop = asyncio.get_event_loop()
    ## pool = ProcessPoolExecutor(max_workers = 4)
    pool = ThreadPoolExecutor(max_workers = 4)
    result = await loop.run_in_executor(pool, cpu_bound)
    print(result) ## 328350

asyncio.run(main())
