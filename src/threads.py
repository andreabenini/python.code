# Version 1
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()
for i in range(num_worker_threads):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

for item in source():
    q.put(item)

q.join()       # block until all tasks are done


# Version 2
import threading
threadStop = False
threadID = threading.Thread(target=threadFunction)
threadID.start()

def threadFunction():
    while not threadStop:
        print('.', end='')
        time.sleep(1)
