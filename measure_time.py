def media():
	import time
	a = time.time()
	for i in range(100):
		doc = frappe.get_doc('Item', 'ITEM-0001')
	b = time.time()
	
	c = time.time()
	for i in range(100):
		values = frappe.db.get_value('Item', 'ITEM0001', ['name', 'descricao', 'valor', 'quantidade_em_estoque'])
	d = time.time()
	
	print(f'{round(b - a, 3)} ms e {round(d - c, 3)} ms')