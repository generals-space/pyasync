import asyncio
from datetime import datetime, timezone
import logging

def utc_now():
    # utcnow returns a naive datetime, so we have to set the timezone manually <sigh>
    return datetime.utcnow().replace(tzinfo=timezone.utc)

class Terminator:
    pass

class AsyncPool:
    def __init__(self, loop, num_workers: int, worker_co, 
                 job_accept_duration: int = None, max_task_time: int = None, 
                 raise_on_join: bool = False):
        """
        This class will create `num_workers` asyncio tasks to work against a queue of
        `num_workers` items of back-pressure (IOW we will block after such
        number of items of work is in the queue).  `worker_co` will be called
        against each item retrieved from the queue. If any exceptions are raised out of
        worker_co, self.exceptions will be set to True.
        @param loop: asyncio loop to use
        @param num_workers: number of async tasks which will pull from the internal queue
        @param worker_co: async coroutine to call when an item is retrieved from the queue
        @param job_accept_duration: maximum number of seconds from first push to last push before a TimeoutError will be thrown.
                Set to None for no limit.  Note this does not get reset on aenter/aexit.
        @param max_task_time: maximum time allowed for each task before a CancelledError is raised in the task.
            Set to None for no limit.
        @return: instance of AsyncWorkerPool
        """
        loop = loop or asyncio.get_event_loop()
        self._loop = loop
        self._num_workers = num_workers
        ## 参数队列, 也即任务队列.
        self._task_queue = asyncio.Queue()
        self._workers = None
        self._job_accept_duration = job_accept_duration
        self._first_push_dt = None
        self._max_task_time = max_task_time
        self._worker_co = worker_co

    async def _worker_loop(self):
        while True:
            got_obj = False
            try:
                item = await self._task_queue.get()
                got_obj = True

                if item.__class__ is Terminator:
                    break

                args, kwargs = item
                # the wait_for will cancel the task (task sees CancelledError) and raises a TimeoutError from here
                # so be wary of catching TimeoutErrors in this loop
                await asyncio.wait_for(self._worker_co(*args, **kwargs), self._max_task_time, loop=self._loop)

            except (KeyboardInterrupt, MemoryError, SystemExit) as e:
                print(e)
            except BaseException as e:
                print('Worker call failed: ', e)
            finally:
                if got_obj:
                    self._task_queue.task_done()

    async def push(self, *args, **kwargs) -> asyncio.Future:
        ''' 
        把任务函数所需的参数推送给工作协程
        :param args: position arguments to be passed to `worker_co`
        :param kwargs: keyword arguments to be passed to `worker_co`
        :return: future of result 
        '''
        if self._first_push_dt is None:
            self._first_push_dt = utc_now()

        if self._job_accept_duration is not None and (utc_now() - self._first_push_dt) > self._job_accept_duration:
            raise TimeoutError("Maximum lifetime of {} seconds of AsyncWorkerPool exceeded".format(self._job_accept_duration))

        await self._task_queue.put((args, kwargs))

    def start(self):
        '''
        启动worker pool, 重设exception state
        '''
        assert self._workers is None
        ## 创建_num_workers个工作协程
        self._workers = [asyncio.ensure_future(self._worker_loop(), loop=self._loop) for _ in range(self._num_workers)]

    async def join(self):
        if not self._workers: return

        # The Terminators will kick each worker 
        # from being blocked against the _task_queue.get() 
        # and allow each one to exit
        for _ in range(self._num_workers):
            await self._task_queue.put(Terminator())

        try:
            await asyncio.gather(*self._workers, loop=self._loop)
            self._workers = None
        except Exception as e:
            print('Exception joining ', e)
            raise
