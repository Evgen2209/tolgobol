from datetime import date, datetime
import sqlite3


a = { 
     "Успенская": [
                    "1",
                    "2А",
                    "2б",
                    "3",
                    "4",
                    "5",
                    "7"
                    ],
     "Тихвинская" : [
        "1",
        "2",
        "3",
        "4",
        "5а",
        "8",
        "8а",
        "9",
        "9б",
        "10",
        "11",
        "24",
     ],
     "Запрудная": [
                 "1",
                "2",
                "3",
     ],
     "Петропавловская": [
                        "2",
                        "3",
                        "4",
                        "5",
                        "5а",
                        "6",
                        "7",
                        "7а",
                        "8",
                        "9",
                        "10",
                        "11",
                        "14",
                        "14а",
                        "15",
                        "16",
                        "17",
                        "19",
                        "20",
                        "21",
                        "21А",
                        "22",
                        "23",
                        "25",
                        "27",
                        "29",
                        "29 стр. 1",
                        "29 стр. 2",
                        ],
     "Сретенская": [
                    "1",
                    "2",
                    "4",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    ],
     "Русская": [
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "15а",
        "16",
        "18",
        "19",
        "20",
        "22",
        "24",
        "25А",
        "25б",
        "27а",
        "28",
        "29",
        "30",
        "30а",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "41",
        "43",
        "45",
         ],
     "Ясная": [
        "7",
        "27",
        "33",
     ],
     "Благовещенская": [
        "1",
        "2",
        "3",
        "3 стр. 2",
        "4",
        "5",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "20",
        "21",
     ],
     "Смоленская": [
        "5",
        "6",
        "6а",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "16",
     ],
     "Владимирская": [
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "12",
     ],
     "Ильинская": [
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
     ],
     "Казанская": [
        "3",
        "4",
        "5",
        "6",
        "6а",
        "7",
        "8",
        "8а",
        "9",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "21",
        "23",
        "24",
        "25",
        "26",
        "28",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "39а",
        "40",
     ],
}

