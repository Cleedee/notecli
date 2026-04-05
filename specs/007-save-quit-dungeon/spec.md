# Feature Specification: Save and Quit Dungeon

**Feature Branch**: `007-save-quit-dungeon`
**Created**: 2026-04-05
**Status**: Draft
**Input**: User description: "Criar uma opção de sair do jogo salvando a posição do personagem na masmorra, diferente da opção 'Sair da Masmorra' que foi implementada."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Salvar Posição e Sair do Jogo (Priority: P1)

Durante a exploração, o jogador pode escolher "Salvar e Sair" para pausar a exploração, salvando a posição exata do personagem na masmorra (segmento atual, portas abertas, estados de portas, estoque de tochas). A sessão de exploração permanece ativa para que o jogador possa retomar de onde parou.

**Why this priority**: Diferente de "Sair da Masmorra" (que encerra a exploração e retira o personagem), esta opção permite pausar e retomar exatamente de onde o jogador parou — essencial para sessões longas de exploração.

**Independent Test**: Durante a exploração, usar "Salvar e Sair", depois executar `notecli explore --resume` e verificar que o jogador retorna ao mesmo segmento, com portas e estoque preservados.

**Acceptance Scenarios**:

1. **Given** que o jogador está explorando um segmento intermediário da masmorra, **When** escolhe "Salvar e Sair", **Then** a posição do segmento atual, estados das portas e estoque do personagem são salvos, e a sessão permanece ativa.
2. **Given** que o jogador salvou e saiu, **When** executa `notecli explore --resume`, **Then** o sistema oferece retomar exatamente do segmento onde parou, com todas as portas e estados preservados.
3. **Given** que o jogador salvou e saiu no meio de um segmento com portas parcialmente abertas, **When** retoma a exploração, **Then** as portas já abertas continuam reveladas e as portas fechadas permanecem inalteradas.

---

### User Story 2 — Diferença Clara entre "Sair da Masmorra" e "Salvar e Sair" (Priority: P2)

O sistema deve deixar claro para o jogador a diferença entre "Sair da Masmorra" (encerra a exploração, personagem fica seguro fora da masmorra) e "Salvar e Sair" (pausa a exploração, personagem permanece na masmorra na posição atual).

**Why this priority**: Sem clareza, o jogador pode confundir as opções e perder progresso ou achar que salvou quando na verdade saiu da masmorra.

**Independent Test**: Executar ambas opções e verificar que mensagens distintas são exibidas e que os estados resultantes são diferentes.

**Acceptance Scenarios**:

1. **Given** que o jogador está na exploração, **When** escolhe "Sair da Masmorra", **Then** o sistema exibe mensagem indicando que a exploração foi encerrada e o personagem está fora da masmorra.
2. **Given** que o jogador está na exploração, **When** escolhe "Salvar e Sair", **Then** o sistema exibe mensagem indicando que o progresso foi salvo e o personagem permanece na masmorra.
3. **Given** que o jogador usou "Sair da Masmorra", **When** executa `notecli explore --resume`, **Then** o sistema informa que não há sessão ativa para retomar.
4. **Given** que o jogador usou "Salvar e Sair", **When** executa `notecli explore --resume`, **Then** o sistema oferece retomar do ponto exato onde parou.

---

### User Story 3 — Retomar com `notecli explore` após "Salvar e Sair" (Priority: P3)

Ao executar `notecli explore` (sem `--resume`) após ter usado "Salvar e Sair", o sistema pergunta se o jogador deseja retomar a sessão salva ou iniciar uma nova exploração.

**Why this priority**: Facilita a retomada — o jogador não precisa lembrar de usar `--resume`.

**Independent Test**: Usar "Salvar e Sair", depois executar `notecli explore` e verificar que a opção de retomar é oferecida.

**Acceptance Scenarios**:

1. **Given** que existe uma sessão ativa de "Salvar e Sair", **When** o jogador executa `notecli explore`, **Then** o sistema pergunta se deseja retomar a sessão ou iniciar nova exploração.
2. **Given** que o jogador escolhe retomar, **When** confirma, **Then** a exploração continua do segmento salvo.
3. **Given** que o jogador escolhe nova exploração, **When** confirma, **Then** a sessão anterior é descartada e uma nova masmorra é gerada.

---

### Edge Cases

- O que acontece se o arquivo de sessão estiver corrompido? O sistema exibe o erro e oferece iniciar nova exploração.
- O que acontece se o personagem salvo não existir mais? O sistema informa e oferece criar novo personagem.
- O que acontece se o jogador salvar e sair, depois criar uma nova masmorra? A sessão antiga é substituída.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST oferecer a opção "Salvar e Sair" durante a exploração, separada de "Sair da Masmorra".
- **FR-002**: Ao usar "Salvar e Sair", o sistema MUST persistir o segmento atual do jogador, o grafo de segmentos, estados de portas e estoque do personagem.
- **FR-003**: A sessão de exploração MUST permanecer ativa após "Salvar e Sair" (não é desativada como em "Sair da Masmorra").
- **FR-004**: Ao retomar via `notecli explore --resume`, o sistema MUST restaurar o segmento atual, grafo de segmentos e estoque do personagem exatamente como estavam.
- **FR-005**: "Sair da Masmorra" MUST desativar a sessão de exploração (comportamento existente preservado).
- **FR-006**: Ao executar `notecli explore` com sessão ativa existente, o sistema MUST perguntar se o jogador deseja retomar ou iniciar nova exploração.
- **FR-007**: Se o jogador escolher iniciar nova exploração, a sessão anterior MUST ser descartada.
- **FR-008**: O sistema MUST exibir mensagens distintas para "Salvar e Sair" (progresso salvo) e "Sair da Masmorra" (exploração encerrada).

### Key Entities

- **ExplorationSession** (existente): Campo `active` já indica se sessão está ativa. Nenhuma modificação necessária na estrutura — apenas no fluxo de CLI.
- **PlayerCharacter** (existente): Posição já é rastreada indiretamente via `segment_graph.current_segment_id` na sessão.
- **DungeonGraph** (existente): Já persiste segmentos, portas e estados. Nenhuma modificação estrutural necessária.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O personagem retorna ao segmento exato onde salvou em 100% das retomadas via `--resume`.
- **SC-002**: Os estados de todas as portas (abertas, trancadas, destrancadas) são preservados em 100% das retomadas.
- **SC-003**: O estoque de tochas do personagem é preservado em 100% das retomadas.
- **SC-004**: As mensagens de "Salvar e Sair" e "Sair da Masmorra" são claramente distintas em 100% das exibições.
- **SC-005**: Ao executar `notecli explore` com sessão ativa, a pergunta de retomar é exibida em 100% das execuções.

## Assumptions

- "Salvar e Sair" não altera o personagem — apenas pausa a sessão.
- Apenas uma sessão pode estar ativa por vez — salvar e sair substitui a sessão anterior se já existir uma.
- A retomada via `--resume` ou `notecli explore` funciona da mesma forma — a diferença é apenas no fluxo de confirmação.
- Não há limite de tempo para retomar uma sessão salva — ela persiste até ser substituída ou descartada.
