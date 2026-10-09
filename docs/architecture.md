# Architecture — executable vertical slice

1. `ProteusAgent.train()` creates deterministic GridWorld tasks indexed by episode.
2. The tabular policy selects an action (epsilon-greedy).
3. The environment returns next observation, reward and termination signal.
4. `ContinualLearner.observe()` performs an online TD update and optional random experience replay.
5. `WorldModel.observe()` records empirical transition frequencies.
6. `EpisodicMemory.add()` writes the transition to SQLite.
7. At checkpoints, Q-values and world-model counts are saved as checksummed JSON and atomic state JSON.
8. `evaluation.evaluate()` runs withheld seeds without calling any learning method.
9. `research.compare_replay()` uses matched seeds and equal training budgets to measure replay effects.
10. Code-execution, sensitive OS interaction and uncontrolled source modification are not allowed.

All files are Python source (`.py`), except docs and configuration. Python bytecode is checked with `compileall` and is not a native executable.
