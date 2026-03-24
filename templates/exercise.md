---
name: {{name}}
movement: {{movement}}
equipment: []
muscle_groups: []
importance: accessory
tags: []
image: {{filename}}.svg
related: []
last_performed: null
---

# {{name}}

![Exercise demonstration](../images/exercises/{{filename}}.svg)

## Setup

[Describe starting position and equipment setup]

## Execution

[Step-by-step movement instructions]

## Common Mistakes

- 
- 

## Safety Notes

-

## Related Exercises

{{#each related}}
- [[{{this}}]]
{{/each}}

## History

```dataview
table date, sets, notes
from "logs"
where exercise = "{{filename}}"
sort date desc
limit 10
```
