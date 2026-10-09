# Learning protocol

At state s with action a, observed reward r and next state s', Q-learning uses:

Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') − Q(s,a)]

For terminal transitions, the future term is zero. The replay buffer samples previously observed transitions, applying a smaller learning-rate multiplier. A curiosity exploration bonus is available but defaults to zero for an interpretable control group. Exploration epsilon is reduced after each episode.

The empirical world model stores frequencies N(s,a,s'). It estimates the most likely next observation and its empirical confidence. It is not yet used for model-based planning in the main training loop; independent planner functions are available for follow-on experiments.

Critically: the system learns from data while running, but the specific toy task does not demonstrate open-ended intelligence. Generalization must be measured on held-out environments.
