import logging, os

class Logger( object ):
    
    def __init__( self ):
        self.root_path = os.path.dirname( __file__ )
        self.log_path = os.path.join( self.root_path, "mylog.log" )
        self.log_level = logging.DEBUG
        #self.log_level = self.get_log_level()
        base_param = { "filename": self.log_path,
                      'level': self.log_level,
                      "filemode":'w',
                      "format":'%(asctime)s:%(msecs)d\t[%(process)d][%(thread)d][%(threadName)s]\t[%(levelname)s]\t%(message)s',
                      "datefmt":'%H:%M:%S'
                      }
        logging.basicConfig( **base_param )
    def __new__( cls ):
        if not hasattr( cls, 'instance'):
            cls.instance = super( Logger, cls ).__new__( cls )
        return cls.instance
    
    # def get_log_level( self ):
    #     try:
    #         import config
    #         level = config.Config().Get( 'Ядро.УровеньЛогирования', 'INFO' )
    #         if level == 'DEBUG':
    #             return logging.DEBUG
    #     except:
    #         self.Log( 'Ошибка импотра модуля config', logging.ERROR, exc_info=True )
    #     return logging.INFO
    
    def Log( self, log_level, *args, **kwargs ):
        print(log_level, 'log_level')
        msg = self._get_msg( *args )
        logging.log( log_level, msg, **kwargs )
    
    @staticmethod
    def _get_msg( *arg ):
        msg = ''
        for i in arg:
            msg += str(i) + ' '
        return msg



def INFO( *massage ):
    stack = traceback.extract_stack()
    parent = stack[2][2] if stack[2][2] != 'info' else ''
    line = stack[-3][-1]
    chaild_lene = line[6:line.find( '(' ) ]
    if chaild_lene.find( '=' ):
        chaild = chaild_lene[chaild_lene.find( '=' )+1:]
    else:
        chaild = chaild_lene
    chaild = '' if chaild == 'func' else chaild

    Logger().Log( logging.INFO, parent, ' / ', chaild,  *massage )
    
def WARNING( *massage ):
    stack = traceback.extract_stack()
    parent = stack[2][2] if stack[2][2] != 'info' else ''
    chaild = stack[-3][-1][6:stack[-3][-1].find('(')]
    chaild = '' if chaild == 'func' else chaild

    Logger().Log( logging.WARNING, parent, ' / ', chaild, log_level=logging.INFO, *massage )

def ERROR( *massage ):
    stack = traceback.extract_stack()
    parent = stack[2][2] if stack[2][2] != 'info' else ''
    chaild = stack[-3][-1][6:stack[-3][-1].find('(')]
    chaild = '' if chaild == 'func' else chaild

    Logger().Log( logging.ERROR, parent, ' / ', chaild, log_level=logging.INFO, *massage )

def EXCEPT( *massage ):
    stack = traceback.extract_stack()
    parent = stack[2][2] if stack[2][2] != 'info' else ''
    chaild = stack[-3][-1][6:stack[-3][-1].find('(')]
    chaild = '' if chaild == 'func' else chaild

    Logger().Log( logging.ERROR, parent, ' / ', chaild, log_level=logging.INFO, *massage, exc_info=True )

def DEBUG( *massage ):
    stack = traceback.extract_stack()
    parent = stack[2][2] if stack[2][2] != 'info' else ''
    chaild = stack[-3][-1][6:stack[-3][-1].find('(')]
    chaild = '' if chaild == 'func' else chaild

    Logger().Log( logging.DEBUG, parent, ' / ', chaild, *massage )
    
import traceback


def logger( func, *args, **kwargs ):
    
    def wrap( *args, **kwargs ):
        Logger().Log( logging.INFO, func.__name__, '[pd][start]', args, kwargs)
        stack = traceback.extract_stack()
        #log([i for i in stack[-2]],stack[-2][-1], stack[1][2])
        res = func( *args, **kwargs )
        Logger().Log( logging.INFO, func.__name__, '[pd][finish]', res)
        return res
        
    return wrap