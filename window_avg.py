import collections
import datetime
import unittest

"""
follow-up:
如果同一时刻到了很多：可以在deque里面分block存储，按照时间，这样清理的时候按照block清理就可以了，
时间复杂度降低为1000/n（n个block）

起一个thread 去access用一个data structure是没有意义的，即使加了lock还是single tread的效果；
一台机器的话，有几个core，可以起几个thread，每个都放一个这个数据结构的copy；
根据key进行sharding，判断数据放在哪个core上；
然后再考虑scale到多台机器，也是根据key进行sharding；
再根据每个方法进行具体分析。

"""
class Event:
    def __init__(self, key, timestamp):
        self.key = key
        self.timestamp = timestamp


class Window:
    def __init__(self):
        # put event in window
        self.window = collections.deque()
        self.key_to_value = collections.defaultdict()

        self.count = 0
        self.total = 0

    def get(self, key):
        self.clean()
        # get from hashmap
        if key not in self.key_to_value:
            raise Exception("Invalid input: key not exist")

        return self.key_to_value

    def put(self, key, value, timestamp):
        if key not in self.key_to_value:
            new_event = Event(key, timestamp)
            self.window.append(new_event)
            self.key_to_value[key] = value
            self.count += 1
            self.total += value

            self.clean()
            return True
        else:

            self.clean()
            return False

    def get_avg(self):
        self.clean()
        if self.count == 0:
            raise Exception("Invalid operation")
        return self.total / self.count

    def clean(self):
        """
        remove expired events
        :return:
        """
        cur_time = datetime.datetime.now.timestamp()
        while self.deque and (cur_time - self.deque[0].timestamp) >= 5 * 60:
            popped_event = self.deque.popleft()
            self.count -= 1
            self.total -= self.key_to_value[popped_event.key]
            del self.key_to_value[popped_event]


class MyTestCase(unittest.TestCase):
    def test_window_avg(self):
        window = Window()
        pass
