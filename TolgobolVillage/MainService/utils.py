import pathlib, os
import uuid
from django.utils import timezone
from .models import FileTmp
from TolgobolVillage import settings
def get_file_ext( name ):
   ext = pathlib.Path( name ).suffixes
   res = ''
   for i in ext:
      res += i
   return res

class TmpFileStorage:
    
    storage = FileTmp
    file_rut = os.path.join( settings.MEDIA_ROOT, 'tmp' )
    
    @classmethod
    def get_tmp_folder( cls, user_id ):
        
        date_start = timezone.now()
        folder_tmp = date_start.strftime( '%d-%m-%Y' )
        
        return os.path.join( cls.file_rut, folder_tmp, str(user_id) )
    
    @classmethod
    def save_file( cls, path ):
        name = os.path.basename( path )
        date = timezone.now()
        fil = cls.storage.objects.create( file_name=name,
                                    tmp_name=name,
                                    tmp_path=str(path),
                                    size=os.path.getsize(path), 
                                    date_start=date, 
                                    date_finish=date )
        return os.path.relpath( path, settings.MEDIA_ROOT )
    
    @classmethod
    def start_upload( cls, file_name, size, user ):
        uid = str(uuid.uuid4())
        tmp_file_name = uid + get_file_ext( file_name ) 
        date_start = timezone.now()
        folder_tmp = date_start.strftime( '%d-%m-%Y' )
        tmp_current_folder = os.path.join( cls.file_rut, folder_tmp, str(user.id) ) 
        if not os.path.exists( tmp_current_folder ):
            os.makedirs(tmp_current_folder)
        tmp_path = os.path.join( tmp_current_folder, tmp_file_name ) 
        if os.path.exists( tmp_path ):
            return None
        open( tmp_path, 'wb+' ).close()
        cls.storage.objects.create( file_name=file_name,
                                    tmp_name=tmp_file_name,
                                    tmp_path=tmp_path,
                                    size=size, 
                                    date_start=date_start )
        return tmp_file_name
    
    @classmethod
    def upload( cls, tmp_name, strim ):
        try:
            file = cls.storage.objects.get( tmp_name=tmp_name )
            with open(file.tmp_path, 'ab+') as f: 
                f.write(strim)
        except:
            pass

    @classmethod
    def finish_upload( cls, tmp_name ):
        file = cls.storage.objects.get( tmp_name=tmp_name )
        file.date_finish = timezone.now()
        file.save()
        return file.id

    @classmethod
    def cancel_upload( cls, tmp_name ):
        file = cls.storage.objects.get( tmp_name=tmp_name )
        os.remove( file.tmp_path )
        file.delete()



