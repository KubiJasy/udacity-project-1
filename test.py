import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
print('file name', __file__)
print('Secret key', SECRET_KEY)
print('base dir', basedir)
