# SuperFastPython.com
# example of executing a target task function in a separate thread
from time import sleep
from threading import Thread
 
# a simple task that blocks for a moment and prints a message
def task():
    # block for a moment
    sleep(2)
    # display a message
    print('This is coming from another thread')
 
# create and configure a new thread to run a function
thread = Thread(target=task)
# start the task in a new thread
thread.start()
# display a message
print('Waiting for the new thread to finish...')
# wait for the task to complete
# thread.join()
print('Check if waiting for finish or not')
