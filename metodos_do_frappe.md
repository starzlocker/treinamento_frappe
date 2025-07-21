# 📚 Guia Completo dos Métodos Mais Úteis do Frappe

## 🎯 **BACKEND (Python)**

### **📄 Manipulação de Documentos**

#### **frappe.get_doc()**
```python
# Buscar documento existente
doc = frappe.get_doc("User", "administrator@example.com")
print(doc.full_name)

# Criar novo documento
new_doc = frappe.get_doc({
    "doctype": "ToDo",
    "description": "Nova tarefa",
    "status": "Open"
})
new_doc.insert()
```
**Quando usar**: Principal método para trabalhar com documentos. Use sempre que precisar carregar, criar ou manipular registros.

#### **frappe.new_doc()**
```python
# Criar novo documento vazio
doc = frappe.new_doc("Item")
doc.item_name = "Produto Teste"
doc.item_group = "Products"
doc.save()
```
**Quando usar**: Para criar documentos novos de forma mais limpa que o get_doc com dict.

#### **frappe.get_list() / frappe.get_all()**
```python
# get_list - apenas campos permitidos
items = frappe.get_list("Item", 
    fields=["name", "item_name", "item_group"],
    filters={"disabled": 0},
    order_by="creation desc",
    limit=10
)

# get_all - todos os campos (ignora permissões)
all_items = frappe.get_all("Item",
    fields=["*"],
    filters={"item_group": "Products"}
)
```
**Quando usar**: Para buscar listas de documentos. Use `get_list` para usuários finais e `get_all` para processos internos.

#### **frappe.get_value() / frappe.get_single_value()**
```python
# Buscar valor específico
user_email = frappe.get_value("User", "administrator", "email")

# Buscar múltiplos campos
user_data = frappe.get_value("User", "administrator", 
    ["email", "full_name", "enabled"], as_dict=True)

# Para DocTypes single (configurações)
company_name = frappe.get_single_value("Global Defaults", "default_company")
```
**Quando usar**: Quando você só precisa de campos específicos, não do documento completo. Mais eficiente que get_doc.

### **💾 Banco de Dados**

#### **frappe.db.sql()**
```python
# Query simples
results = frappe.db.sql("SELECT name, email FROM `tabUser` WHERE enabled=1")

# Com parâmetros (seguro contra SQL injection)
results = frappe.db.sql("""
    SELECT name, total_amount 
    FROM `tabSales Invoice` 
    WHERE customer=%s AND posting_date>=%s
""", ("Customer Name", "2023-01-01"), as_dict=True)
```
**Quando usar**: Para queries complexas que não podem ser feitas com get_list. Sempre use parâmetros para valores dinâmicos.

#### **frappe.db.get_value() / frappe.db.get_list()**
```python
# Equivalente ao frappe.get_value mas direto no DB
email = frappe.db.get_value("User", "administrator", "email")

# Buscar com filtros complexos
items = frappe.db.get_list("Item",
    filters=[["item_group", "in", ["Products", "Services"]]],
    fields=["name", "item_name"]
)
```
**Quando usar**: Quando você quer pular validações de permissão ou trabalhar direto com o banco.

#### **frappe.db.set_value() / frappe.db.delete()**
```python
# Atualizar valor direto no banco
frappe.db.set_value("User", "user@example.com", "enabled", 0)

# Atualizar múltiplos campos
frappe.db.set_value("Item", "ITEM-001", {
    "item_name": "Novo Nome",
    "disabled": 1
})

# Deletar registro
frappe.db.delete("ToDo", "TODO-001")
```
**Quando usar**: Para atualizações rápidas sem triggers ou validações. Use com cuidado!

### **🔄 Transações**

#### **frappe.db.commit() / frappe.db.rollback()**
```python
try:
    frappe.db.begin()
    # Operações que devem ser atômicas
    doc1.save()
    doc2.save()
    frappe.db.commit()
except Exception:
    frappe.db.rollback()
    raise
```
**Quando usar**: Para operações que devem ser executadas completamente ou não executadas (atomicidade).

#### **Context Manager para Transações**
```python
from contextlib import contextmanager

@contextmanager
def db_transaction():
    try:
        frappe.db.begin()
        yield
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        raise

# Uso
with db_transaction():
    doc1.save()
    doc2.save()
```

