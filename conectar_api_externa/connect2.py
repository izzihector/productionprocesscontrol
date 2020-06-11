import xmlrpc.client
url = 'https://processcontrol.odoo.com'
db = 'marcosescano-productionprocesscontrol-master-977617'
username = 'hector.cerezo@processcontrol.es'
password = 'AJahn2332'
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
output = common.version()
uid = common.authenticate(db, username, password, {})
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

result = models.execute(db, uid, password, 'res.partner', 'search_read', [['id', '=', 1]])
number_of_customers = models.execute(db, uid, password, 'res.partner', 'search_count', [])
print('Number of customers: ' + str(number_of_customers))
print(result)