# Yeni config.py yaradın və ya onun adını eyni dir və idxalda config.py faylı olaraq dəyişdirin, sonra bu sinfi genişləndirin.
import json
import os



def get_user_list(config, key):
    with open("{}/SerroToBoT/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Yeni config.py yaradın və ya onun adını eyni dir və idxalda config.py faylı olaraq dəyişdirin, sonra bu sinfi genişləndirin.

class Config(object):
    LOGGER = True
    # TƏLƏB OLUNUR
    # https://my.telegram.org saytına daxil olun və onun verdiyi təfərrüatlarla bu slotları doldurun
    
    API_ID = 24066716  # integer value, dont use ""
    API_HASH = "09e30e6e0b1a4c71e43a055979c51b3b"
    TOKEN = "6622010568:AAFf-aMN92QLGBedBNQUYs4S_8TYIXm02gA" 
    
   # Bu var API_KEY idi, lakin indi TOKEN-dir, uyğun olaraq tənzimləyin.
   
    OWNER_ID = 123456789 
    
    # Əgər bilmirsinizsə, botu işə salın və onunla şəxsi söhbətinizdə /id edin, həm də tam ədəd
    
    OWNER_USERNAME = "otobotowner"
    SUPPORT_CHAT = "otobotsport"
    
    # Dəstək üçün öz qrupunuz, @ əlavə etməyin
    
    JOIN_LOGGER = (
        -1002096806763
        
    ) 
    # Botun əlavə olunduğu hər hansı yeni qrupu çap edir, yalnız adı və şəxsiyyəti çap edir.
    
    EVENT_LOGS = (
        -1002096806763
   
   # Botun əlavə olunduğu hər hansı yeni qrupu çap edir, yalnız adı və şəxsiyyəti çap edir.
   
    ALLOW_CHATS = True

    # TÖVSİYƏ
    
    SQLALCHEMY_DATABASE_URI = "mongodb+srv://nesirovq1997:qadir1997@cluster0.pavador.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
   
    # istənilən verilənlər bazası modulları üçün lazımdır
    
    DB_NAME = "nesirovq1997"  
    
    # cron_jobs modulu üçün lazımdır, SQLALCHEMY_DATABASE_URI-dən eyni verilənlər bazası adından istifadə edin
    
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = "KYwCk3Q5dCy2wQnfQk0f785GqAxfFC2X3qkrEsCcbiOAyOINVQ3_W04u0cFBLMnS"  
    # açarı əldə etmək üçün support.spamwat.ch saytına daxil olun
    
    SPAMWATCH_SUPPORT_CHAT = "@otobotsport"
    WEATHER_API = "40fbf20f71e48ffe889014e901afa7db"
    #açarı əldə etmək üçün openweathermap.org/api saytına daxil olun

    # OPSİYONAL
    ##Bota sudo girişi olan istifadəçilər üçün id-lərin siyahısı - (istifadəçi adları deyil).
    SUDO_USERS = get_user_list("elevated_users.json", "sudos")
    ##İdentifikatorların siyahısı - sahibi ilə eyni icazələrə malik olan tərtibatçılar üçün (istifadəçi adları deyil).
    DEV_USERS = get_user_list("elevated_users.json", "devs")
    ##Gban-a icazə verilən, lakin qadağan edilə bilən istifadəçilər üçün id-lərin (istifadəçi adlarının deyil) siyahısı.
    SUPPORT_USERS = get_user_list("elevated_users.json", "supports")
    # Bot tərəfindən qadağan olunmayan /kicked qovulmayan istifadəçilər üçün id-lərin (istifadəçi adlarının deyil) siyahısı.
    WHITELIST_USERS = get_user_list("elevated_users.json", "whitelists")
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True 
    # İstifadəçilərin daxil ola bilmədiyi əmrləri silin, məsələn, qeyri-inzibatçı istifadə edərsə, silmək /ban qadağan etmək.
    STRICT_GBAN = True
    WORKERS = (
        8 
        # İstifadə ediləcək alt başlıqların sayı. Prosessorunuzun istifadə etdiyi iplərin sayı kimi təyin edin
    )
    BAN_STICKER = "🤖" 
    # banhammer marie stiker id-si olduqda, bot bu stikeri söhbətdə istifadəçini qadağan etmədən və ya təpikləməzdən əvvəl göndərəcək.
    
    ALLOW_EXCL = True 
    # İcazə verin! əmrləri, eləcə də / (Qara siyahının işləməsi üçün bunu doğru olaraq buraxın)
    CASH_API_KEY = (
        "0JNDO94L7GPKW3PH"  
        # API açarınızı https://www.alphavantage.co/support/#api-key saytından əldə edin
    )
    TIME_API_KEY = "<font style="vertical-align: inherit;"><font style="vertical-align: inherit;">http://api.timezonedb.com/v2.1/list-time-zone</font></font>" 
   # API açarınızı https://timezonedb.com/api saytından əldə edin
    WALL_API = (
        "42806009-09039b4e09c1bdbd7bdd42170" 
        # Divar kağızları üçün https://pixabay.com/api/docs ünvanından birini əldə edin
    )
    AI_API_KEY = "mongodb+srv://nesirovq1997:qadir1997@cluster0.pavador.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" 
    # Çatbot üçün https://coffeehouse.intellivoid.net/dashboard saytından birini əldə edin
    
    BL_CHATS = [] 
    # Qara siyahıya salınmasını istədiyiniz qrupların siyahısı.
    SPAMMERS = None
    
    BACKUP_PASS = "19970202" 
    # Cron ehtiyat nüsxələri üçün istifadə edilən parol zip
    DROP_UPDATES = False
    # gözləyən yeniləmələri buraxıb-yatırmamaq

class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
