import logging
from io import StringIO

logger = logging.getLogger('course.executor')

def execute(job_id):
    logger.info('started job=%s', job_id)
    logger.info('finished job=%s code=%s', job_id, 0)
    return 0

def test_logging():
    stream = StringIO()
    handler = logging.StreamHandler(stream)
    previous = logger.level
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    try:
        assert execute('job-1') == 0
        text = stream.getvalue()
        assert text.count('job-1') == 2
    finally:
        logger.removeHandler(handler)
        handler.close()
        logger.setLevel(previous)

if __name__ == '__main__':
    test_logging()
    print('correlated log events verified')
