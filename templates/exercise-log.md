---
date: {{date}}
exercise: {{exercise}}
muscle_groups: []
type: push
sets: []
notes: ""
---

# {{exercise}} - {{date}}

## Previous Session

```dataview
table date, sets, notes
from "logs"
where exercise = "{{exercise}}"
where date < "{{date}}"
sort date desc
limit 1
```

## Today's Sets

| Set | Reps | Weight (kg) | RPE | Notes |
|-----|------|-------------|-----|-------|
| 1   |      |             |     |       |
| 2   |      |             |     |       |
| 3   |      |             |     |       |
| 4   |      |             |     |       |

## Exercise Reference

[[{{exercise}}]]
