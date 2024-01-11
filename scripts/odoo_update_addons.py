from time import sleep
import logging
import xmlrpc.client as xmlrpclib
import sys

_logger = logging.getLogger(__name__)

USER = sys.argv[1]
PASSWORD = sys.argv[2]
ODOO_URL = sys.argv[3]
DB = sys.argv[4]

print('++++++++++++++++++++++++++ ODOO_URL', ODOO_URL)
print('++++++++++++++++++++++++++ USER', USER)
# print('++++++++++++++++++++++++++ PASSWORD', PASSWORD)
print('++++++++++++++++++++++++++ DB', DB)
uid = False

MAX_ATTEMPTS = 5

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f'--------------------- Attempt {attempt}')
    try:
        common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(ODOO_URL), allow_none=True)
        print('--------------------- TRY server')
        uid = common.authenticate(DB, USER, PASSWORD, {})
        print('--------------------- TRY uid')
        if uid:
            str_error = None
            break  # Break the loop if authentication is successful
    except Exception as e:
        str_error = e
        print(f'--------------------- Authentication error: {str_error}')
    if attempt < MAX_ATTEMPTS:
        print(f'--------------------- Retrying in 10 seconds...')
        sleep(10)

if uid:
    print('--------------------- UID: ', uid)
    object = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(ODOO_URL), allow_none=True)
    object.execute_kw(DB, uid, PASSWORD, 'ir.module.module', 'upgrade_changed_checksum', [])
    print('--------------------- UPGRADE PROCESS')
else:
    print('Authentication failed after multiple attempts.')
    sys.exit(1)  # Exit with a non-zero status code to indicate failure
