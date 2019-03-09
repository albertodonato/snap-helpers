import logging


def setup_log(logfile):
    logging.basicConfig(
        filename=str(logfile),
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)
