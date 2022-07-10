from ..api import worker

@worker.task(name='test')
def test_task():
    print('hello world')