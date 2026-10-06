"""Growth OS CLI — a local-first runner for the workflows/ and agents/ prompts.

The prompts in workflows/ and agents/ are the actual asset. This package is just
the deterministic scaffolding around them: interview I/O, vault writes, and a
single stateless model call per run, agent-agnostic via subprocess.
"""

__version__ = "0.1.0"
