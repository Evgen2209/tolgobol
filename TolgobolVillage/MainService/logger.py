import logging, os
from TolgobolVillage import settings
from django.core.handlers.wsgi import WSGIRequest
class Logger( object ):
    
    def __init__( self ):
        self.root_path = os.path.dirname( __file__ )
        self.log_path = os.path.join( settings.BASE_DIR, "mylog.log" )
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
    def get_user_args( args ):
        for i in args:
            if isinstance( i, WSGIRequest ):
                user = i.user
                if user.is_authenticated:
                    return f' [ user_id ] "{user.id}", {user.first_name} {user.last_name}, [ adres_id ] "{user.adres_id}" '
        else:
            if len( args ):
                h = args[0]
                if hasattr( h, 'request' ):
                    request = getattr( h, 'request' )
                    user = request.user
                    if user.is_authenticated:
                        return f' [ user_id ] "{user.id}", {user.first_name} {user.last_name}, [adres_id] "{user.adres_id}" '
        return ' [ user_id ] None '
    
    def get_user_kwargs( res ):
        view = res.get( 'view', None )
        if view:
            if hasattr( view, 'request' ):
                
                request = getattr( view, 'request' )
                user = request.user
                if user.is_authenticated:
                    return f' [ user_id ] "{user.id}", {user.first_name} {user.last_name}, [adres_id] "{user.adres_id}" '
        return ' [ user_id ] None '
            
            
    def wrap( *args, **kwargs ):
        Logger().Log( logging.INFO, func.__name__, '[pd][start]', get_user_args(args), args, kwargs)
        res = func( *args, **kwargs )
        Logger().Log( logging.INFO, func.__name__, '[pd][finish]', get_user_kwargs(res), res)
        return res
        
    return wrap