### **⚡ Jobs em Background**

#### **frappe.enqueue()**
```python
# Job simples
frappe.enqueue(
    "myapp.utils.send_email",
    queue="short",
    email="user@example.com",
    subject="Test"
)

# Job com mais opções
frappe.enqueue(
    "myapp.utils.heavy_process",
    queue="long",
    timeout=3600,
    job_name="process_data",
    user_data={"user": frappe.session.user}
)
```
**Quando usar**: Para tarefas que demoram muito (emails, relatórios, processamento de arquivos).

### **📨 Validações e Mensagens**

#### **frappe.throw() / frappe.msgprint()**
```python
# Parar execução com erro
if not user.enabled:
    frappe.throw("Usuário desabilitado", title="Erro de Validação")

# Mensagem informativa
frappe.msgprint("Operação realizada com sucesso!", 
    title="Sucesso", indicator="green")

# Mensagem com mais opções
frappe.msgprint({
    "message": "Dados salvos com sucesso!",
    "title": "Confirmação",
    "indicator": "blue",
    "alert": True
})
```

#### **Validações Comuns**
```python
# Verificar se existe
if not frappe.db.exists("Item", item_code):
    frappe.throw(f"Item {item_code} não encontrado")

# Verificar permissões
if not frappe.has_permission("Sales Invoice", "create"):
    frappe.throw("Sem permissão para criar faturas")

# Validar email
from frappe.utils import validate_email_address
if not validate_email_address(email):
    frappe.throw("Email inválido")
```

### **🛠️ Utilitários**

#### **frappe.utils - Funções de Data/Hora**
```python
from frappe.utils import now, today, add_days, formatdate, get_datetime

# Data/hora atual
current_time = now()  # 2023-12-01 14:30:00
current_date = today()  # 2023-12-01

# Manipular datas
future_date = add_days(today(), 30)
formatted = formatdate(today(), "dd/mm/yyyy")

# Converter strings em datetime
dt = get_datetime("2023-12-01 14:30:00")
```

#### **frappe.utils - Manipulação de Valores**
```python
from frappe.utils import flt, cint, cstr

# Conversões seguras
amount = flt("123.45")  # 123.45 (float)
quantity = cint("10")   # 10 (int)
text = cstr(123)        # "123" (string)

# Com valores padrão
safe_amount = flt(user_input, 0)  # 0 se conversão falhar
```

### **🔍 Meta Informações**

#### **frappe.get_meta()**
```python
meta = frappe.get_meta("Sales Invoice")

# Campos do DocType
for field in meta.fields:
    if field.fieldtype == "Link":
        print(f"{field.fieldname} -> {field.options}")

# Verificar se campo existe
if meta.has_field("custom_field"):
    print("Campo existe")

# Obter configurações
print(meta.autoname)  # Como o nome é gerado
print(meta.is_submittable)  # Se pode ser submetido
```

### **👤 Sessão e Usuário**

#### **frappe.session**
```python
# Informações do usuário atual
current_user = frappe.session.user
user_roles = frappe.get_roles()

# Dados da sessão
if frappe.session.user == "Guest":
    frappe.throw("Login necessário")

# Verificar permissões
if "System Manager" in frappe.get_roles():
    # Código para admin
    pass
```

---

## 🎨 **FRONTEND (JavaScript)**

### **📄 Manipulação de Documentos**

#### **frappe.get_doc() / frappe.db.get_doc()**
```javascript
// Buscar documento (com cache)
const doc = await frappe.get_doc('User', 'administrator');
console.log(doc.full_name);

// Buscar direto do banco (sem cache)
const freshDoc = await frappe.db.get_doc('User', 'administrator');

// Criar novo documento
const newDoc = await frappe.get_doc({
    doctype: 'ToDo',
    description: 'Nova tarefa',
    status: 'Open'
});
```

