import time
import os

production = os.environ.get("PRODUCTION")

if production != 'yes':
    from dotenv import load_dotenv

    load_dotenv()

botconfig = {
    "default_prefix": "k.",
    "member_role_id": "868788263035498507",
    "log_channel_id": "869638984161189908",
    "support_id":     "761991504793174117",
    "error_id":       "868788281528160266",

    "devs": {
        "BANana": {
            "site": "https://bananadev.ml",
            "description": "просто разработчик, который нашел смысл дискорда.",
        },
        "Un Zote 4o2": {
            "site": "https://misha-python.ml",
            "description": "Непризнанный геней",
        },
    },

    "token": os.getenv('BOTTOKEN'),
    "production": production == 'yes',

    "ignore_cogs": ["channels"],

    "start_time": time.time (),
}