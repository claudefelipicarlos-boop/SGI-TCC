# Casos de Teste — SGI

Sistema de Gestão Industrial — 1 caso de teste de cada tipo (Funcional, Interface, Integração, API, Segurança, Performance)

*Estrutura de campos e prefixos de código conforme o "Modelo de Formulário de Teste de Software" fornecido pelo aluno.*

## Sobre esta versão

| Campo | Descrição |
|---|---|
| **Objetivo deste documento** | Apresentação de hoje: 1 caso de teste representativo de cada tipo do modelo (CT, UI, INT, API, SEC, PERF), independente do resultado ter sido Aprovado ou Reprovado. |
| **Método de execução** | Casos CT/UI/INT/SEC: testes automatizados em Node.js (`testes/test_tipos.js`), executando o CÓDIGO REAL extraído de `index.html`. Caso API: teste automatizado em Python (`testes/test_api.py`), subindo o servidor HTTP REAL de `servidor.py` numa porta local e fazendo requisições HTTP de verdade (só a função que abre o Chrome via Selenium foi substituída por um dublê). |
| **Suíte completa** | Este documento mostra 1 caso de cada tipo. A suíte completa, com 23 casos (12 CT, 3 UI, 2 INT, 2 API, 3 SEC, 1 PERF — 18 aprovados, 5 reprovados), está documentada em `Casos_de_Teste_SGI_Tipos.docx`. |

---

## CT — Caso de Teste Funcional

### Caso de Teste CT-002: Nome repetido (planta/peça/máquina) não bloqueia mais — vira pendente e não conecta

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | CT-002 |
| Nome do Teste | Nome repetido (planta/peça/máquina) não bloqueia mais — vira pendente e não conecta |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | Cadastro Geral — Planta / Peça / Máquina |
| Tipo de Teste | Funcional |
| Prioridade | Alta |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Verificar se cadastrar um nome já existente não bloqueia mais o salvamento (permitindo colar um bloco copiado), mas marca o registro como pendente (invalido=true) e impede que ele se conecte a outros blocos até ser corrigido — sem gerar falso-positivo em nomes realmente únicos. |
| Explicação da Tela | Formulário de Planta/Peça/Máquina, e conexões entre blocos no grafo (graphCriarLigacao). |
| Pré-condições | Já existe uma planta "Planta 1" cadastrada para o cliente X. |
| Dados de Entrada | Tentativa de criar "planta   1" (espaços/maiúsculas diferentes) pro mesmo cliente; e, em separado, "Planta 2" (nome único). |
| Passos para Execução | 1. Salvar planta com nome que colide (ignorando maiúscula/espaço) com uma existente. 2. Conferir que grava mesmo assim, como invalido=true. 3. Repetir com nome único (controle). 4. Tentar conectar um bloco invalido e um bloco válido no grafo. |
| Resultado Esperado | Nome duplicado: grava normalmente, com invalido=true e aviso por toast, sem bloquear o formulário. Nome único: grava com invalido=false, sem aviso. Bloco invalido: graphCriarLigacao() recusa a conexão com toast de aviso. Bloco válido: conecta normalmente. |
| Resultado Obtido | Confirmado nos quatro pontos: duplicado salvou pendente e avisou; nome único salvou normal (sem falso-positivo); ligação envolvendo bloco pendente foi bloqueada; ligação envolvendo bloco válido foi permitida. |
| **Status** | ✅ **Aprovado** |
| Evidências | testes/test_tipos.js, caso CT-002. |
| Observações | Implementado a pedido do usuário nesta rodada, substituindo o bloqueio total que existia antes. Regra idêntica aplicada a peça e à máquina (ativo). |

---

## UI — Caso de Interface