di = {
   "Успенская": {  
      "1": ['1', '2'], 
      "2а": [],
      "2б": [],
      "3": ['1', '2'], 
      "4": [], 
      "5": [], 
      "7": [], 
   },
   "Тихвинская": { 
      "1": [], 
      "2": ['1', '2'], 
      "3": [],
      "4": [],
      "5а": [],
      "7": [],
      "8": [],
      "8а": [],
      "9": [],
      "9б": [],
      "10": [],
      "11": [],
      "24": [],
   },
   "Запрудная": {
      "1": [],
      "2": [],
      "3": [],
   },
   "Петропавловская": {
      "2": [],
      "3": [],
      "4": [],
      "5": [],
      "5а": [],
      "6": [],
      "7": [],
      "7а": [],
      "8": [],
      "9": [],
      "10": [],
      "11": [],
      "14": [],
      "14а": [],
      "15": [],
      "16": [],
      "17": [],
      "19": [],
      "20": [],
      "21": [],
      "21а": [],
      "22": [],
      "23": [],
      "25": [],
      "27": ['1', '2'],
      "29": ['1', '2'],
   },
   "Сретенская": {
      "1": [],
      "2": [],
      "4": [],
      "5": [],
      "6": [],
      "7": [],
      "8": [],
      "9": [],
      "10": [],
      "11": [],
      "12": ['1', '2'],
      "13": ['1', '2'],
      "14": [],
      "15": [],
      "16": [],
   },
   "Русская": {
      "3": [],
      "4": ['1', '2'],
      "5": [],
      "6": [],
      "7с": [],
      "7о": [],
      "8": [],
      "9": [],
      "10": ['1', '2'],
      "11": [],
      "12": ['1', '2'],
      "13": [],
      "14": [],
      "15": [],
      "15а": [],
      "16": [],
      "18": [],
      "19": [],
      "20": [],
      "22": [],
      "24": [],
      "25а": [],
      "25б": [],
      "27а": [],
      "28": [],
      "29": [],
      "30": [],
      "30а": [],
      "31": [],
      "32": [],
      "33": [],
      "34": [],
      "35": [],
      "36": [],
      "37": [],
      "38": [],
      "39": [],
      "41": [],
      "43": [],
      "45": [],
   },
   "Ясная": {
      "7": [],
      "27": [],
      "33": [],
   },
   "Благовещенская": {
      "1": [],
      "2": ['1', '2'],
      "3": ['1', '2'],
      "4": [],
      "5": [],
      "6": [],
      "7": [],
      "8": [],
      "9": [],
      "10": [],
      "11": [],
      "12": [],
      "13": [],
      "14": [],
      "15": ['1', '2'],
      "16": [],
      "17": [],
      "18": [],
      "19": [],
      "20": [],
      "21": [],
   },
   "Смоленская": {
      "5": [],
      "6": [],
      "6а": [],
      "7": [],
      "8": [],
      "9": [],
      "10": [],
      "11": [],
      "12": [],
      "13": [],
      "16": [],
   },
   "Владимирская": {
      "1": [],
      "2": [],
      "3": [],
      "4": [],
      "5": [],
      "6": [],
      "7": [],
      "8": [],
      "12": [],
   },
   "Ильинская": {
      "3": [],
      "4": [],
      "5": [],
      "6": [],
      "7": [],
      "8": [],
      "9": ['1', '2'],
      "10": [],
      "11": [],
      "12": [],
      "13": [],
      "14": [],
      "15": ['1', '2'],
      "16": [],
   },
   "Казанская": {
      "3": [],
      "4": ['1', '2'],
      "5": [],
      "6": [],
      "6а": [],
      "7": ['1', '2'],
      "8": [],
      "8а": [],
      "9": [],
      "10": [],
      "11": [],
      "12": ['1', '2'],
      "13": ['1', '2'],
      "14": [],
      "15": [],
      "16": ['1', '2'],
      "17": [],
      "18": [],
      "19": [],
      "21": [],
      "23": [],
      "24": [],
      "25": [],
      "26": [],
      "27": [],
      "28": [],
      "29": [],
      "30": ['1', '2'],
      "31": [],
      "32": [],
      "33": [],
      "34": [],
      "35": [],
      "36": [],
      "37": [],
      "38": [],
      "39": [],
      "39а": [],
      "40": [],
   },
   "Счастливая": {
      '11': [],
      '14': [],
      '20': [],
   }
}

def sql():
   
   id = 1
   import sqlite3
   conn = sqlite3.connect(r'D:\tolgobol\TolgobolVillage\TolgobolVillage.sqlite3')
   cur = conn.cursor()
   for strit, value in di.items():
   #Добавили улицу
      cur.execute( f'INSERT INTO AuthService_strit (strit_name) VALUES ("{strit}")' )
      for hous, sub_value in value.items():
         if len(sub_value):
               for kv in sub_value:
                  s = f'INSERT INTO AuthService_adres (id, strit_id, hous, kv) VALUES ( {id}, ( SELECT id FROM AuthService_strit WHERE strit_name = "{strit}"), "{hous}", "{kv}" );'
                  cur.execute( s )
                  id = id +1
         else:
            s = f'INSERT INTO AuthService_adres (id, strit_id, hous) VALUES ( {id}, ( SELECT id FROM AuthService_strit WHERE strit_name = "{strit}"), "{hous}" );'
            cur.execute( s )
            id = id +1
   conn.commit()
    
    

