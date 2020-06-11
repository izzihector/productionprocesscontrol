import xmlrpc.client
url = 'https://odoo.processcontrol.es'
db = 'marcosescano-productionprocesscontrol-master-977617'
username = 'hector.cerezo@processcontrol.es'
password = 'AJahn2332'

info = xmlrpc.client.ServerProxy('https://processcontrol.odoo.com').start()
url, db, username, password = \
    info['host'], info['database'], info['user'], info['password']

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
{
    "server_version": "8.0",
    "server_version_info": [8, 0, 0, "final", 0],
    "server_serie": "8.0",
    "protocol_version": 1,
}

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
models.execute_kw(db, uid, password,
    'res.partner', 'check_access_rights',
    ['read'], {'raise_exception': False})