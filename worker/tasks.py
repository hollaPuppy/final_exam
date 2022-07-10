from worker_config import worker_cel

@worker_cel.task(name='hello.task')
def hello_world():
    print('hello world')