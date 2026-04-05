# Data Model: Save and Quit Dungeon

**Purpose**: Document data flow for save-quit feature
**Created**: 2026-04-05

## Data Flow

No new entities. Existing structures reused:

```
"Salvar e Sair":
  1. _save_session(graph) — persists DungeonGraph (segments, doors, current)
  2. _save_character(pc) — persists character (torches, HP, etc.)
  3. Session remains active=True
  4. Exit exploration loop

"Retomar via --resume ou explore":
  1. load_exploration() returns active session
  2. DungeonGraph.from_dict(session["segment_graph"])
  3. Restore current_segment_id, visited_stack
  4. Resume exploration_loop
```

## State Differences

| Action | Session Active | Segment Preserved | Character Preserved |
|--------|---------------|-------------------|---------------------|
| Salvar e Sair | ✅ True | ✅ Current segment | ✅ Torches, HP, etc. |
| Sair da Masmorra | ❌ False | ❌ Lost | ✅ Saved outside |
