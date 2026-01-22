import os

CHUQIN_DIR = os.getenv("CHUQIN_DIR", os.path.expanduser("~"))
CHUQIN_CONFIG_DIR = os.path.join(CHUQIN_DIR, ".chuqin")
