---
name: Chest
volume_target_weekly: 16
importance: high
---

# Chest Exercises

## Core Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "chest")
where importance = "core"
sort name
```

## Accessory Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "chest")
where importance = "accessory"
sort last_performed asc
```

## Volume Tracking

```dataview
table sum(rows.sets.length) as sets_this_week
from "logs"
where contains(muscle_groups, "chest")
where date >= date(today) - dur(7 days)
group by true
```
