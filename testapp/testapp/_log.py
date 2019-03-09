import logging


def setup_log(log_dir):
    logfile = log_dir / 'hooks.log'
    logging.basicConfig(
        filename=str(logfile),
        filemode='a',
        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
        datefmt='%H:%M:%S',
        level=logging.DEBUG)