mm = [
   date(year=2021, month=11, day=1),
   date(year=2021, month=12, day=1),
   date(year=2022, month=1, day=1),
   date(year=2022, month=2, day=1),
   date(year=2022, month=3, day=1),
   date(year=2022, month=4, day=1),
   date(year=2022, month=5, day=1),
   date(year=2022, month=6, day=1),
   date(year=2022, month=7, day=1),
   date(year=2022, month=8, day=1),
   date(year=2022, month=9, day=1),
   date(year=2022, month=10, day=1),
   date(year=2022, month=11, day=1),
   date(year=2022, month=12, day=1),
]
def xl():
   def try_int( st ):
      try:
         return int(st)
      except:
         return 0
   def try_str( st ):
      try:
         return str(st)
      except:
         return 
   import pandas as pd
   import sqlite3
   conn = sqlite3.connect(r'D:\tolgobol\TolgobolVillage\TolgobolVillage.sqlite3')
   cur = conn.cursor()
   excel_data = pd.read_excel(r'C:\Users\Evgen\Downloads\Копия Толгоболь .xlsx')
   data = pd.DataFrame(excel_data)
   com = "Фонд поселка необходим для благоустройства и развития. Из фонда поселка деньги берутся на совместные проекты с администрацие, такие как установка фонарей или ремонт дренажной канавы. Так же из фонда берутся деньги на ямочный ремонт дороги"
   insert_collect = f'INSERT INTO MainService_collectmoney (title, comment, on_months, need_summ_on_user, need_total_summ) VALUES ("Фонд поселка", "{com}", 1, 300, 0 )'
   cur.execute(insert_collect)
   conn.commit()

   for i, row in data.iterrows(): 
      strit_str = row[0].split(' ')
      strit = strit_str[0]
      if strit == 'Руусская':
         strit = 'Русская'
      hous = strit_str[1].split('/')[0]
      buf = strit_str[1].split('/')
      kv = buf[1] if len(buf) == 2 else None
      user_last_name = row[1]
      sql_collect_id = 'SELECT id FROM MainService_collectmoney WHERE id = 1'
      collect_id = cur.execute(sql_collect_id).fetchone()[0]
      for m in mm:
         summ = try_int(row[mm.index(m)+2])
         sql_strit = f'SELECT id FROM AuthService_strit WHERE strit_name = "{strit}"'
         f = cur.execute( sql_strit )
         strit_id = f.fetchone()[0]
         if kv:
            
            sql_adr = f'SELECT id FROM AuthService_adres WHERE strit_id = {strit_id} AND hous = "{hous}" AND kv = {kv}'
         else:
            
            sql_adr = f'SELECT id FROM AuthService_adres WHERE strit_id = {strit_id} AND hous = "{hous}"'
         adres_id = cur.execute(sql_adr).fetchone()[0]
         if isinstance(user_last_name, str):
            sql_str = f'INSERT INTO MainService_collectmoneymonth (month, maney, adres_id, collect_id, user_last_name, strit_id) VALUES' \
            + f'( "{m}",'\
            + f' {summ},'\
            + f' {adres_id},'\
            + f' ({collect_id})'\
            + f', "{user_last_name}",'\
            + f' {strit_id} );'
         else:
            sql_str = f'INSERT INTO MainService_collectmoneymonth (month, maney, adres_id, collect_id, strit_id) VALUES' \
            + f'( "{m}",'\
            + f' {summ},'\
            + f' {adres_id},'\
            + f' ({collect_id}),'\
            + f' {(strit_id)}'\
            + ' );'
         try:
            cur.execute( sql_str )
         except:
            raise
   conn.commit()


