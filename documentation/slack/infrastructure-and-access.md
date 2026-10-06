# Infrastructure and Access

## Source control

- Canonical organization: Human Augment Analytics.
- Historical links may use `Porto-photogrammetry-` with a trailing dash; the repository was renamed in August 2026.
- Older `augenblick` repositories and forks are historical references, not necessarily the current source of truth.
- Syed Fahad Rizvi and Ihor Vilkhovyi received the requested repository access in August 2026.

## HiperGator

Use a federated UF Research Computing account sponsored by Arthur Porto. Open OnDemand is the preferred browser interface for interactive sessions.

### Storage

- Do not treat the login-node home quota as project storage.
- Use Blue storage under the `arthur.porto` allocation.
- RealityScan outputs were placed at `/blue/arthur.porto/data/datasets/photogrammetry/realityscan`.
- The cleaned Fall 2026 candidate dataset is at `/blue/arthur.porto/data/datasets/photogrammetry/neurips/raw`.
- Tab completion under `/blue` was reported as unreliable; an explicit `ls /blue/arthur.porto/` may work when completion does not.
- The Blue SMB hostname changed to `smb.rc.ufl.edu` in February 2026.

### Compute constraints

As of 1 September 2026, the `arthur.porto` group had limits of 64 CPUs and eight GPUs, and active jobs had consumed all GPUs and all but four CPUs. New COLMAP array jobs were pending with `QOSGrpCpuLimit`.

Arthur asked the active compute users to join the Biocosmos Slack workspace and use its HiperGator channel to coordinate resource use with the wider group. Syed was able to launch jobs by 4 September. This does not prove that the group limit is permanently resolved, so check the queue before scheduling arrays.

A known COLMAP job request used:

```bash
#SBATCH --account=arthur.porto
#SBATCH --partition=hpg-rtx6000
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --gpus=1
#SBATCH --mem=24gb
#SBATCH --time=1:00:00
#SBATCH --array=0-5
```

Request CPU-only nodes for package installation or other non-GPU work. GPU idle limits may terminate sessions before training begins.

On 16 September the team requested temporary access to an RTX PRO 6000, 16-32 CPUs, and 96 GB RAM for 7-10 days. Arthur noted that 32 CPUs represented half the allocation, so the team agreed to work with 16 and escalate if the requested resources remained unavailable after 24 hours.

## PACE

PACE was used throughout the project, including H200 experiments, but earlier constraints included limited GPU hours, build incompatibilities, and uncertainty about retained summer files during access transitions. The September 2026 question about whether previous PACE files would survive renewed access had no visible answer in the archived channel.

Om confirmed access to the PACE ICE cluster on 9 September. Each researcher should still verify their own account rather than assuming access is inherited from another team member.

Mohamed's access was verified on 11 September using the live SSH hostname `login-ice.pace.gatech.edu`; the older `pace-ice.pace.gatech.edu` hostname no longer resolved. His Slurm association is account `coc` with QOS `coc-ice`, and the canonical repository was cloned to personal scratch storage. No `/storage/ice-shared/coc-ice` directory was available, so a shared PACE dataset location remains unresolved.

Meeting 4 on 25 September reported that PACE had reduced a concurrent-job limit from 500 to 50 after excessive use. Treat this as a report to verify against the live scheduler rather than a permanent documented policy. The same meeting established two operating rules: use identical hardware for wall-clock comparisons, and ask Arthur to coordinate resource conflicts with the active users before any jobs are cancelled.

Om's Week 4 report identified two unstable L40S nodes, `atl1-1-03-004-21-0` and `atl1-1-03-004-23-0`, following uncorrectable ECC and pycolmap CUDA failures. Exclude them from submissions until their status is confirmed repaired.

## Environment strategy

- Pin Python, PyTorch, CUDA, compiler, and submodule versions.
- Prefer containers for reproducibility.
- Allow separate backend images or Conda environments when one environment cannot satisfy every method.
- Keep a CPU-safe test suite in continuous integration.
- Record GPU model, runtime, peak memory, and exact command for every benchmark.

## Data-access dependencies

- MorphoSource project-wide access was requested because many files require individual download permission.
- Museum contact Zach Randall joined the channel on 1 September. He noted that email may be a faster fallback if a Slack request goes unanswered.
- Eight existing photogrammetry objects reportedly have paired structured-light scans; the project requested all eight for short-term evaluation.
- The current 76-element prepared dataset with SAM 3 masks was reported at `/blue/arthur.porto/data/datasets/photogrammetry/neurips/prepared` on 22 September.
- Shareable dataset links should be treated as private operational data and kept out of public Git history.
