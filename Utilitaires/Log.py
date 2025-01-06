import logging
import logging.config
from datetime import datetime

def loggerInit(parser = None):
    args, unknown = parser.parse_known_args()
    
    
    date : str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.config.fileConfig('config/logging.conf', defaults={'date':date, 'logConsole':args.logConsole ,'logFile':args.logFile})
    
    # create logger
    logger = logging.getLogger('__name__')
    return logger
