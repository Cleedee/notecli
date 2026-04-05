# Quickstart: Save and Quit Dungeon

**Purpose**: Guide for testing save-quit feature
**Created**: 2026-04-05

## Prerequisites

```bash
uv sync
```

## During Exploration

```
> salvar_e_sair

💾 Progresso salvo. Personagem permanece na masmorra.
   Execute 'notecli explore --resume' para continuar.
```

## Resume

```bash
uv run notecli explore --resume
# → Retoma diretamente do segmento salvo
```

## Prompt on Normal Explore

```bash
uv run notecli explore
# → "Sessão encontrada. Retomar? (r/n) > r"
#   → Retoma
# → ou "Sessão encontrada. Retomar? (r/n) > n"
#   → Descarta sessão antiga, gera nova masmorra
```

## Testing

```bash
uv run python -m unittest tests.test_save_quit -v
```
