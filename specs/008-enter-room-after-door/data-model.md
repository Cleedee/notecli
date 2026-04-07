# Data Model: Enter Room After Opening Door

**Purpose**: Define Door entity modifications for enter-room feature
**Created**: 2026-04-05

## Entity: Door (modified)

**Fields**:
- `is_open` (bool): Door is physically open?
- `is_locked` (bool): Door is locked?
- `has_trap` (bool): Door has active trap?
- `target_segment_id` (int | None): Target segment (set on first reveal)

**Validation**:
- `is_open` and `is_locked` can be True independently
- `target_segment_id` set when door first reveals destination

**State transitions**:
1. Try open (is_locked=True) → no change, message "trancada"
2. Pick lock (consume torch) → `is_open=True, is_locked=False`
3. Try open (has_trap=True) → trap triggered, `is_open=True, has_trap=False`
4. Try open (unlocked) → `is_open=True`
5. After action → `is_open=False` (door closes, keeps is_locked and has_trap)

## Display Table

| is_open | is_locked | has_trap | Display |
|---------|-----------|----------|---------|
| False | False | False | 🔒 Fechada |
| False | True | False | 🔐 Fechada + Trancada |
| False | False | True | ⚠️ Fechada + Armadilha |
| True | False | False | ✅ Aberta — entrar |

## Storage Format (backward compatible)

```json
{
  "index": 0,
  "is_open": false,
  "is_locked": false,
  "has_trap": false,
  "target_segment_id": 1
}
```

Migration: old `state` string maps to new booleans:
- `"fechada"` → `is_open=False, is_locked=False, has_trap=False`
- `"armadilha"` → `is_open=False, is_locked=False, has_trap=True`
- `"trancada"` → `is_open=False, is_locked=True, has_trap=False`
- `"destrancada"` → `is_open=True, is_locked=False, has_trap=False`
