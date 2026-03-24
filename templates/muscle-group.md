---
name: {{name}}
volume_target_weekly: 12
importance: medium
---

# {{name}} Exercises

## Core Exercises

```dataview
table importance, equipment, last_performed
from "exercises"
where contains(muscle_groups, "{{name}}")
where importance = "core"
sort name
```

## Accessory Exercises

```dataview
table importance, equipment, last_performed
from "exercises"
where contains(muscle_groups, "{{name}}")
where importance = "accessory"
sort last_performed asc
```

## Volume Tracking

```dataview
table sum(rows.sets.length) as sets_this_week
from "logs"
where contains(muscle_groups, "{{name}}")
where date >= date(today) - dur(7 days)
group by true
```
