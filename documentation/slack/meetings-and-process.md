# Meetings and Working Process

## Current cadence

The Fall 2026 recurring meeting was set for Fridays from 10:00 to 11:00 AM Eastern. Arthur Porto asked that at least some team members touch base with him every two weeks if the wider group also meets separately.

On 11 September Riyam confirmed that this group may continue meeting weekly and is therefore exempt from the proposed Museum unit-meeting and project-representative requirement. Researchers should continue submitting weekly time logs. Riyam was unavailable for the 11 September meeting and asked that administrative questions be tagged in Slack.

Meeting links changed across semesters. Use the current calendar invitation rather than historical Google Meet or Teams URLs preserved in Slack.

## Weekly reporting

Weekly reports are the primary progress record. A useful report should include:

- Work completed during the week.
- Evidence: outputs, metrics, screenshots, code, or literature reviewed.
- Impediments and failed experiments.
- Exact configurations and resource use when reporting benchmarks.
- Planned next steps.

The channel contains extensive report series from Syed Fahad Rizvi, Tianshu Wu, and Ihor Vilkhovyi. New reports should link to stable repository artifacts or shared storage rather than relying only on Slack uploads.

As of Meeting 4, Anthony's report bot finds attached weekly reports without a manager tag or keyword. The bot's displayed description briefly still mentioned tagging, but Anthony confirmed that text was outdated.

Meeting 4 also established publication-oriented homework: researchers should read recent dataset and benchmark papers and extract what makes their analyses compelling, especially ablations and method-specific failure analysis beyond a score table. The project dataset will need a public release; MorphoSource and Hugging Face are the current candidates, with repository requirements and ownership still to be decided.

## Communication norms

- Use threads for troubleshooting so resolutions remain attached to the original problem.
- Summarize decisions in the wiki rather than leaving them buried in long conversations.
- Post large data to project storage and share a stable path; do not use personal cloud storage as the long-term archive.
- Ask before treating a commercial output as ground truth.
- Include the method, pose source, masks, specimen, resolution, iterations, GPU, and commit when sharing results.
- Run wall-clock comparisons on the same hardware; otherwise label the numbers as operational observations rather than method comparisons.
- Keep public documentation free of private share tokens, email addresses, and verbatim private-channel transcripts.
- Merge the active Fall 2026 PRs in the announced dependency order: PR 19, PR 17, PR 20, then PR 18. The author of each later PR resolves conflicts against the updated main branch.

## Suggested meeting template

1. Compute and data-access blockers.
2. Results since the last meeting, with evidence.
3. Comparison validity: same images, masks, poses, and resource budget.
4. Decisions required.
5. Owners and deadlines.
6. Wiki and experiment-manifest updates.
