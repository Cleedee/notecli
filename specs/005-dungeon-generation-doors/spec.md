# Feature Specification: Dungeon Pre-Generation and Door Mechanics

**Feature Branch**: `005-dungeon-generation-doors`
**Created**: 2026-04-05
**Status**: Draft
**Input**: User description: "A tocha não é consumida toda vez que o personagem entra em um novo segmento. A Sala Final não pode ser encontrada sem que todas as portas tenham sido abertas. Então, seria melhor o jogo gerar toda a dungeon e, nosso processo, a Sala Final seria criada também. Abrir porta é uma ação que pode revelar: 1 - ativou Armadilha, 2 e 3 - Trancada, 4 a 6: Destrancada. Porta Trancada habilita a ação de Abrir Fechadura que destranca a porta e consome uma tocha. Cada tipo de masmorra tem uma tabela própria de Armadilhas em Portas com 6 entradas informando a armadilha que foi acionada ou mesmo se nada acontece. Essas entradas serão implementadas posteriormente."

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Gerar Masmorra Completa Antes da Exploração (Priority: P1)

Ao iniciar uma exploração, o sistema gera toda a masmorra de uma vez, incluindo a Sala Final, antes do jogador começar a explorar portas. A Sala Final é o último segmento acessível da masmorra gerada.

**Why this priority**: Sem a geração completa, não há como garantir que a Sala Final exista ou que todas as portas possam ser abertas. Esta é a base para todas as outras mecânicas.

**Independent Test**: Executar `notecli explore` e verificar que a masmorra é gerada por completo antes da primeira interação do jogador, com a Sala Final presente.

**Acceptance Scenarios**:

1. **Given** que uma nova exploração é iniciada, **When** a masmorra é gerada, **Then** todos os segmentos são criados e a Sala Final é posicionada como destino de um dos segmentos finais.
2. **Given** que a masmorra foi gerada por completo, **When** o jogador começa a explorar, **Then** a Sala Final já existe e está acessível através de uma cadeia de portas.
3. **Given** que a masmorra foi gerada, **When** o jogador verifica a descrição, **Then** o sistema exibe o nome da masmorra e o tipo da entrada.

---

### User Story 2 — Mecânica de Abrir Porta com Resultado Aleatório (Priority: P2)

Ao abrir uma porta, o sistema revela o estado da porta com uma rolagem: 1 = Armadilha acionada, 2-3 = Porta Trancada, 4-6 = Porta Destrancada. Portas destrancadas revelam o segmento conectado. Portas trancadas exigem a ação adicional de Abrir Fechadura.

**Why this priority**: Esta é a mecânica central de interação com a masmorra — substitui a geração incremental anterior por um sistema de descoberta progressiva com risco.

**Independent Test**: Abrir uma porta e verificar que o resultado segue a distribuição: 1/6 armadilha, 2/6 trancada, 3/6 destrancada.

**Acceptance Scenarios**:

1. **Given** que o jogador escolhe abrir uma porta, **When** a rolagem é 1, **Then** uma armadilha é acionada e o segmento conectado é revelado.
2. **Given** que o jogador escolhe abrir uma porta, **When** a rolagem é 2 ou 3, **Then** a porta é revelada como trancada e a ação "Abrir Fechadura" fica disponível.
3. **Given** que o jogador escolhe abrir uma porta, **When** a rolagem é 4, 5 ou 6, **Then** a porta é destrancada e o segmento conectado é revelado.
4. **Given** que uma porta foi aberta (trancada ou destrancada), **When** o jogador tenta abrir a mesma porta novamente, **Then** o sistema exibe o segmento já revelado sem nova rolagem.

---

### User Story 3 — Abrir Fechadura Consome Tocha (Priority: P3)

Quando uma porta está trancada, o jogador pode usar a ação "Abrir Fechadura" para destrancá-la. Esta ação consome exatamente 1 tocha do estoque do personagem.

**Why this priority**: Adiciona custo estratégico à exploração — o jogador deve decidir se vale a pena gastar uma tocha para acessar um segmento.

**Independent Test**: Com uma porta trancada e tochas disponíveis, abrir a fechadura e verificar que 1 tocha é consumida.

**Acceptance Scenarios**:

1. **Given** que uma porta está trancada e o personagem tem 1+ tochas, **When** o jogador usa "Abrir Fechadura", **Then** a porta é destrancada, 1 tocha é consumida e o segmento é revelado.
2. **Given** que uma porta está trancada e o personagem tem 0 tochas, **When** o jogador tenta "Abrir Fechadura", **Then** o sistema exibe aviso de que não há tochas e a porta permanece trancada.
3. **Given** que uma porta já foi destrancada, **When** o jogador tenta "Abrir Fechadura" novamente, **Then** o sistema informa que a porta já está destrancada sem consumir tocha.

---

### User Story 4 — Tabelas de Armadilhas por Tipo de Masmorra (Priority: P4)

Cada um dos 6 tipos de masmorra (Palácio, Cripta, Tumba, Santuário, Templo, Calabouço) possui sua própria tabela de armadilhas com 6 entradas. Quando uma armadilha é acionada, a tabela correspondente ao tipo da masmorra é usada para determinar qual armadilha foi ativada.