#### **frappe.get_list() / frappe.db.get_list()**
```javascript
// Buscar lista com filtros
const items = await frappe.db.get_list('Item', {
    fields: ['name', 'item_name', 'item_group'],
    filters: {
        disabled: 0,
        item_group: 'Products'
    },
    limit: 10,
    order_by: 'creation desc'
});

// Com filtros complexos
const invoices = await frappe.db.get_list('Sales Invoice', {
    fields: ['name', 'customer', 'grand_total'],
    filters: [
        ['posting_date', '>=', '2023-01-01'],
        ['grand_total', '>', 1000]
    ]
});
```

#### **frappe.get_value() / frappe.db.get_value()**
```javascript
// Buscar valor específico
const email = await frappe.db.get_value('User', 'administrator', 'email');
console.log(email.message.email);

// Múltiplos campos
const userData = await frappe.db.get_value('User', 'administrator', 
    ['email', 'full_name', 'enabled']);
console.log(userData.message);
```

### **🔧 Manipulação de Forms**

#### **Form Events - frappe.ui.form.on()**
```javascript
frappe.ui.form.on('Sales Invoice', {
    // Quando form carrega
    onload(frm) {
        // Configurações iniciais
        frm.set_query('customer', () => ({
            filters: { disabled: 0 }
        }));
    },

    // Quando form é exibido/atualizado
    refresh(frm) {
        if (!frm.doc.__islocal) {
            frm.add_custom_button('Ação Customizada', () => {
                // Sua lógica aqui
            });
        }
    },

    // Validação antes de salvar
    validate(frm) {
        if (frm.doc.grand_total <= 0) {
            frappe.throw('Valor total deve ser maior que zero');
        }
    },

    // Quando campo específico muda
    customer(frm) {
        if (frm.doc.customer) {
            frappe.db.get_value('Customer', frm.doc.customer, 'default_currency')
                .then(r => {
                    if (r.message.default_currency) {
                        frm.set_value('currency', r.message.default_currency);
                    }
                });
        }
    }
});

// Events para child table
frappe.ui.form.on('Sales Invoice Item', {
    qty(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    },

    rate(frm, cdt, cdn) {
        calculate_item_amount(frm, cdt, cdn);
    }
});

function calculate_item_amount(frm, cdt, cdn) {
    const row = locals[cdt][cdn];
    row.amount = row.qty * row.rate;
    frm.refresh_field('items');
}
```

#### **Métodos do Form (frm)**
```javascript
// Definir valores
frm.set_value('field_name', 'value');
frm.set_value({
    'field1': 'value1',
    'field2': 'value2'
});

// Setar configurações do campo
frm.set_df_property('field_name', 'read_only', 1); // somente leitura
frm.set_df_property('field_name', 'hidden', 1); // ocultar campo
frm.set_df_property('field_name', 'reqd', 1); // campo obrigatório

// Filtros para Link fields
frm.set_query('customer', () => ({
    filters: { 
        disabled: 0,
        customer_type: 'Company'
    }
}));

// Atualizar display
frm.refresh_field('field_name');
frm.refresh_fields(['field1', 'field2']);

// Salvar documento
frm.save();
frm.save_or_update();

// Botões customizados
frm.add_custom_button('Meu Botão', () => {
    frappe.msgprint('Botão clicado!');
}, 'Grupo de Ações');

// Dashboard
frm.dashboard.add_indicator('Status', 'blue');
```

### **📞 Chamadas de API**

#### **frappe.call()**
```javascript
// Chamada simples
const response = await frappe.call({
    method: 'myapp.api.my_function',
    args: {
        param1: 'value1',
        param2: 'value2'
    }
});
console.log(response.message);

// Com opções avançadas
frappe.call({
    method: 'myapp.api.heavy_process',
    args: { data: large_data },
    freeze: true,
    freeze_message: 'Processando...',
    callback: (r) => {
        if (r.message) {
            frappe.msgprint('Sucesso!');
        }
    },
    error: (r) => {
        frappe.msgprint('Erro: ' + r.message);
    }
});
```

#### **frappe.xcall() - Versão Async/Await**
```javascript
try {
    const result = await frappe.xcall('myapp.api.my_function', {
        param1: 'value1'
    });
    console.log(result);
} catch (error) {
    frappe.msgprint('Erro: ' + error.message);
}
```

### **💬 Interface e Feedback**

