# Feature Specification: Dungeon Segment Generation

**Feature Branch**: `004-dungeon-segments`
**Created**: 2026-04-05
**Status**: Draft
**Input**: User description: "As masmorras são formadas por segmentos de três tipos: escadaria, corredor e sala. Esses segmentos são conectados por portas. O primeiro segmento de uma masmorra sempre é uma escadaria com uma porta. Ao abrirmos uma porta pela primeira vez, o sistema gera um novo segmento escolhendo de uma tabela com 6 opções. São 3 tabelas: uma para portas abertas a partir de uma escadaria, uma para portas abertas a partida de um corredor e outra para portas abertas a partir de uma sala. A primeira tabela gera corredores com uma a três portas; A segunda tabela gera salas com uma a duas portas, com um dos resultados gerando uma escadaria com uma porta no fundo; a terceira tabela gera salas sem portas, à exceção de um resultado que gera uma escadaria com uma porta no fundo."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Gerar Segmento Inicial da Masmorra (Priority: P1)

Ao iniciar uma exploração, o sistema gera automaticamente o primeiro segmento da masmorra, que sempre é uma escadaria descendendo para o primeiro nível com exatamente uma porta à frente.

**Why this priority**: Sem o segmento inicial, não há masmorra para explorar — é o ponto de entrada obrigatório.

**Independent Test**: Executar `notecli explore` e verificar que o primeiro segmento gerado é uma escadaria com uma porta e indicação de nível 1.

**Acceptance Scenarios**:

1. **Given** que uma nova exploração é iniciada, **When** o primeiro segmento é gerado, **Then** o tipo é "escadaria", nível 1, com exatamente 1 porta.
2. **Given** que o primeiro segmento foi gerado, **When** o jogador vê a descrição, **Then** o sistema exibe "Escadaria — Nível 1" e indica que há 1 porta à frente.

---

### User Story 2 — Gerar Novo Segmento ao Abrir Porta (Priority: P2)

Quando o jogador abre uma porta pela primeira vez, o sistema gera um novo segmento usando a tabela de transição correspondente ao tipo do segmento atual. Cada escadaria aberta aumenta o nível da masmorra. Ao alcançar o nível 3, a Sala Final é encontrada.

**Why this priority**: Este é o mecanismo central de geração procedural da masmorra — é assim que a exploração se desenrola.

**Independent Test**: Abrir uma porta a partir de uma escadaria e verificar que o segmento gerado é um corredor com 1-3 portas. Abrir uma escadaria e verificar que o nível aumenta.

**Acceptance Scenarios**:

1. **Given** que o jogador está em uma escadaria, **When** a porta é aberta, **Then** um novo segmento do tipo "corredor" é gerado com 1 a 3 portas (conforme tabela de 6 opções) e o nível aumenta em 1.
2. **Given** que o jogador está em um corredor, **When** uma porta é aberta, **Then** um novo segmento é gerado conforme a tabela de corredor: sala com 1-2 portas ou escadaria com 1 porta (um dos 6 resultados gera escadaria).
3. **Given** que o jogador está em uma sala, **When** uma porta é aberta, **Then** um novo segmento é gerado conforme a tabela de sala: sala sem portas ou escadaria com 1 porta (um dos 6 resultados gera escadaria).
4. **Given** que uma porta já foi aberta anteriormente, **When** o jogador passa por ela novamente, **Then** o sistema exibe o segmento já existente sem gerar duplicata.
5. **Given** que o jogador está prestes a entrar no nível 3 (já desceu 2 escadarias), **When** uma escadaria é aberta, **Then** a Sala Final é gerada como destino.
6. **Given** que a masmorra foi explorada sem gerar 2 escadarias intermediárias, **When** a última porta disponível é aberta e nenhuma escadaria adicional existe, **Then** o último segmento gerado é marcado como Sala Final.

---

### User Story 3 — Retroceder Entre Segmentos (Priority: P3)

O jogador pode voltar para um segmento já visitado, retrocedendo pelo caminho percorrido. Se o caminho até a entrada estiver livre de monstros, o jogador pode optar por sair da masmorra imediatamente.

**Why this priority**: Permite ao jogador gerenciar risco e recursos, criando uma decisão estratégica de quando parar de explorar.

**Independent Test**: Avançar 2+ segmentos e retroceder até o segmento anterior, verificando que o estado é preservado.

**Acceptance Scenarios**:

1. **Given** que o jogador avançou para um segmento, **When** escolhe retroceder, **Then** retorna ao segmento anterior visitado.
2. **Given** que o jogador está no primeiro segmento (entrada), **When** tenta retroceder, **Then** recebe opção de sair da masmorra.
3. **Given** que existe um caminho livre de monstros até a entrada, **When** o jogador escolhe sair, **Then** a masmorra é encerrada e o personagem é salvo.
4. **Given** que existem monstros no caminho até a entrada, **When** o jogador tenta sair, **Then** o sistema alerta sobre os monstros no caminho.

---

### User Story 4 — Encontrar e Completar a Sala Final (Priority: P4)

A Sala Final é o objetivo da exploração. Ela aparece quando o jogador entra no nível 3 (duas escadarias já foram descidas) ou é o último segmento gerado se a masmorra não produziu escadarias suficientes.