**Why this priority**: Fornece variedade temática entre tipos de masmorra, mas as entradas serão implementadas posteriormente — nesta feature, apenas a estrutura é criada.

**Independent Test**: Acionar uma armadilha em cada tipo de masmorra e verificar que a tabela correta é consultada.

**Acceptance Scenarios**:

1. **Given** que o jogador aciona uma armadilha em um Palácio, **When** a tabela de armadilhas é consultada, **Then** a tabela específica do Palácio é usada.
2. **Given** que uma entrada de armadilha indica "nada acontece", **When** a armadilha é acionada, **Then** o sistema exibe que nada de ruim aconteceu.
3. **Given** que as entradas de armadilha serão implementadas posteriormente, **When** uma armadilha é acionada, **Then** o sistema exibe uma mensagem genérica de placeholder.

---

### Edge Cases

- O que acontece quando o jogador está sem tochas e encontra uma porta trancada? O jogador não pode abrir a fechadura e deve buscar outro caminho ou retroceder.
- A Sala Final é acessível mesmo se houver portas trancadas no caminho? Sim — o jogador precisa destrancar todas as portas no caminho até a Sala Final.
- A masmorra pode gerar caminhos sem saída? Sim — nem todos os segmentos levam à Sala Final.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST gerar toda a masmorra antes do jogador iniciar a exploração.
- **FR-002**: A Sala Final MUST ser gerada como parte da geração completa da masmorra, não durante a exploração incremental.
- **FR-003**: O sistema NÃO MUST consumir tochas ao entrar em um novo segmento — apenas ao abrir fechaduras.
- **FR-004**: Ao abrir uma porta, o sistema MUST realizar uma rolagem de d6: 1 = Armadilha, 2-3 = Trancada, 4-6 = Destrancada.
- **FR-005**: Quando uma porta é trancada, a ação "Abrir Fechadura" MUST ficar disponível para o jogador.
- **FR-006**: A ação "Abrir Fechadura" MUST consumir exatamente 1 tocha do estoque do personagem.
- **FR-007**: Se o jogador não possui tochas, a ação "Abrir Fechadura" MUST exibir aviso e não consumir tochas.
- **FR-008**: Cada tipo de masmorra MUST possuir sua própria tabela de armadilhas com exatamente 6 entradas.
- **FR-009**: Quando uma armadilha é acionada, o sistema MUST consultar a tabela correspondente ao tipo da masmorra atual.
- **FR-010**: Portas já abertas (trancadas ou destrancadas) NÃO MUST gerar nova rolagem ao serem interagir novamente.
- **FR-011**: O jogador MUST poder abrir fechaduras apenas em portas que estão no estado "Trancada".
- **FR-012**: O sistema MUST rastrear o estado de cada porta: Fechada, Armadilha, Trancada, Destrancada.

### Key Entities

- **Door**: Representa uma porta entre segmentos. Possui estado (Fechada, Armadilha, Trancada, Destrancada), resultado da rolagem, e referência ao segmento de destino.
- **DoorState**: Enum com 4 valores: FECHADA, ARMADILHA, TRANCADA, DESTRANCADA.
- **TrapTable**: Tabela com 6 entradas por tipo de masmorra. Cada entrada descreve a armadilha acionada (a ser implementada futuramente).
- **Dungeon**: Coleção de segmentos conectados por portas. Gerada por completo antes da exploração.

### Key Entities — Modificações em Entidades Existentes

- **Segment**: Agora contém uma lista de `Door` objects (ao invés de `connected_segments` simples).
- **PlayerCharacter**: Campo `torches` não é mais decrementado ao entrar em segmento — apenas ao abrir fechaduras.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A masmorra completa é gerada em menos de 100ms ao iniciar a exploração em 100% das execuções.
- **SC-002**: A Sala Final está presente e acessível em 100% das masmorras geradas.
- **SC-003**: Tochas são consumidas apenas ao abrir fechaduras (não ao entrar em segmentos) em 100% das interações.
- **SC-004**: A distribuição de resultados de porta segue a especificação (1/6 armadilha, 2/6 trancada, 3/6 destrancada) dentro de 5% de margem estatística após 100 rolagens.
- **SC-005**: Cada tipo de masmorra consulta sua tabela de armadilhas correta em 100% dos acionamentos.

## Assumptions

- As 6 tabelas de armadilhas terão 6 entradas cada, selecionadas por rolagem de d6. As entradas serão implementadas em feature futura — por enquanto, são placeholders.
- O jogador pode abrir uma porta por vez, escolhendo qual porta abrir quando há múltiplas.
- "Abrir Fechadura" destranca a porta e revela o segmento conectado — não há falha na tentativa de abrir fechadura (sempre funciona se houver tocha).
- A Sala Final é garantida em cada masmorra gerada — não há masmorras sem saída.
- Não há limite de tentativas para abrir fechaduras — o jogador pode tentar enquanto tiver tochas.
