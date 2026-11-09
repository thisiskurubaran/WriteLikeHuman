# Eval results

Each file here is a score summary from one run of `tests/run_evals.py --save <label>`, usually one per release (`v0.4.0.json`, `v0.4.1.json`, and so on).

A summary holds the date, the models used, the pass, fail, and skip counts, and pass or fail for each case. It never holds the prompts' answers, so nothing personal ends up here.

To compare two releases, open both files and look at `pass_rate` and at cases that changed from `true` to `false`. A drop usually points at a module or a router row that needs attention. These runs are a first pass. Trying a few cases in the Claude app is still the real test.
