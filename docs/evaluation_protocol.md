# Evaluation protocol

- Evaluate on seed range 8100+ using the greedy action policy.
- Do not update Q-values, replay memory, world-model counts or semantic memory during evaluation.
- Track success rate, mean return and mean steps.
- Run more than one paired seed for exploratory algorithm comparisons.
- Report both matched seed pair differences and uncertainty. The 1.96·SE interval is normal-approximate and can be inaccurate for small samples.
- Prevent test contamination: use a disjoint final holdout seed family for confirmation after candidate selection.
- Reject claims of robust improvement without repeated controlled comparisons and evidence of retention.
