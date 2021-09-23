# Race condition in orignal procs.py

Thanks to reader Michael Albert who noticed the code I published during the Early Release had a race condition in `proc.py`.

If you are curious,
[this diff](https://github.com/fluentpython/example-code-2e/commit/2c1230579db99738a5e5e6802063bda585f6476d)
shows the bug and how I fixed it—but note that I later refactored
the example to delegate parts of `main` to the `start_jobs` and `report` functions.

The problem was that I ended the `while` loop that retrieved the results when the `jobs` queue was empty.
However, it was possible that the queue was empty but there were still processes working.
If that happened, one or more results would not be reported.
I did not notice the problem when I tested my original code,
but Albert showed that adding a `sleep(1)` call before the `if jobs.empty()` line made the bug occur frequently.
I adopted one of his solutions: have the `worker` function send back a `PrimeResult` with `n = 0` as a sentinel,
to let the main loop know that the process had completed, ending the loop when all processes were done.