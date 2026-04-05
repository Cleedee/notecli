# Contract: Segment Exploration CLI Interaction

**Purpose**: Define the CLI interaction contract for dungeon segment exploration
**Created**: 2026-04-05

## Command

```
notecli explore [--resume]
```

## Interaction Loop

After initial dungeon generation (type, name, entrance description), the player enters a segment exploration loop:

```
🪜 Escadaria — Nível 1
   1 porta à frente.

Ações: abrir <porta>, voltar, sair
> _
```

## Available Actions

| Action | Syntax | Description |
|--------|--------|-------------|
| Open door | `abrir <N>` | Opens door N (1-based index). Generates new segment if first time. |
| Backtrack | `voltar` | Returns to previous segment in visited stack. |
| Exit dungeon | `sair` | Attempts to exit if path to entrance is clear of monsters. |
| Help | `ajuda` | Shows available commands. |
| Status | `status` | Shows character and dungeon state. |

## Output Format

### Segment Display

```
[emoji] [SegmentType display name] — Nível [level]
   [doors_description]
   [connected_doors_info if any]
```

| SegmentType | Emoji | Display Name |
|-------------|-------|-------------|
| ESCADARIA | 🪜 | Escadaria |
| CORREDOR | 🚶 | Corredor |
| SALA | 🏛️ | Sala |
| SALA_FINAL | 🏆 | Sala Final |

### Door Descriptions

- 0 doors: `Nenhuma porta disponível — caminho sem saída.`
- 1 door: `1 porta à frente.`
- 2+ doors: `N portas à frente.`
- Some doors already opened: `Porta 1 → Corredor (já explorada)`

### Action Results

| Action | Success Output | Error Output |
|--------|---------------|--------------|
| `abrir 1` (new) | `🚪 Você abre a porta 1...\n\n[segment display]` | — |
| `abrir 1` (already opened) | `🚪 Porta 1 já foi aberta. Ela leva a: [segment description]` | — |
| `abrir X` (invalid door) | — | `⚠️ Porta X não existe. Este segmento tem N portas.` |
| `voltar` (has previous) | `🔙 Você retorna ao segmento anterior...\n\n[segment display]` | — |
| `voltar` (at entrance) | `Você está na entrada da masmorra.` + exit prompt | — |
| `sair` (path clear) | `⚠️ Caminho livre. Sair? (s/n)` → `🏁 Você sai da masmorra com vida.` | — |
| `sair` (monsters) | `⚠️ Há monstros no caminho até a entrada!` | — |
| `ajuda` | List of commands | — |
| Invalid input | — | `⚠️ Comando desconhecido. Digite 'ajuda' para ver as opções.` |

## Exit Codes

- `0`: Normal exit (player chose to leave)
- `1`: Error (corrupted save, invalid state)

## Error Handling

All error messages go to **stderr** with format:
```
⚠️ [error message in Portuguese]
```
