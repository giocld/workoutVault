---
name: Back
volume_target_weekly: 16
importance: high
---

# Back Exercises

## Core Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "back")
where importance = "core"
sort name
```

## Accessory Exercises

```dataview
table importance, equipment
from "exercises"
where contains(muscle_groups, "back")
where importance = "accessory"
sort last_performed asc
```

## Volume Tracking

```dataview
table sum(rows.sets.length) as sets_this_week
from "logs"
where contains(muscle_groups, "back")
where date >= date(today) - dur(7 days)
group by true
```
