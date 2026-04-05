# Feature Specification: Dungeon Map Display

**Feature Branch**: `006-dungeon-map-display`
**Created**: 2026-04-05
**Status**: Draft
**Input**: User description: "O comando 'notecli map' exibe o mapa completo da última masmorra jogada."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Exibir Mapa da Última Masmorra (Priority: P1)

O jogador executa `notecli map` e o sistema exibe o mapa completo da última sessão de exploração, mostrando todos os segmentos gerados, suas conexões por portas, e o estado de cada porta (explorada, trancada, destrancada).

**Why this priority**: Este é o único e central comportamento da funcionalidade — sem ele, o comando `map` não entrega valor algum.

**Independent Test**: Executar `notecli map` após uma sessão de exploração e verificar que todos os segmentos, portas e conexões são exibidos.

**Acceptance Scenarios**:

1. **Given** que existe uma sessão de exploração ativa ou encerrada, **When** o jogador executa `notecli map`, **Then** o sistema exibe o mapa completo da masmorra com todos os segmentos e suas conexões.
2. **Given** que não existe nenhuma sessão de exploração, **When** o jogador executa `notecli map`, **Then** o sistema exibe uma mensagem informando que nenhuma masmorra foi explorada ainda.
3. **Given** que o jogador explora parcialmente uma masmorra, **When** executa `notecli map`, **Then** o sistema exibe todos os segmentos gerados (incluindo os ainda não visitados) com seus estados de porta.

---

### User Story 2 — Legenda do Mapa (Priority: P2)

O mapa exibido inclui uma legenda explicando os símbolos usados para tipos de segmentos e estados de portas, tornando a visualização autoexplicativa.

**Why this priority**: Sem legenda, o mapa pode ser confuso para jogadores que não conhecem os símbolos.

**Independent Test**: Executar `notecli map` e verificar que a legenda está presente e cobre todos os símbolos usados.

**Acceptance Scenarios**:

1. **Given** que o mapa é exibido, **When** o jogador lê a saída, **Then** uma legenda está presente explicando cada símbolo de tipo de segmento (Escadaria, Corredor, Sala, Sala Final).
2. **Given** que o mapa é exibido, **When** o jogador lê a saída, **Then** uma legenda está presente explicando cada estado de porta (Fechada, Armadilha, Trancada, Destrancada).

---

### Edge Cases

- O que acontece quando a sessão de exploração foi encerrada (saiu da masmorra)? O mapa da última sessão ainda deve ser exibível.
- O que acontece quando não há sessão salva? Mensagem amigável informando que nenhuma masmorra foi explorada.
- O mapa é exibível durante a exploração (em um novo terminal)? Sim — o comando lê o arquivo de persistência, que é atualizado a cada ação.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O comando `notecli map` MUST exibir o mapa completo da última sessão de exploração quando uma existe.
- **FR-002**: O mapa MUST mostrar todos os segmentos gerados na masmorra, incluindo tipo, nível e conexões.
- **FR-003**: O mapa MUST mostrar o estado de cada porta (Fechada, Armadilha, Trancada, Destrancada).
- **FR-004**: O mapa MUST incluir uma legenda explicando símbolos de segmentos e portas.
- **FR-005**: Quando não existe sessão de exploração, o sistema MUST exibir mensagem informativa ao jogador.
- **FR-006**: O mapa MUST ser legível em um terminal de largura padrão (80 colunas).
- **FR-007**: O comando `notecli map` MUST funcionar tanto durante quanto após uma sessão de exploração.

### Key Entities

- **DungeonMap**: Representação textual/visual do grafo de segmentos da masmorra. Derivada dos dados de `ExplorationSession` e `DungeonGraph`.
- **Segment** (existente): Reutilizado para tipo, nível e portas do segmento.
- **Door** (existente): Reutilizado para estado e conexões de cada porta.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O mapa completo é exibido em menos de 100ms após executar `notecli map` em 100% das execuções.
- **SC-002**: Todos os segmentos gerados são exibidos no mapa em 100% das execuções com sessão ativa.
- **SC-003**: A legenda está presente e cobre todos os símbolos usados em 100% das exibições.
- **SC-004**: O mapa é legível em terminal de 80 colunas sem quebra de linha em 100% das exibições.

## Assumptions

- O mapa é exibido como texto ASCII/Unicode no terminal (sem interface gráfica).
- Os dados da masmorra são lidos de `~/.notecli/exploration.json`, que já persiste o grafo de segmentos.
- Não há limite de vezes que o jogador pode executar `notecli map`.
- O mapa não modifica o estado da sessão — é apenas leitura.