#### **Mensagens e Diálogos**
```javascript
// Mensagens simples
frappe.msgprint('Operação concluída!');
frappe.msgprint({
    title: 'Sucesso',
    message: 'Dados salvos com sucesso!',
    indicator: 'green'
});

// Toast (notificação rápida)
frappe.show_alert('Salvo automaticamente', 3);
frappe.show_alert({
    message: 'Email enviado!',
    indicator: 'green'
}, 5);

// Confirmar ação
frappe.confirm('Tem certeza que deseja excluir?', () => {
    // Ação confirmada
    delete_record();
});

// Prompt para input
frappe.prompt('Digite seu nome', (values) => {
    frappe.msgprint('Olá, ' + values.value);
});

// Prompt com múltiplos campos
frappe.prompt([
    {
        fieldtype: 'Data',
        fieldname: 'date',
        label: 'Data',
        reqd: 1
    },
    {
        fieldtype: 'Currency',
        fieldname: 'amount',
        label: 'Valor'
    }
], (values) => {
    console.log(values);
}, 'Preencha os dados');
```

#### **Diálogos Customizados**
```javascript
// Criar diálogo
const dialog = new frappe.ui.Dialog({
    title: 'Meu Diálogo',
    fields: [
        {
            fieldtype: 'Link',
            fieldname: 'customer',
            label: 'Cliente',
            options: 'Customer',
            reqd: 1
        },
        {
            fieldtype: 'Currency',
            fieldname: 'amount',
            label: 'Valor'
        }
    ],
    primary_action_label: 'Salvar',
    primary_action: (values) => {
        console.log(values);
        dialog.hide();
    }
});

dialog.show();

// Definir valores
dialog.set_value('customer', 'CUST-001');
dialog.set_values({
    'customer': 'CUST-001',
    'amount': 1000
});
```

### **📋 Listagem e Filtros**

#### **frappe.listview_settings**
```javascript
// Configurações para ListView
frappe.listview_settings['Sales Invoice'] = {
    add_fields: ['customer', 'grand_total', 'outstanding_amount'],
    
    get_indicator: (doc) => {
        if (doc.outstanding_amount > 0) {
            return [__('Unpaid'), 'orange', 'outstanding_amount,>,0'];
        } else {
            return [__('Paid'), 'green', 'outstanding_amount,=,0'];
        }
    },

    onload: (listview) => {
        // Filtros padrão
        listview.page.add_menu_item('Apenas em Aberto', () => {
            listview.filter_area.add_filter('outstanding_amount', '>', 0);
        });
    }
};
```

### **🎯 Utilitários Frontend**

#### **Formatação e Conversão**
```javascript
// Formatação de números
const formatted_currency = format_currency(1234.56, 'BRL');
const formatted_number = format_number(1234.56, null, 2);

// Datas
const formatted_date = frappe.datetime.global_date_format(date_string);
const user_date = frappe.datetime.str_to_user(date_string);

// Conversões
const float_val = flt(string_number, 2);  // Com 2 decimais
const int_val = cint(string_number);
```

#### **Navegação**
```javascript
// Ir para documento
frappe.set_route('Form', 'Sales Invoice', 'SI-001');

// Ir para listagem
frappe.set_route('List', 'Customer');

// Ir para relatório
frappe.set_route('query-report', 'Sales Analytics');

// Voltar
frappe.route_history.back();
```

#### **Local Storage**
```javascript
// Salvar no localStorage
frappe.boot.cache_user_settings = {
    'my_setting': 'value'
};

// Acessar configurações do usuário
const user_settings = frappe.user_settings;
```

### **⚙️ Configurações e Hooks**

#### **Boot Info**
```javascript
// Informações disponíveis no carregamento
console.log(frappe.boot.user);           // Usuário atual
console.log(frappe.boot.sysdefaults);    // Configurações do sistema
console.log(frappe.boot.user_info);      // Info detalhada do usuário
console.log(frappe.defaults);            // Valores padrão
```

#### **Eventos Globais**
```javascript
// Escutar eventos
$(document).on('app_ready', () => {
    console.log('App carregado!');
});

// Disparar eventos customizados
frappe.realtime.on('custom_event', (data) => {
    console.log('Evento recebido:', data);
});
```

---

