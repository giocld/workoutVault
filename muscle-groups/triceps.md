---
name: Triceps
volume_target_weekly: 10
importance: medium
---

# Triceps Exercises

## Core Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "triceps")
where importance = "core"
sort name
```

## Accessory Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "triceps")
where importance = "accessory"
sort last_performed asc
```

## Volume Tracking

```dataview
table sum(rows.sets.length) as sets_this_week
from "logs"
where contains(muscle_groups, "triceps")
where date >= date(today) - dur(7 days)
group by true
```
