# Feature Specification: Enter Room After Opening Door

**Feature Branch**: `008-enter-room-after-door`
**Created**: 2026-04-05
**Status**: Draft
**Input**: User description: "Precisamos de uma opção na exploração para o personagem entrar na sala que ele acabou de abrir. Do contrário ele fica no mesmo segmento. Caso ele realize outra ação que não entrar no segmento, a porta será fechada. Caso ele entre, a porta será fechada igualmente."

## Door State Model

Uma porta possui três atributos independentes:

| Atributo | Valores | Descrição |
|----------|---------|-----------|
| **Visibilidade** | Fechada, Aberta | Se a porta está fisicamente aberta ou fechada |
| **Trava** | Trancada, Destrancada | Se a porta requer tocha para destrancar |
| **Armadilha** | Sim, Não | Se a porta possui armadilha ativa |

### Comportamento ao Tentar Abrir

1. **Porta Fechada + Trancada**: Permanece Fechada + Trancada. O jogador deve usar "Abrir Fechadura" (consome 1 tocha).
2. **Porta Fechada + Armadilha**: Armadilha é acionada. A porta revela o destino.
3. **Porta Fechada + Destrancada**: A porta abre, revela o destino, fica Aberta + Destrancada.

### Após Qualquer Ação Subsequente

- Após entrar no segmento revelado **ou** após escolher outra ação, a porta volta a **Fechada + Destrancada**.
- Não há nova rolagem — o destino já foi revelado ao jogador.
- Portas Trancadas e com Armadilha mantêm seus estados originais até resolução.

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Entrar na Sala Após Abrir Porta (Priority: P1)

Quando o jogador abre uma porta com sucesso (resultado Destrancada), o sistema oferece a opção de entrar no segmento revelado. Se o jogador escolhe entrar, ele se move para o novo segmento e a porta se fecha atrás (Fechada + Destrancada). Se o jogador escolhe outra ação (abrir outra porta, retroceder, etc.), a porta recém-aberta se fecha (Fechada + Destrancada) e o jogador permanece no segmento atual.

**Why this priority**: Sem esta opção, o jogador abre portas mas permanece sempre no mesmo segmento, sem progresso real na exploração.

**Independent Test**: Abrir uma porta Destrancada, escolher "entrar", verificar que o jogador está no novo segmento e a porta está Fechada + Destrancada. Abrir outra porta e escolher outra ação, verificando que a porta se fechou como Fechada + Destrancada.

**Acceptance Scenarios**:

1. **Given** que o jogador abriu uma porta Destrancada, **When** escolhe "entrar", **Then** o jogador se move para o novo segmento e a porta fica Fechada + Destrancada.
2. **Given** que o jogador abriu uma porta Destrancada, **When** escolhe outra ação, **Then** a porta fica Fechada + Destrancada e o jogador permanece no segmento atual.
3. **Given** que a porta está Fechada + Destrancada (já revelada), **When** o jogador interage com ela novamente, **Then** ele pode entrar sem nova rolagem.

---

### User Story 2 — Portas Trancadas e com Armadilha (Priority: P2)

Portas Trancadas não abrem sem destruir a fechadura (consome 1 tocha). Portas com Armadilha acionam o efeito ao abrir. Em ambos os casos, após qualquer ação subsequente, a porta se fecha mantendo seus atributos de trava e armadilha.

**Why this priority**: Define o comportamento correto para portas que não são Destrancada.

**Independent Test**: Tentar abrir porta Trancada — verificar que permanece Fechada + Trancada. Usar "Abrir Fechadura" — verificar que fica Aberta + Destrancada. Escolher outra ação — verificar que volta a Fechada + Destrancada.

**Acceptance Scenarios**:

1. **Given** que o jogador tenta abrir porta Fechada + Trancada, **When** usa "abrir", **Then** a porta permanece Fechada + Trancada e o sistema indica que precisa destruir a fechadura.
2. **Given** que o jogador destrancou uma porta com tocha, **When** a porta abre, **Then** fica Aberta + Destrancada e o destino é revelado.
3. **Given** que o jogador abriu porta com Armadilha, **When** o efeito da armadilha é aplicado, **Then** o destino é revelado e a porta fica Aberta.

