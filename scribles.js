frappe.get_doc(‘Item’, ‘ITEM-0001’)
// GET /doctype/Item/ITEM-0001

frappe.db.get_value('Item', 'ITEM-0001', 'item_name')

frappe.get_list('Item')