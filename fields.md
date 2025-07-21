Estes são os blocos de construção para criar formulários e modelos de dados (DocTypes) no Frappe. Eles definem que tipo de dados cada campo de um formulário pode armazenar e como ele é exibido para o usuário.

# Campos de Dados Comuns

## Data			
Um campo de texto padrão para textos curtos e simples.	
Uso Típico: Nomes, títulos, códigos de produto.

## Attach			
Permite ao usuário anexar qualquer tipo de arquivo, que é salvo no Gerenciador de Arquivos. 
Uso Típico:	Anexar PDFs, planilhas, documentos.

## Attach Image	
Um campo especializado para anexar imagens, que exibe uma pré-visualização (thumbnail).	
Uso Típico: Foto do perfil, imagem de um item.

## Check			
Uma caixa de seleção que armazena 1 (marcado) ou 0 (desmarcado).	
Uso Típico: "Ativo", "Habilitado", "Concluído".

## Code			
Uma área de texto para exibir código (como JS, Python, HTML) com destaque de sintaxe.	
Uso Típico: Armazenar scripts customizados, templates.

## Color			
Exibe um seletor de cores e armazena o código da cor (ex: #FFFFFF).	
Uso Típico: Personalizar a cor de um status ou categoria.

## Dynamic Link
Um campo "Link" especial que pode se conectar a diferentes DocTypes. O tipo de DocType é definido por outro campo no mesmo formulário.	
Uso Típico: Ligar um Pagamento a uma "Fatura de Venda" ou "Fatura de Compra".

# Campos de Data e Hora

## Date		
Um seletor de datas que armazena o valor no formato YYYY-MM-DD.
## Datetime	
Um seletor que permite escolher data e hora.
## Time		
Um seletor que armazena apenas a hora.

# Campos de Números

Tipo de Campo	Descrição
## Currency	
Para valores monetários. Geralmente vinculado a um campo de moeda (ex: USD, BRL) para formatação correta.

## Float	
Para números com casas decimais (números de ponto flutuante). A precisão pode ser configurada.

## Int	
Para números inteiros (sem casas decimais).

## Percent	
Armazena um número, mas o exibe com o símbolo de porcentagem (%).

# Campos de Texto

## Small Text		Uma área de texto para textos de tamanho médio, com múltiplas linhas e sem formatação.
## Long Text		Uma área de texto maior para textos longos, sem formatação.
## Text Editor		Uma área de texto com formatação (Rich Text), permitindo negrito, itálico, listas, imagens, etc.
## Password		Um campo de texto que oculta os caracteres digitados. O valor é salvo de forma criptografada.

# Campos de Seleção e Relações

## Link	
Cria uma relação com outro DocType, exibindo uma lista de registros para seleção. É a base dos relacionamentos no Frappe.	
Uso típico: Selecionar um "Cliente" em uma "Ordem de Venda".
## Select	
Cria uma lista de opções pré-definidas (dropdown) para o usuário escolher.	
Uso típico: Status (Aberto, Em Andamento, Fechado), Tipo (Pessoa Física, Jurídica).
## Table	
Permite criar uma tabela (grade) dentro de um formulário, vinculada a um "Child DocType".	
Uso típico: Itens de uma fatura, lista de contatos de um cliente.
## Table (MultiSelect)	
Uma tabela que permite selecionar e vincular múltiplos registros de um DocType alvo.	
Uso típico: Associar várias "Categorias" a um "Produto".

# Campos Estruturais e de Exibição (Não armazenam dados)

## Section Break	
Cria uma nova seção no formulário, ajudando a agrupar e organizar os campos visualmente.

## Column Break	
Divide uma seção em colunas, permitindo posicionar campos lado a lado.

## Tab Break		
Cria uma nova aba (tab) no formulário, ideal para separar formulários longos em partes lógicas.

## Heading			
Apenas exibe um texto formatado como um título.

## HTML			
Renderiza um bloco de código HTML customizado dentro do formulário.

## Image			
Exibe uma imagem a partir de uma URL ou de um campo "Attach Image" do mesmo DocType.

## Button			
Adiciona um botão clicável que pode executar uma ação de script (JavaScript) do lado do cliente.

## Read Only		
Apenas exibe um valor; não pode ser editado pelo usuário. Geralmente preenchido via script.


# Campos Especiais

## Barcode	
Armazena um valor e gera uma imagem de código de barras para ele.
## Geolocation	
Permite capturar e exibir coordenadas geográficas (latitude, longitude) em um mapa.
## Signature	
Exibe uma área onde o usuário pode desenhar uma assinatura digital.
## Icon	
Permite ao usuário selecionar um ícone de uma biblioteca pré-definida.
