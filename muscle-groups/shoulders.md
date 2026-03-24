---
name: Shoulders
volume_target_weekly: 12
importance: high
---

# Shoulder Exercises

## Core Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "shoulders")
where importance = "core"
sort name
```

## Accessory Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "shoulders")
where importance = "accessory"
sort last_performed asc
```

## Volume Tracking

```dataview
table sum(rows.sets.length) as sets_this_week
from "logs"
where contains(muscle_groups, "shoulders")
where date >= date(today) - dur(7 days)
group by true
```