def vvod():
   conn = sqlite3.connect(r'D:\tolgobol\TolgobolVillage\TolgobolVillage.sqlite3')
   cur = conn.cursor()
   
   sections = {
      'Новости': 1,
      'Вопрос\Ответ': 0,
      'Обсуждения': 0,
      'Реклама\Объявления': 0,
   }
   for key, val in sections.items():
      
      section_sql = f'INSERT INTO Forum_section (name, is_news ) VALUES ( "{key}", {val})'
      cur.execute(section_sql)
   
   title = 'Сайт поселка'
   text = 'Уважаемые жильцы Я сделал этот сайт только по своей инициативе и на свои средства. Основной идею было то что бы все консолидировать в одно месте. А именно что бы каждому была доступна информация по состоянию фонда поселка (сколько собранно, сколько потрачено и куда, кто сдает а кто нет). Так же реализовал механизм голосований который позволяет учитывать голос от одной квартиры\дома, да бы не было накрутки :).'\
   + '\nИ кстати что бы иметь возможность смотреть все разделы целиком необходима авторизация. А что бы было все максимально прозрачно регистрация возможна только с указанием адреса и по приглашению если адрес уже кем то занят.'\
   + '\nПризнаю я не дизайнер а программист и то в другой области, поэтому получилось как то так. Если у кого то есть предложения то я всегда рад.'
   date = '2022-07-22'
   is_news = 1
   news = f'INSERT INTO Forum_post (title, text, date, update_date, is_news, author_id, section_id, is_delet ) VALUES ( "{title}", "{text}","{date}","{date}",{is_news}, 1, 1, 0 )'
   cur.execute(news)
   
   
   title = 'Сайт поселка'
   comment = 'Рад буду услышать ваше мнение по поводу сайта. Если он будет полезен то буду его развивать и дальше'
   is_finish = 1
   voting = f'INSERT INTO MainService_voting (id, title, comment, is_finish ) VALUES ( 1, "{title}", "{comment}",{is_finish} )'
   cur.execute(voting)
   voting_item = ['Норм идея, так держать', 'Мне без разницы', 'Он лишний, лучше в вайбере пол дня искать нужные сообщения']
   for i in voting_item:
      voting_titems_sql = f'INSERT INTO MainService_votingitem (name, voting_id ) VALUES ("{i}", 1)'
      cur.execute(voting_titems_sql)
      
# class AnyContact( models.Model ):
#     title = models.CharField( _('Название контакта'), max_length=100, blank=False, unique=False )
#     comment = models.CharField( _('Комментарий'), max_length=1000, blank=True, unique=False )
#     is_chief = models.BooleanField( _('Является ли старостой'), default=False )

# class ContactField( models.Model ):
#     key = models.CharField( _('Название'), max_length=100, blank=False, unique=False )
#     value = models.CharField( _('Значение'), max_length=1000, blank=False, unique=False )
#     contact = models.ForeignKey( AnyContact, on_delete = models.CASCADE )

   contact = (
      ( 1, 'ул. Казанская ( верх )', 'Юлия Колпакова', 1, [] ),
      ( 2, 'ул. Успенская', 'Денис Домнин', 1, [] ),
      ( 3, 'Амбулатория с. Толгоболь', 'с 09:00 до 12:00 с понедельника по пятницу, первая суббота месяца - рабочая', 0, [ ( 'геристратура', '94-32-89' ), ] ),
      ( 4, 'Амбулатория с. Лесная поляна', 'с 08:00 до 12:00 с понедельника по субботу', 0, [ ( 'геристратура', '765440' ), ] ),
      ( 5, 'Дежурная ЯрЭнерго', '', 0, [( 'телефон', '88005050115' ),] ),
      ( 6, 'Парикмахер', 'Варя Портнова.\nЛюбые парикмахерские услуги: мужские, женские стрижки, укладки, прически, окрашивание волос, коррекция и покраска бровей', 0, [( 'телефон', '89159666092' ), ( 'vk', 'vk.com/id258283296' )] )
   )
   
   for i in contact:
      con_sql = f'INSERT INTO MainService_anycontact (id, title, comment, is_chief ) VALUES ( {i[0]}, "{i[1]}", "{i[2]}",{i[3]} )'
      cur.execute(con_sql)
      for b in i[4]:
         conf_sql = f'INSERT INTO MainService_contactfield (key, value, contact_id ) VALUES ( "{b[0]}", "{b[1]}", {i[0]} )'
         cur.execute(conf_sql)
   
   conn.commit()



# sql()
# xl()
vvod()

   