## 🚀 **Dicas de Performance e Boas Práticas**

### **Backend**
1. **Use `frappe.get_value()` ao invés de `frappe.get_doc()`** quando só precisar de campos específicos
2. **Prefira `frappe.db.get_list()` ao invés de loops com `get_doc()`**
3. **Use transações para operações múltiplas relacionadas**
4. **Implemente cache quando apropriado** com `frappe.cache()`
5. **Use background jobs para tarefas pesadas**

### **Frontend**
1. **Cache documentos quando possível** - use `frappe.get_doc()` ao invés de `frappe.db.get_doc()`
2. **Debounce chamadas de API** em campos que mudam frequentemente
3. **Use `frm.refresh_field()` ao invés de `frm.refresh()`** para atualizações específicas
4. **Implemente loading states** com `freeze: true` em chamadas longas
5. **Valide dados no frontend** antes de enviar para o backend

---

## 📝 **Métodos Específicos para Child Tables**

### **Backend**
```python
# Trabalhar com child tables
doc = frappe.get_doc("Sales Invoice", "SI-001")

# Adicionar linha
doc.append("items", {
    "item_code": "ITEM-001",
    "qty": 1,
    "rate": 100
})

# Remover linha específica
for item in doc.items:
    if item.item_code == "ITEM-001":
        doc.remove(item)
        break

# Limpar todas as linhas
doc.items = []

doc.save()
```

### **Frontend**
```javascript
// Adicionar linha na child table
let row = frm.add_child('items');
row.item_code = 'ITEM-001';
row.qty = 1;
row.rate = 100;
frm.refresh_field('items');

// Remover linha específica
frm.doc.items = frm.doc.items.filter(item => item.item_code !== 'ITEM-001');
frm.refresh_field('items');

// Acessar linha específica em eventos
frappe.ui.form.on('Sales Invoice Item', {
    qty(frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        row.amount = row.qty * row.rate;
        frm.refresh_field('items');
    }
});
```

---

## 🔒 **Permissões e Segurança**

### **Backend**
```python
# Verificar permissões
if frappe.has_permission("Sales Invoice", "create"):
    # Usuário pode criar
    pass

# Verificar permissão específica para documento
if frappe.has_permission("Sales Invoice", "write", "SI-001"):
    # Usuário pode editar este documento específico
    pass

# Ignorar permissões (usar com cuidado)
doc.insert(ignore_permissions=True)
doc.save(ignore_permissions=True)

# Executar como usuário específico
frappe.set_user("Administrator")
# ... operações como admin
frappe.set_user(original_user)
```

### **Frontend**
```javascript
// Verificar se usuário tem permissão
if (frappe.perm.has_perm('Sales Invoice', 0, 'create')) {
    // Mostrar botão de criar
}

// Verificar roles
if (frappe.user_roles.includes('Sales Manager')) {
    // Lógica específica para Sales Manager
}
```

---

## 🌐 **Hooks e Eventos**

### **Backend (hooks.py)**
```python
# hooks.py
doc_events = {
    "Sales Invoice": {
        "before_save": "myapp.utils.before_save_invoice",
        "after_insert": "myapp.utils.after_insert_invoice",
        "on_submit": "myapp.utils.on_submit_invoice",
        "on_cancel": "myapp.utils.on_cancel_invoice"
    },
    "*": {
        "before_save": "myapp.utils.global_before_save"
    }
}

# Implementação
def before_save_invoice(doc, method):
    # Lógica executada antes de salvar qualquer Sales Invoice
    pass

def global_before_save(doc, method):
    # Executado antes de salvar qualquer documento
    pass
```

### **Frontend**
```javascript
// Hooks globais
frappe.ui.form.on('*', {
    refresh(frm) {
        // Executado em todos os forms
        console.log(`Form ${frm.doctype} carregado`);
    }
});

// Hook para múltiplos DocTypes
['Sales Invoice', 'Purchase Invoice'].forEach(doctype => {
    frappe.ui.form.on(doctype, {
        validate(frm) {
            // Validação comum para ambos os DocTypes
        }
    });
});
```

Este guia cobre os métodos mais utilizados no dia a dia do desenvolvimento Frappe! 🎉
