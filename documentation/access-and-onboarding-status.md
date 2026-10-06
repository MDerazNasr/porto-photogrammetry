# Access and Onboarding Status

**Last checked:** September 11, 2026

## Completed

- [x] Slack access to the private `#porto-photogrammetry` channel.
- [x] GitHub.com CLI authentication refreshed for `MDerazNasr`.
- [x] Canonical repository confirmed as `Human-Augment-Analytics/porto-photogrammetry`.
- [x] Canonical repository added locally as the `upstream` remote.
- [x] Current `upstream/main` checked out separately at `team-repo/` on local branch `team-main`.
- [x] All three declared Git submodules initialized.
- [x] Current repository architecture and PACE/HiperGator job documentation inspected.

## GitHub follow-up

- [ ] Obtain write permission to the organization repository or confirm that contributions should come from a GitHub fork.
- [ ] Do not push `team-main` until the expected contribution workflow is confirmed.
- [ ] The existing `MDerazNasr/photogrammetry` repository is not registered on GitHub as a fork of the team repository.

## PACE ICE

- [x] Install and connect the Georgia Tech GlobalProtect VPN.
- [x] Verify `mnasr34` as the correct GT username for PACE.
- [x] Test SSH access through the live host `login-ice.pace.gatech.edu`.
- [x] Confirm the `coc` SLURM account with `coc-ice` QOS.
- [x] Clone the canonical repository and submodules to `$HOME/scratch/porto-photogrammetry`.
- [x] Build the L40S environment at `$HOME/scratch/conda/augenblick_l40s` with the 2DGS and PGSR backends.
- [x] Verify the setup job completed successfully (`5759849`, exit code `0:0`, September 11, 2026).
- [x] Verify the `augenblick` CLI loads and lists the available SfM and reconstruction methods.
- [ ] Confirm access to project data or determine the shared PACE path.

Current blocker: `/storage/ice-shared/coc-ice` does not exist. The checkout is correctly placed in personal scratch storage, but no shared project dataset path has been identified on PACE.

## HiPerGator

- [x] Submit the UF federated-account request using Georgia Tech identity and Arthur Porto as sponsor.
- [x] Generate and upload a dedicated HiPerGator ED25519 public key.
- [ ] Receive sponsor approval and UF account-created confirmation email.
- [ ] After sponsor approval, test federated Open OnDemand at `https://ood.rc.ufl.edu`.
- [ ] Confirm membership in the `arthur.porto` allocation.
- [ ] Confirm access to `/blue/arthur.porto/data/datasets/photogrammetry/neurips/raw`.
- [ ] Join the Biocosmos Slack/HiperGator coordination channel if invited.

## MorphoSource and reference data

- [x] Sign in to MorphoSource and confirm access to project `000381689`.
- [x] Confirm partial access: some records are directly downloadable and others require individual permission.
- [ ] Ask Zach Randall whether Mohamed should receive project-wide rights or use the cleaned shared-storage copy.
- [ ] Confirm access to the final subset of the 42 shortlisted rigid specimens.
- [ ] Confirm whether the eight paired structured-light scans are already available in project storage.
- [ ] Obtain a MorphoSource API key only if direct downloads are required.
- [ ] Never commit an API key, private download URL, or data-use token.

## Local environment

- [x] Source code is available locally for reading.
- [x] Build the executable environment on PACE Linux/CUDA using an L40S GPU.
- [x] Use the repository's L40S setup wrapper for the selected GPU model.
- [x] Run a CPU-safe CLI smoke test before launching a reconstruction job.
- [ ] Obtain an approved project dataset and run a small end-to-end GPU smoke test.

### PACE environment evidence

- Environment: `$HOME/scratch/conda/augenblick_l40s`
- Repository: `$HOME/scratch/porto-photogrammetry`
- Setup job: `5759849` (`COMPLETED`, `0:0`, wall time `00:31:44`)
- Verified core components: PyTorch `2.9.1+cu130`, CUDA `13.0`, PyTorch3D, VGGT, COLMAP bindings, Open3D, 2DGS rasterizer, and PGSR rasterizer.
- Intentionally omitted: SuGaR/3DGS modules and tetrahedralization, because this first environment targets 2DGS and PGSR.
