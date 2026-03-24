---
date: {{date}}
type: push
duration_minutes: 
---

# Workout - {{date}}

## Exercises

```dataview
table exercise, sets, notes
from "logs"
where date = "{{date}}"
sort file.name asc
```

## Volume by Muscle Group

```dataview
table sum(rows.sets.length) as sets
from "logs"
where date = "{{date}}"
flatten muscle_groups
group by muscle_groups
```

## Notes

