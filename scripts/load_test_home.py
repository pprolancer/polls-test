import time
from threading import Thread

import datetime
import random
import logging
import requests

from polls.models import Question


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class Caller(object):

    @staticmethod
    def call(path):
        path_dict = {'home': '/', 'not_found': '/polls/not_found/', 'error': '/polls/error/'}
        fragment = path_dict[path]
        url = 'http://polls.raajakshar.com' + fragment
        response = requests.get(url)


class UrlThread(Thread):

    def __init__(self, num_times, path):
        self.num_times = num_times
        self.path = path
        super(UrlThread, self).__init__()

    def run(self):
        start = datetime.datetime.now()
        logger.info("Start: {}".format(start,))
        for i in range(self.num_times):
            Caller.call(self.path)
        end = datetime.datetime.now()
        logger.info("End: {}".format(end,))


def invoke_url(num_threads, num_times, path='home'):
    """
    This mimics num_thread concurrent connections.

    Thus when one connection is being processed, other connection would be waiting in queue.

    Also, a connection would make num_times requests. Thus we can notice some continuous requests and see how the load increases.
    :return:
    """

    threads = []
    start = time.time()
    for _ in range(num_threads):
        t = UrlThread(num_times, path)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    end = time.time()
    logger.info("Took {} seconds".format(end - start))


if __name__ == '__main__':
    invoke_url(1, 1)
