import logging
log_level = None
logger = logging.getLogger('qa_automation')
hdlr = logging.FileHandler('./qa_automation.log')
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)

def set_log_level(ll='debug'):
    global log_level
    log_level = ll

    if not log_level or 'error' in log_level:
        log_level = logging.ERROR
    elif 'info' in log_level:
        log_level = logging.INFO
    elif 'warning' in log_level:
        log_level = logging.WARNING
    elif 'debug' in log_level:
        log_level = logging.DEBUG
    logger.setLevel(log_level)
    return log_level

def log_force(msg):
    ''' Log and print msg regardless of log level
    '''
    if log_level != logging.ERROR and log_level != logging.DEBUG:
        print msg
    logger.setLevel(logging.DEBUG) # Override debug level to be able to log all
    logger.info(msg)
    logger.setLevel(log_level) # Restore original level