**Why this priority**: Define a condição de vitória/completude da exploração da masmorra.

**Independent Test**: Explorar até encontrar 2 escadarias e verificar que a Sala Final é gerada como destino da segunda escadaria.

**Acceptance Scenarios**:

1. **Given** que o jogador desceu 2 escadarias (está prestes a entrar no nível 3), **When** abre a porta da segunda escadaria, **Then** a Sala Final é gerada.
2. **Given** que o jogador está na Sala Final, **When** a exploração é concluída, **Then** o sistema exibe mensagem de masmorra completada.
3. **Given** que nenhuma escadaria adicional foi gerada e não há mais portas para abrir, **When** o último segmento é alcançado, **Then** esse segmento é marcado como Sala Final.

---

### Edge Cases

- O que acontece quando o jogador tenta abrir uma porta inexistente (todas já abertas)? O sistema informa que não há mais portas naquele segmento.
- O que acontece quando um segmento sem saída (sala sem portas) é alcançado? O jogador é informado e precisa retroceder.
- A masmorra pode ter loops? Sim — se uma porta gera um segmento já existente, o sistema conecta ao segmento existente em vez de criar um novo.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST gerar exatamente 3 tipos de segmentos: escadaria, corredor e sala.
- **FR-002**: O primeiro segmento de toda masmorra MUST ser uma escadaria de nível 1 com exatamente 1 porta.
- **FR-003**: O sistema MUST manter 3 tabelas de transição separadas: uma para escadaria, uma para corredor e uma para sala.
- **FR-004**: Cada tabela de transição MUST ter exatamente 6 opções de resultado.
- **FR-005**: A tabela de transição de escadaria MUST gerar apenas segmentos do tipo "corredor" com 1 a 3 portas.
- **FR-006**: A tabela de transição de corredor MUST gerar segmentos do tipo "sala" com 1-2 portas ou "escadaria" com 1 porta (um dos 6 resultados gera escadaria).
- **FR-007**: A tabela de transição de sala MUST gerar segmentos do tipo "sala" sem portas, exceto um dos 6 resultados que gera "escadaria" com 1 porta.
- **FR-008**: O sistema MUST gerar um novo segmento apenas na primeira vez que uma porta é aberta — portas já abertas não geram segmentos duplicados.
- **FR-009**: O sistema MUST exibir o tipo do segmento atual, o nível e o número de portas disponíveis ao jogador.
- **FR-010**: Cada escadaria aberta MUST aumentar o nível da masmorra em 1.
- **FR-011**: Ao alcançar o nível 3, o sistema MUST gerar a Sala Final como destino da escadaria.
- **FR-012**: Se a masmorra não gerar escadarias suficientes para chegar ao nível 3, o último segmento alcançado MUST ser marcado como Sala Final.
- **FR-013**: O jogador MUST poder retroceder para o segmento anterior visitado.
- **FR-014**: O jogador MUST poder sair da masmorra se o caminho até a entrada estiver livre de monstros.
- **FR-015**: O sistema MUST alertar o jogador sobre monstros no caminho ao tentar sair da masmorra.

### Key Entities

- **Segment**: Representa um segmento da masmorra. Possui tipo (escadaria, corredor ou sala), nível, número de portas, segmentos conectados (referências), e flag `is_final_room`.
- **SegmentType**: Enum com 3 valores: ESCADARIA, CORREDOR, SALA, SALA_FINAL.
- **TransitionTable**: Tabela com 6 opções de segmento, mapeada por tipo de segmento de origem.
- **Dungeon**: Coleção de segmentos conectados em grafo. Mantém referência ao segmento atual, nível máximo alcançado, histórico de segmentos visitados (para retrocesso), e estado de monstros por segmento.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O primeiro segmento de toda masmorra é uma escadaria de nível 1 com 1 porta em 100% das execuções.
- **SC-002**: Ao abrir uma porta, um novo segmento é gerado usando a tabela de transição correta em 100% das execuções.
- **SC-003**: Portas já abertas não geram novos segmentos em 100% das execuções.
- **SC-004**: O jogador consegue identificar o tipo do segmento, nível e número de portas a partir da mensagem exibida em 100% das interações.
- **SC-005**: A Sala Final é gerada corretamente ao entrar no nível 3 ou como último segmento em 100% das execuções.
- **SC-006**: O jogador consegue retroceder pelo caminho percorrido preservando o estado dos segmentos visitados em 100% das tentativas.

## Assumptions

- As 3 tabelas de transição terão 6 entradas cada, selecionadas por rolagem de d6.
- A escolha de qual porta abrir (quando há múltiplas) é feita pelo jogador via input numérico.
- Segmentos gerados são mantidos em memória durante a sessão e persistidos via `exploration.json`.
- O sistema de monstros por segmento será implementado em feature futura — nesta feature, apenas rastreamos se um segmento "tem monstros" ou não (booleano).
- Retrocesso funciona como uma pilha (stack) — o jogador volta ao último segmento visitado.
- "Sair da masmorra" encerra a sessão de exploração e salva o personagem.
