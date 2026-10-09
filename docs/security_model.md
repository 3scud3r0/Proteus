# Security boundaries

The internal GridWorld has no access to the host system. Tools are separate and available only through explicit CLI operations. Workspace resolves paths and denies traversal, absolute paths and symlink escapes. Shell and network access are denied regardless of tool requests. The arithmetic evaluator accepts a small allowlist of AST nodes and bounds depth/magnitude. Candidate improvement promotes *settings* only with explicit `Approval`.

Important limitation: filesystem path restrictions are not a hardened OS sandbox against concurrent adversaries / TOCTOU. There is no secure arbitrary generated Python execution. Do not feed untrusted code to the host Python interpreter; use an externally administered VM/container if expanding scope.
