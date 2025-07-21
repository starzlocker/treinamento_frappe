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




## 🔄 **6. FLUXO COMPLETO DE UM DOCUMENTO** {#fluxo}

### **6.1 Criação de Documento - Fluxo Detalhado:**

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