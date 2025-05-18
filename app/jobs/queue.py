from fastapi import BackgroundTasks
from typing import Callable, Dict, Any

class JobQueue:
    def __init__(self, background_tasks: BackgroundTasks):
        self.background_tasks = background_tasks
    
    def dispatch(self, job: Callable, *args, **kwargs):
        self.background_tasks.add_task(job, *args, **kwargs)