### Caso de Teste UI-003: Bloco pendente (nome duplicado) aparece esmaecido/cinza no grafo e não conecta pela porta

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | UI-003 |
| Nome do Teste | Bloco pendente (nome duplicado) aparece esmaecido/cinza no grafo e não conecta pela porta |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | Cadastro Geral (grafo) |
| Tipo de Teste | Interface |
| Prioridade | Média |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Verificar se um bloco marcado como pendente (invalido=true, ver CT-002) recebe o estilo visual esmaecido/cinza no grafo, e se as portas de conexão desse bloco ficam desativadas ao passar o mouse. |
| Explicação da Tela | Blocos do grafo (planta/máquina/peça) usam a classe ".gnode-invalido" quando invalido=true. |
| Pré-condições | Nenhuma — verificação direta da regra CSS gerada. |
| Dados de Entrada | Regras CSS ".gnode-invalido", ".gnode-invalido .gnode-hd" e ".gnode-invalido .gport" em index.html. |
| Passos para Execução | 1. Localizar a regra ".gnode-invalido". 2. Conferir opacity e filter (grayscale). 3. Conferir se as portas (.gport) dentro do bloco inválido têm pointer-events:none. |
| Resultado Esperado | Bloco pendente deve ficar com opacity reduzida e escala de cinza (grayscale), e suas portas de conexão devem ficar desativadas ao clique (pointer-events:none). |
| Resultado Obtido | Confirmado: opacity:.55 + filter:grayscale(.7) na regra principal, e pointer-events:none nas portas do bloco inválido. |
| **Status** | ✅ **Aprovado** |
| Evidências | testes/test_tipos.js, caso UI-003 (verificação de regra CSS real). |
| Observações | Complementa o CT-002 do lado puramente visual — o usuário vê de cara, no grafo, qual bloco precisa de correção antes de poder conectar. |

---

## INT — Caso de Integração

### Caso de Teste INT-001: Numeração de OS sob concorrência: duas criações simultâneas podem gerar o MESMO número

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | INT-001 |
| Nome do Teste | Numeração de OS sob concorrência: duas criações simultâneas podem gerar o MESMO número |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | Ordens de Serviço — cadastro / integração com Firestore |
| Tipo de Teste | Integração |
| Prioridade | Alta |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Verificar se duas criações de OS ao mesmo tempo (dois usuários, ou duas abas do mesmo usuário) podem receber o mesmo "número" de OS, por a numeração não usar transação atômica do Firestore. |
| Explicação da Tela | Ao criar uma OS, o sistema lê o tamanho atual da coleção "ordens_servico" e usa esse tamanho+1 pra montar o número exibido (ex.: "OS-2901") — em duas chamadas Firestore separadas, não numa transação. |
| Pré-condições | Coleção "ordens_servico" simulada com 0 documentos; duas "abas" concorrentes usando o mesmo Firestore simulado, com latência de rede simulada. |
| Dados de Entrada | Duas chamadas concorrentes ao trecho real de numeração, extraído de salvarOS(). |
| Passos para Execução | 1. Dispara as duas chamadas ao mesmo tempo (Promise.all). 2. Aguarda os dois números retornados. 3. Compara se são iguais ou diferentes. |
| Resultado Esperado | Num sistema correto, cada criação de OS deveria receber um número ÚNICO, mesmo sob concorrência. |
| Resultado Obtido | REPROVADO: as duas chamadas concorrentes retornaram o MESMO número ("OS-2901" duas vezes) — confirma a condição de corrida. |
| **Status** | 🔴 **Reprovado** |
| Evidências | testes/test_tipos.js, caso INT-001. |
| Observações | ACHADO DE BUG ainda não corrigido. O padrão certo já existe no próprio sistema (proximoCodigo, usado em Máquina/Técnico/Peça). |

---

## API — Caso de API

### Caso de Teste API-002: Endpoint /enviar exige numero e mensagem; aciona o envio quando os dois estão presentes

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | API-002 |
| Nome do Teste | Endpoint /enviar exige numero e mensagem; aciona o envio quando os dois estão presentes |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | servidor.py — servidor de envio WhatsApp (porta 5000) |
| Tipo de Teste | API |
| Prioridade | Alta |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Verificar se /enviar rejeita a requisição com 400 quando faltam os parâmetros obrigatórios (numero/mensagem), e se aciona o envio corretamente quando ambos estão presentes. |
| Explicação da Tela | Endpoint que recebe um número de telefone e uma mensagem, e dispara o envio real via WhatsApp Web (Selenium). |
| Pré-condições | Servidor real rodando; enviar_whatsapp() substituída por um dublê que só registra a chamada. |
| Dados de Entrada | GET /enviar (sem parâmetros); GET /enviar?numero=19987654321&mensagem=Teste de envio. |
| Passos para Execução | 1. Chamar /enviar sem parâmetros. 2. Conferir erro 400. 3. Chamar /enviar com numero e mensagem preenchidos. 4. Conferir resposta 200. |
| Resultado Esperado | Sem parâmetros: HTTP 400. Com parâmetros: HTTP 200, e enviar_whatsapp() chamada com os valores certos. |
| Resultado Obtido | Confirmado nos dois casos. |
| **Status** | ✅ **Aprovado** |
| Evidências | testes/test_api.py, caso API-002 — servidor real, requisições HTTP reais. |
| Observações | Nenhuma. |

