#!/user/bin/env python3
# -*- coding: utf-8 -*-


import time


class TimedSet(set):
    def __init__(self):
        self.__table = {}

    def add(self, item, timeout=1):
        self.__table[item] = time.time() + timeout
        set.add(self, item)
        print(self.__table)

    def __contains__(self, item):
        if self.__table.get(item):
            return time.time() < self.__table.get(item)

    def __iter__(self):
        for item in set.__iter__(self):
            print(f'item: {item}')
            if time.time() < self.__table.get(item):
                yield item


if __name__ == '__main__':
    t_set = TimedSet()
    t_set.add('a', 0.6)
    time.sleep(0.7)
    print('a' in t_set)

    time.sleep(0.6)
    print('a' in t_set)

    t_set.add('sdsag时间 ', 0.3)
    t_set.add('y', 0.4)
    t_set.add('z', 0.5)
    time.sleep(0.35)
    if "sdsag时间 " in t_set:
        print(1)
    if "y" in t_set:
        print(2)
    # for item in t_set:
    #     print(item)
