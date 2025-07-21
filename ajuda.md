# Comandos do bench

``` bash
# Iniciar o servidor --> npm run dev ou algo assim
bench start 

bench restart

# Similar ao git reset --hard, além disso, reinstala os apps, builda os assets, migra o banco de dados e instala patches de migração
bench update <opcional> --apps nome_do_app </opcional> --reset
# Reinstala os apps mas NÃO builda e nem migra automaticamente, precisa fazer na mão
bench update --patch

bench use nome_do_site

# Criar um novo app
bench new-app nome_do_app
# Instalar o app no site
bench --site nome_do_site install-app nome_do_app
# Criar um novo site
bench new-site nome_do_site
# Migrar o banco de dados
bench --site nome_do_site migrate
# Limpar o cache
bench clear-cache
# Verificar o status do banco de dados
bench --site nome_do_site doctor
# BUildar os assets do site (CSS, JS)
bench --site nome_do_site build

```

# Eventos do front-end
``` javascript

frappe.ui.form.on('Doctype', {...}); // API para eventos de um DOCTYPE ESPECÍFICO

frappe.ui.form.on('Doctype', { // Eventos EM ORDEM CRONOLÓGICA
    setup(frm) {
        // Lógica a ser executada quando o formulário é criado
    },

    onload(frm) {
        // Lógica a ser executada quando o formulário é carregado
    },

    refresh(frm) { // Ocorre após o onload e sempre que o form atualiza
        // Lógica a ser executada ao atualizar o formulário
    }

    validate(frm) {
        // Lógica de validação do formulário
    },

    before_save(frm) {
        // Lógica a ser executada antes de salvar o formulário
    },

    after_save(frm) {
        // Lógica a ser executada após salvar o formulário
    },

    /**
     * DOCUMENTOS QUE PODEM SER SUBMETIDOS
     */

    before_submit(frm) {
        // Lógica a ser executada antes de submeter o formulário
    },

    on_submit(frm) {
        // Lógica a ser executada após submeter o formulário
    },

    before_cancel(frm) {
        // Lógica a ser executada antes de cancelar o formulário
    },

    after_cancel(frm) {
        // Lógica a ser executada após cancelar o formulário
    },

    // Evento de onchange
    fieldname(frm) {
        // Lógica a ser executada quando o campo "fieldname" é alterado
    },
});

```

# Eventos do back-end
``` python
from frappe.model.document import Document

class Doctype(Document):
    def before_insert(self):
        """Executado ANTES de inserir no banco"""
        # Configurações iniciais, numeração automática
        pass
    
    def validate(self):
        """Validação principal - SEMPRE executado antes de salvar"""
        # Validações de negócio
        if not self.valor_total:
            frappe.throw("Valor total é obrigatório")

    def before_save(self):
        """Executado ANTES de salvar (insert ou update)"""
        # Cálculos automáticos
        self.calcular_total()
    
    def after_insert(self):
        """Executado APÓS inserir no banco"""
        # Criar documentos relacionados
        self.criar_titulos_financeiros()
    
    def on_update(self):
        """Executado APÓS atualizar no banco"""
        # Sincronizar com outros sistemas
        pass
    
    def before_submit(self):
        """Executado ANTES de submeter (docstatus = 1)"""
        # Validações finais
        pass
    
    def on_submit(self):
        """Executado APÓS submeter"""
        # Ações pós-submissão
        pass
    
    def before_cancel(self):
        """Executado ANTES de cancelar"""
        # Verificar se pode cancelar
        pass
    
    def on_cancel(self):
        """Executado APÓS cancelar"""
        # Reverter ações
        pass
    
    def on_trash(self):
        """Executado ANTES de deletar"""
        # Limpar dados relacionados
        pass
```


# Fluxo de Eventos
```
Frontend                    Backend                    Database
    │                          │                          │
    ├─ frappe.call()           │                          │
    │  └─ POST /api/method     │                          │
    │     └─ JSON payload      │                          │
    │                          ├─ @frappe.whitelist()     │
    │                          ├─ Autenticação            │
    │                          ├─ Validação de params     │
    │                          ├─ Execução do método      │
    │                          │  └─ frappe.get_doc()     │
    │                          │     └─ SQL SELECT        ├─ MariaDB
    │                          │  └─ Business Logic       │
    │                          │  └─ doc.save()           │
    │                          │     └─ SQL INSERT/UPDATE ├─ MariaDB
    │                          ├─ Retorno JSON            │
    │                          │                          │
    ├─ response.message        │                          │
    └─ Atualizar UI            │                          │
```

