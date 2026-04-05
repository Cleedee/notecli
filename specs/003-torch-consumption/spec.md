# Feature Specification: Torch Consumption on Exploration Start

**Feature Branch**: `003-torch-consumption`
**Created**: 2026-04-04
**Status**: Draft
**Input**: User description: "No início da exploração uma tocha é acesa e o estoque é reduzido em um."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Consumir Tocha ao Iniciar Exploração (Priority: P1)

Ao iniciar uma sessão de exploração de masmorra, o sistema consome automaticamente uma tocha do estoque do personagem, acende a luz ambiente e exibe uma mensagem informando o jogador sobre a tocha acesa e o estoque restante.

**Why this priority**: Este é o único e central comportamento da funcionalidade — sem ele, a feature não existe.

**Independent Test**: Pode ser testado executando `notecli explore` e verificando que o estoque de tochas do personagem é reduzido em 1 e a luz é acesa após o início da exploração.

**Acceptance Scenarios**:

1. **Given** que o personagem possui 10 tochas, **When** a exploração é iniciada, **Then** o estoque é reduzido para 9, a luz é acesa e uma mensagem informativa é exibida.
2. **Given** que o personagem possui 1 tocha, **When** a exploração é iniciada, **Then** o estoque é reduzido para 0, a luz é acesa e uma mensagem alerta sobre o estoque esgotado é exibida.
3. **Given** que o personagem possui 0 tochas, **When** a exploração é iniciada, **Then** o estoque permanece em 0, a luz não é acesa e uma mensagem de aviso sobre a falta de tochas é exibida.

---

### Edge Cases

- O que acontece quando o estoque de tochas já está em 0 antes da exploração? O sistema exibe um aviso e inicia a exploração no escuro.
- A tocha é consumida mesmo se a sessão for retomada (`--resume`)? Não — o consumo ocorre apenas no início de uma nova exploração. Ao retomar, o estado existente é preservado.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST consumir exatamente 1 tocha do estoque do personagem ao iniciar uma nova sessão de exploração.
- **FR-002**: O sistema MUST ativar a luz (`light_on = True`) quando uma tocha é consumida com sucesso.
- **FR-003**: O sistema MUST exibir uma mensagem informativa ao jogador quando uma tocha é acesa, incluindo o estoque restante.
- **FR-004**: O sistema MUST exibir uma mensagem de aviso quando o personagem não possui tochas disponíveis ao iniciar a exploração.
- **FR-005**: O sistema NÃO MUST consumir tochas ao retomar uma sessão existente via `--resume`.
- **FR-006**: O estoque de tochas do personagem NÃO pode ser negativo (mínimo 0).

### Key Entities

- **PlayerCharacter (torches, light_on)**: Entidade existente. O campo `torches` é decrementado em 1 e `light_on` é definido como `True` ao iniciar exploração.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Ao iniciar uma exploração com tochas disponíveis, o estoque é reduzido em exatamente 1 unidade em 100% das execuções.
- **SC-002**: Ao iniciar uma exploração sem tochas, o sistema exibe um aviso claro e inicia no escuro em 100% das execuções.
- **SC-003**: O jogador consegue identificar o estoque restante de tochas a partir da mensagem exibida no terminal.

## Assumptions

- O consumo de tocha ocorre apenas no início de uma nova exploração, não em retomadas (`--resume`).
- O estoque máximo de tochas é 10 (limite já existente no `PlayerCharacter`).
- A mensagem de consumo de tocha segue o mesmo estilo visual das demais mensagens do `explore_menu`.
- Não há mecanismo de reacender tochas durante a exploração nesta feature — isso será tratado em feature futura.
