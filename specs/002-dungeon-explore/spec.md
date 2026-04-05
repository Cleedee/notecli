# Feature Specification: Dungeon Exploration Flow

**Feature Branch**: `002-dungeon-explore`
**Created**: 2026-04-04
**Status**: Draft
**Input**: User description: "O comando 'notecli explore' inicia uma nova masmorra. O tipo dela é escolhido aleatoriamente entre 6 tipos, após o qual o nome dela é gerada baseada no tipo e mais duas tabelas (O Templo ... da Dor ...Nebulosa). Aparece no terminal a descrição da entrada da masmorra (cada tipo tem uma descrição da entrada). Após isso, o jogador deve escolher um personagem pronto (caso não existe um novo será criado)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Iniciar Exploração de Masmorra (Priority: P1)

O jogador executa `notecli explore` e o sistema gera uma nova masmorra com tipo aleatório, nome composto e descrição de entrada. Em seguida, o sistema solicita que o jogador escolha um personagem existente ou crie um novo para iniciar a exploração.

**Why this priority**: Este é o fluxo principal e único da funcionalidade — sem ele, o comando `explore` não entrega valor algum.

**Independent Test**: Pode ser testado executando `notecli explore` e verificando se uma masmorra é gerada com tipo, nome e descrição visíveis, seguida da opção de selecionar ou criar personagem.

**Acceptance Scenarios**:

1. **Given** que não existem personagens salvos, **When** o jogador executa `notecli explore`, **Then** o sistema gera uma masmorra com tipo aleatório, nome composto e descrição de entrada, e em seguida cria automaticamente um novo personagem.
2. **Given** que existem personagens salvos, **When** o jogador executa `notecli explore`, **Then** o sistema gera uma masmorra com tipo aleatório, nome composto e descrição de entrada, e exibe um menu para o jogador escolher um personagem existente ou criar um novo.
3. **Given** que o jogador escolheu ou criou um personagem, **When** a seleção é confirmada, **Then** o sistema exibe uma mensagem de início de exploração com o nome do personagem e informações da masmorra.

---

### User Story 2 - Visualizar Informações da Masmorra Gerada (Priority: P2)

O jogador vê no terminal o tipo da masmorra, o nome gerado a partir de tabelas e a descrição da entrada correspondente ao tipo.

**Why this priority**: Fornece feedback imediato e imersivo ao jogador sobre o ambiente que irá explorar.

**Independent Test**: Pode ser testado executando `notecli explore` e verificando que as informações da masmorra (tipo, nome, descrição) são exibidas corretamente no terminal.

**Acceptance Scenarios**:

1. **Given** que o jogador executou `notecli explore`, **When** a masmorra é gerada, **Then** o tipo é exibido como um dos 6 tipos disponíveis.
2. **Given** que a masmorra foi gerada, **When** o nome é composto, **Then** segue o padrão "[Artigo] [Substantivo] ... [Preposição] ... [Adjetivo]" (ex: "O Palácio da Dor Nebulosa").
3. **Given** que a masmorra tem um tipo definido, **When** a descrição de entrada é exibida, **Then** corresponde ao tipo sorteado.

---

### User Story 3 - Selecionar Personagem Existente (Priority: P3)

Quando existem personagens salvos, o jogador pode escolher um deles para explorar a masmorra.

**Why this priority**: Permite reutilização de personagens existentes, mas não bloqueia o fluxo principal (um novo pode ser criado automaticamente).

**Independent Test**: Pode ser testado salvando um personagem via `notecli character` e então executando `notecli explore` para verificar que o menu de seleção aparece e o personagem escolhido é associado à exploração.

**Acceptance Scenarios**:

1. **Given** que existem 2 ou mais personagens salvos, **When** o jogador executa `notecli explore`, **Then** um menu numerado é exibido com os nomes e ancestrais de cada personagem.
2. **Given** que o menu de seleção foi exibido, **When** o jogador escolhe um número válido, **Then** esse personagem é selecionado para a exploração.
3. **Given** que o menu de seleção foi exibido, **When** o jogador escolhe a opção "Criar novo personagem", **Then** um novo personagem é gerado automaticamente.

---

### Edge Cases

- O que acontece quando o jogador fornece uma opção inválida no menu de seleção? O sistema deve exibir uma mensagem de erro e solicitar novamente.
- Como o sistema lida com falha ao carregar personagens salvos? Deve fallback para criação automática de novo personagem.
- O que acontece se o arquivo de personagens estiver corrompido? O sistema deve informar o erro e criar um novo personagem automaticamente.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema MUST sortear aleatoriamente um tipo de masmorra entre 6 tipos pré-definidos ao executar `notecli explore`. Os tipos são: Palácio, Cripta, Tumba, Santuário, Templo e Calabouço.
- **FR-002**: O sistema MUST gerar um nome composto para a masmorra combinando elementos de três tabelas (artigo + substantivo + preposição + adjetivo, ou padrão equivalente).
- **FR-003**: O sistema MUST exibir a descrição de entrada correspondente ao tipo de masmorra sorteado.
- **FR-004**: O sistema MUST verificar se existem personagens salvos ao iniciar a exploração.
- **FR-005**: O sistema MUST exibir um menu de seleção de personagem quando existem personagens salvos, permitindo escolher um existente ou criar um novo.
- **FR-006**: O sistema MUST criar automaticamente um novo personagem quando não existem personagens salvos.
- **FR-007**: O sistema MUST associar o personagem selecionado ou criado à sessão de exploração da masmorra.
- **FR-008**: O sistema MUST validar a entrada do jogador no menu de seleção, repetindo a solicitação em caso de opção inválida.
- **FR-009**: O sistema MUST persistir o estado da exploração atual para recuperação em caso de interrupção.

### Key Entities

- **Dungeon**: Representa uma masmorra gerada. Possui tipo (um entre 6), nome composto (string gerada a partir de tabelas), descrição de entrada (texto associado ao tipo) e estado atual de exploração.
- **DungeonType**: Enum com os 6 tipos de masmorra. Cada tipo possui uma descrição de entrada única.
- **DungeonNameTable**: Tabelas de geração de nomes compostos, com artigos, substantivos, preposições e adjetivos temáticos.
- **ExplorationSession**: Representa uma sessão ativa de exploração, vinculando uma Dungeon a um PlayerCharacter.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O jogador vê as informações da masmorra (tipo, nome, descrição) no terminal em menos de 1 segundo após executar `notecli explore`.
- **SC-002**: O sistema gera nomes de masmorra válidos e coerentes em 100% das execuções.
- **SC-003**: O jogador consegue selecionar ou criar um personagem e iniciar a exploração em menos de 3 interações com o terminal.
- **SC-004**: 95% dos jogadores conseguem completar o fluxo de início de exploração sem erros ou confusão na primeira tentativa.

## Assumptions

- Os 6 tipos de masmorra já estão definidos ou serão definidos em uma tabela semelhante à de ancestrais.
- As tabelas de geração de nomes (artigos, substantivos, preposições, adjetivos) serão fornecidas como parte desta feature ou em feature relacionada.
- O sistema de persistência de personagens (`~/.notecli/characters.json`) já está funcional e será reutilizado.
- A criação automática de personagem segue o mesmo fluxo do comando `notecli character` já existente.
- O terminal suporta exibição de texto e interação via input padrão (stdin/stdout).
- Não há suporte a interface gráfica — toda interação é via linha de comando.
