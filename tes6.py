#!/user/bin/env python3
# -*- coding: utf-8 -*-
import time
from queue import Queue

# 设置队列长度为1
que = Queue(maxsize=100)


# 此时如果入队列两次, put将会一直堵塞，等待前一个出队列

def the_put():
    while True:
        print(que)
        que.put(1)
        print(que.qsize())
        time.sleep(1)


if __name__ == '__main__':
    the_put()
