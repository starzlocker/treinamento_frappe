# 1 Criar os doctypes
## 1.1 Criar o doctype "Item"
### 1.1.1 Campos:
- Descrição [descricao] (Data, obrigatório)
- Valor [valor] (Currency, obrigatório, com precisão de 2 casas decimais)
- Quantidade em estoque [quantidade_em_estoque] (Float, obrigatório, com precisão de 4 casas decimais)

### 1.1.2 Especificações:
- Permitir renomear o item automaticamente com o formato "ITEM-.####"

## 1.2 Criar o doctype "compra_itens" (TABELA FILHO)
### 1.2.1 Campos:
- Item [item] (Link para o doctype "Item", obrigatório)
- Descrição [descricao] (Data, preenchido automaticamente a partir do item selecionado)
- Valor Unitário [valor_unitario] (Currency, preenchido automaticamente a partir do item selecionado, obrigatório, com precisão de 2 casas decimais)
- Quantidade [quantidade] (Int, obrigatório, padrão 1, com precisão de 4 casas decimais)
- Valor Total [valor_total] (Currency, preenchido automaticamente com o cálculo de "Valor Unitário" * "Quantidade", obrigatório, com precisão de 2 casas decimais)

## 1.3 Criar o doctype "Compra"
### 1.3.1 Campos:
- Data da Compra [data_da_compra] (Datetime, obrigatório)
- Itens [itens] (Tabela, obrigatório, doctype "compra_itens")
- Total de Itens [total_de_itens] (Int, preenchido automaticamente com o total de itens na tabela "Itens da Compra", obrigatório, somente leitura)
- Valor Total [valor_total] (Currency, preenchido automaticamente com a soma dos valores totais dos itens na tabela "Itens da Compra", obrigatório, somente leitura)

### 1.3.2 Especificações:
- Permitir que o doctype "Compra" seja submetido
- Permitir renomear a compra automaticamente com o formato "COMPRA-.####"

# 2 Criar os scripts do front-end
## 2.1 Script para o doctype "Compra"
- Deve conter a função `refresh` que exibe uma mensagem de atualização quando o formulário é carregado
- Deve conter a API para as alterações da tabela filho "compra_itens"

### 2.1.1 Validações:
- Ao salvar uma compra, deve verificar se há itens suficientes no inventário

### 2.1.2 Funcionalidades da tabela de itens:
- Ao adicionar um item, deve preencher automaticamente os campos "descricao" e "valor_unitario"
- Ao remover uma linha da tabela, deve atualizar o total de itens e o valor total
- Ao alterar o campo "Quantidade", deve recalcular o "valor_total" do item e atualizar o total de itens e o valor total da compra
- Ao alterar o campo "valor_unitario", deve recalcular o "valor_total" do item e atualizar o total de itens e o valor total da compra
- Ao alterar o campo "valor_total", deve atualizar o "valor_unitario" com "valor_total / quantidade"


```javascript
// MODULO/doctype/compra/compra.js

frappe.ui.form.on('Compra', {
    // Trigger de REFRESH (atualização do formulário)
    validate: function(frm) {
        // Ação quando o formulário é validado
        frappe.msgprint('Formulário validado com sucesso!');
    },

    refresh: function(frm) {
        frappe.toast('Atualizando...')
    },

    campo: function(frm) {
        // Ação quando o campo "campo" é alterado
        frm.set_value('campo2', 'Novo Valor');
    },

    campo2: function(frm) {
        // Ação quando o campo "campo2" é alterado
        frm.set_value('campo', 'Outro Valor');
    },
});

frappe.ui.form.on('compra_itens', {
    NOME_CAMPO_TABELA_add: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
        
    },

    NOME_CAMPO_TABELA_remove: function(frm, cdt, cdn) {
        const row = locals[cdt][cdn];
    },

    // Trigger de CHANGE (mudança de valor)
    nome_do_campo: (frm, cdt, cdn) => {
        const row = locals[cdt][cdn];
        row.campo = 2 + 2;
        frm.refresh_field(' NOME_CAMPO_TABELA ');
    }
});
```


==> SEGUNDA PARTE <==
# 3 Criar a validação no backend
## 3.1 Validação de inventário
- Ao salvar uma compra, o inventário deve ser conferido para garantir que há itens suficientes
- Ao submeter uma compra, o inventário deve ser atualizado

```python
# MODULO/doctype/compra/compra.py
import frappe
from frappe.model.document import Document


class Compra(Document):
    def validate(self):
        check_inventory_availability(self.itens)

    def on_submit(self):
        pass


@frappe.whitelist()
def check_inventory_availability(itens):
    pass

# - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# MODULE/doctype/item/item.py
class Item(Document):
    def update_inventory(self, quantidade):
        pass

```