import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def is_empty(self):
        return not self._queue

    def size(self):
        return len(self._queue)

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        if self.is_empty():
            raise Exception('Priority queue is empty')
        popped = heapq.heappop(self._queue)
        return popped[-1], -popped[0]  # return item, priority