---

### User Story 3 — Feedback Visual de Porta Fechando (Priority: P3)

O sistema deve informar claramente ao jogador quando uma porta se fecha, qual o estado resultante e se o destino já foi revelado.

**Independent Test**: Abrir porta e entrar — verificar mensagem de porta fechando com estado resultante.

**Acceptance Scenarios**:

1. **Given** que o jogador entrou no novo segmento, **When** a porta se fecha, **Then** o sistema exibe "Porta fechada — destino já revelado."
2. **Given** que o jogador escolheu outra ação após abrir porta, **When** a porta se fecha, **Then** o sistema exibe "Porta fechada."

---

### Edge Cases

- **Múltiplas portas abertas**: Se há várias portas Abertas + Destrancada no mesmo segmento, todas se fecham quando o jogador escolhe outra ação.
- **Voltar conta como outra ação**: Sim — todas as portas abertas se fecham.
- **Porta já revelada**: Interagir com porta Fechada + Destrancada (já revelada) permite entrar direto, sem rolagem.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Ao abrir uma porta com resultado Destrancada, o sistema MUST oferecer a opção de entrar no segmento revelado.
- **FR-002**: Se o jogador escolhe entrar, o sistema MUST mover o personagem para o novo segmento.
- **FR-003**: Após entrar ou escolher outra ação, a porta Aberta + Destrancada MUST voltar a Fechada + Destrancada.
- **FR-004**: Porta Fechada + Trancada NÃO abre ao usar "abrir" — permanece Fechada + Trancada até usar "Abrir Fechadura".
- **FR-005**: Após destruir fechadura (consome 1 tocha), a porta fica Aberta + Destrancada e o destino é revelado.
- **FR-006**: Porta com Armadilha aciona o efeito ao abrir e revela o destino.
- **FR-007**: Após qualquer ação subsequente, todas as portas Abertas + Destrancada voltam a Fechada + Destrancada.
- **FR-008**: Interagir com porta Fechada + Destrancada (já revelada) permite entrar sem nova rolagem.
- **FR-009**: O sistema MUST exibir mensagem informando que a porta se fechou após entrar ou escolher outra ação.
- **FR-010**: Portas Trancadas e com Armadilha mantêm seus atributos ao se fechar — apenas Destrancada alterna entre Aberta e Fechada.

### Key Entities

- **Door** (existente — modificar): Adicionar atributos `is_locked: bool` e `has_trap: bool`. Estado visual combina visibilidade + trava + armadilha.
- **Segment** (existente): Sem modificações.
- **DungeonGraph** (existente): current_segment_id muda ao entrar.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Após abrir porta Destrancada e escolher "entrar", o jogador está no novo segmento em 100% das tentativas.
- **SC-002**: A porta volta a Fechada + Destrancada após entrada em 100% das tentativas.
- **SC-003**: A porta volta a Fechada + Destrancada quando o jogador escolhe outra ação em 100% das tentativas.
- **SC-004**: Porta já revelada (Fechada + Destrancada) permite entrar sem rolagem em 100% das tentativas.
- **SC-005**: Porta Trancada não abre sem destruir fechadura em 100% das tentativas.
- **SC-006**: Mensagem de porta fechando é exibida em 100% dos fechamentos.

## Assumptions

- "Entrar" é uma opção adicional no menu que aparece após abrir uma porta Destrancada.
- Se há múltiplas portas abertas no mesmo segmento, todas se fecham se o jogador não entrar por nenhuma.
- O destino revelado é "lembrado" pelo jogador — mesmo com porta fechada, ele sabe para onde aquela porta leva.
- "Voltar" conta como "outra ação" — todas as portas abertas se fecham.
- Armadilha é acionada uma única vez — após acionada, o atributo `has_trap` pode ser removido.
