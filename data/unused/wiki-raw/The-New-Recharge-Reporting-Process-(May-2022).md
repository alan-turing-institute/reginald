This page documents the first run of the "new" process whereby REG's allocations to projects eventually end up in the Finance system. There are three steps (and several sub-steps that are not shown):

1. After month end, REG produce a "recharge _pro forma_" for the month

2. PMU sign off this pro forma.

3. Finance upload the allocations.

## 1. Recharge _pro forma_

1. Oliver created [`regolith`](https://github.com/alan-turing-institute/regolith), a Racket script for producing a monthly summary from Forecast.

2. James G used `regolith` to manually produce a _pro forma_ for April. That involved:
   - deleting all months other than April
   - deleting rows with no allocation
   - adding columns for PMU sign-off, proposed edits, and REG sign-off for the edits
   - adding an instructions sheet

3. James G asked Catherine L who from PMU should be REG's working contact.
