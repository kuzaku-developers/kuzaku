import os

if os.environ.get("PRODUCTION") != 'yes':
    from dotenv import load_dotenv

    load_dotenv()

botconfig={
    "default_prefix" : "k.",
    "support_id": "761991504793174117",
    "error_id":"868788281528160266",
    "member_role_id":"868788263035498507",
    "log_channel_id":"869638984161189908",
    "devs":
        {"BANana": 
            {'site':"https://bananadev.ml",
            "description":"просто разработчик, который нашел смысл дискорда."}
        },
    "token": os.getenv('BOTTOKEN')
}