---

## SEC — Caso de Segurança

### Caso de Teste SEC-002: XSS armazenado: nome de cliente com HTML/script não é escapado

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | SEC-002 |
| Nome do Teste | XSS armazenado: nome de cliente com HTML/script não é escapado |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | Contas de Acesso — seletor de cliente |
| Tipo de Teste | Segurança |
| Prioridade | Crítica |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Verificar se um nome de cliente contendo HTML/JavaScript malicioso é inserido "cru" (sem escapar) no innerHTML da tela, executando o script no navegador de quem visualizasse essa tela. |
| Explicação da Tela | popularClientesConta() monta as opções do seletor de cliente com template string e innerHTML, sem função de escape. |
| Pré-condições | Nenhuma. |
| Dados de Entrada | Cliente cadastrado com nome contendo uma tag de imagem com evento de erro disparando um script (payload de teste). |
| Passos para Execução | 1. Cadastrar (simular) um cliente com esse nome. 2. Rodar popularClientesConta(). 3. Inspecionar o innerHTML gerado. |
| Resultado Esperado | O nome do cliente deveria ser escapado antes de entrar no HTML, impedindo a execução do script. |
| Resultado Obtido | O innerHTML gerado contém o payload EXATO, sem qualquer escape de tags ou aspas. |
| **Status** | 🔴 **Reprovado** |
| Evidências | testes/test_tipos.js, caso SEC-002. |
| Observações | ACHADO DE SEGURANÇA ainda não corrigido. O mesmo padrão aparece em 48 pontos de index.html. |

---

## PERF — Caso de Performance

### Caso de Teste PERF-001: Custo de leitura da numeração de OS cresce com o tamanho da coleção (O(n)); numeração por contador é O(1)

**Informações Gerais do Teste**

| Campo | Valor |
|---|---|
| Código do Teste | PERF-001 |
| Nome do Teste | Custo de leitura da numeração de OS cresce com o tamanho da coleção (O(n)); numeração por contador é O(1) |
| Responsável | Felipi |
| Data do Teste | 26/08/2026 |
| Versão do Sistema | index.html — versão atual (v2.0.1) |
| Módulo/Tela | Ordens de Serviço — custo de leitura no Firestore |
| Tipo de Teste | Performance |
| Prioridade | Média |

**Descrição do Cenário**

| Campo | Valor |
|---|---|
| Objetivo do Teste | Medir quantos documentos são lidos do Firestore só para gerar o número de uma nova OS, e comparar com o custo constante de proximoCodigo(). |
| Explicação da Tela | Cada OS nova lê a coleção inteira só para saber quantos documentos já existem. |
| Pré-condições | Coleções simuladas com 10, 500 e 3000 OS já existentes. |
| Dados de Entrada | Contagem de documentos lidos em cada chamada, para coleções de 10 / 500 / 3000 OS; e para proximoCodigo. |
| Passos para Execução | 1. Simular coleções de 3 tamanhos diferentes. 2. Instrumentar a leitura. 3. Rodar a numeração de OS em cada tamanho. 4. Rodar proximoCodigo() como comparação. |
| Resultado Esperado | A numeração de OS deveria ler sempre 1 único documento, não importa quantas OS já existem — custo constante O(1), igual a proximoCodigo(). |
| Resultado Obtido | REPROVADO: a leitura cresce junto com a coleção — leu 10, 500 e 3000 documentos nos três tamanhos testados. proximoCodigo() leu sempre exatamente 1. |
| **Status** | 🔴 **Reprovado** |
| Evidências | testes/test_tipos.js, caso PERF-001. |
| Observações | ACHADO DE PERFORMANCE ainda não corrigido. Mesma causa raiz do INT-001. |

---

## Resumo desta versão

| Caso | Tipo | Status |
|---|---|---|
| CT-002 | Funcional | ✅ Aprovado |
| UI-003 | Interface | ✅ Aprovado |
| INT-001 | Integração | 🔴 Reprovado |
| API-002 | API | ✅ Aprovado |
| SEC-002 | Segurança | 🔴 Reprovado |
| PERF-001 | Performance | 🔴 Reprovado |

**3 aprovados, 3 reprovados** — os reprovados são achados reais, ainda sem correção aplicada.
