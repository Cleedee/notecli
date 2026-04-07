# Quickstart: Enter Room After Opening Door

**Purpose**: Guide for testing enter-room-after-door feature
**Created**: 2026-04-05

## Prerequisites

```bash
uv sync
```

## Basic Usage

```bash
uv run notecli explore
```

## Opening a Door

```
🪜 Escadaria — Nível 1
   1 porta à frente.
   🔒 Porta 1: Fechada

> abrir 1

🎲 Rolagem: 5 — Porta Destrancada!
   ✅ Aberta → 🚶 Corredor (Nível 1)

Entrar no segmento? (s/n) > s

🚶 Corredor — Nível 1
   🔑 Você entra. Porta fecha atrás.
   2 portas à frente.
   🔒 Porta 1: Fechada
   🔒 Porta 2: Fechada
```

## Choosing Not to Enter

```
Entrar no segmento? (s/n) > n

🔒 Porta fecha.
```

## Already-Revealed Door

```
> abrir 1

Porta já revelada. Entrar? (s/n) > s

🚶 Corredor — Nível 1
   🔑 Você entra. Porta fecha atrás.
```

## Testing

```bash
uv run python -m unittest discover -s tests -v
```
