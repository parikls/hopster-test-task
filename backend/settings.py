import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

JWT_SECRET = 'vmdfkvj438nvjkfvFjsnSK19ekjfkgfdsf2SFF2gi2v2'
JWT_SECONDS_EXPIRY_TIME = 60 * 15  # 15 minutes