```
👤 USUÁRIO AÇÃO                🖥️ FRONTEND                  🐍 BACKEND                   💾 DATABASE
     │                              │                          │                           │
1.   ├─ Clica "Novo"                │                          │                           │
     │                              ├─ frappe.new_doc()        │                           │
     │                              ├─ Carrega form.js         │                           │
     │                              ├─ Executa setup()         │                           │
     │                              ├─ Executa onload()        │                           │
     │                              └─ Executa refresh()       │                           │
     │                                                         │                           │
2.   ├─ Preenche campos             │                          │                           │
     │                              ├─ Triggers de campos      │                           │
     │                              ├─ valor_servicos()        │                           │
     │                              ├─ frappe.call()           │                           │
     │                              │  ├─ POST /api/method     │                           │
     │                              │  └─ JSON: {doc: {...}}   │                           │
     │                                                         ├─ @frappe.whitelist()      │
     │                                                         ├─ calculo_imposto_nfse()   │
     │                                                         ├─ Business logic           │
     │                                                         └─ return {...}             │
     │                              ├─ response.message        │                           │
     │                              └─ Atualiza campos UI      │                           │
     │                                                         │                           │
3.   ├─ Clica "Salvar"              │                          │                           │
     │                              ├─ Executa validate()      │                           │
     │                              ├─ frm.save()              │                           │
     │                              ├─ POST /api/resource      │                           │
     │                              └─ JSON: documento completo│                           │
     │                                                         ├─ frappe.get_doc()         │
     │                                                         ├─ doc.insert()             │
     │                                                         │  ├─ before_insert()       │
     │                                                         │  ├─ validate()            │
     │                                                         │  ├─ before_save()         │
     │                                                         │  ├─ SQL INSERT            ├─ INSERT tabNF...
     │                                                         │  ├─ after_insert()        │
     │                                                         │  └─ on_update()           │
     │                                                         └─ return doc.as_dict()     │
     │                              ├─ Sucesso!                │                           │
     │                              ├─ Atualiza form           │                           │
     │                              └─ Executa after_save()    │                           │
     │                                                         │                           │
4.   ├─ Form atualizado             │                          │                           │
     └─ Documento salvo             │                          │                           │
```

### **6.2 Atualização de Documento - Fluxo:**

```
👤 USUÁRIO                     🖥️ FRONTEND                  🐍 BACKEND                    💾 DATABASE
     │                              │                           │                           │
1.   ├─ Abre documento              │                           │                           │
     │                              ├─ GET /api/resource        │                           │
     │                              │                           ├─ frappe.get_doc()         │
     │                              │                           │  └─ SQL SELECT            ├─ SELECT * FROM...
     │                              ├─ Executa onload()         │                           │
     │                              ├─ Carrega dados            │                           │
     │                              └─ Executa refresh()        │                           │
     │                                                          │                           │
2.   ├─ Modifica campo              │                           │                           │
     │                              ├─ Trigger do campo         │                           │
     │                              └─ Lógica de negócio        │                           │
     │                                                          │                           │
3.   ├─ Salva alterações            │                           │                           │
     │                              ├─ PUT /api/resource        │                           │
     │                              │                           ├─ doc.save()               │
     │                              │                           │  ├─ before_save()         │
     │                              │                           │  ├─ validate()            │
     │                              │                           │  ├─ check_if_latest()     │
     │                              │                           │  ├─ SQL UPDATE            ├─ UPDATE tabNF...
     │                              │                           │  ├─ on_update()           │
     │                              │                           │  └─ after_save()          │
     │                              └─ Form atualizado          │                           │
```

### **6.3 Submissão de Documento (Workflow):**

```
👤 USUÁRIO                     🖥️ FRONTEND                  🐍 BACKEND              💾 DATABASE
     │                              │                          │                          │
1.   ├─ Clica "Submit"              │                          │                          │
     │                              ├─ Validações client       │                          │
     │                              ├─ POST /api/method        │                          │
     │                              │                          ├─ doc.submit()            │
     │                              │                          │  ├─ validate()           │
     │                              │                          │  ├─ before_submit()      │
     │                              │                          │  ├─ SET docstatus = 1    ├─ UPDATE...docstatus=1
     │                              │                          │  ├─ on_submit()          │
     │                              │                          │  └─ after_submit()       │
     │                              └─ Status atualizado       │                          │
     │                                                         │                          │
2.   ├─ Documento submetido         │                          │                          │
     │   (não pode mais editar)     │                          │                          │
```