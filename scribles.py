import frappe
import Document
import Item

class Compra(Document):
    def on_submit(self):
        for item in self.itens:
            doc = frappe.get_doc('Item', item.item)
            if not doc:
                frappe.throw(f"Item {item.item} não encontrado.")
            doc.quantidade_em_estoque = doc.quantidade_em_estoque - item.quantidade
            doc.save()            

frappe.db.get_doc('Item', 'ITEM-0001')
frappe.db.get_value('Item', 'ITEM-0001', ['name', 'descricao', 'valor', 'quantidade_em_estoque'])
frappe.db.get_all('Item', fields=['name', 'descricao', 'valor', 'quantidade_em_estoque'])