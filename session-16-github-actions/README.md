# Session 16: CI/CD with GitHub Actions

This directory contains short exercises for workflows, triggers, jobs,
runners, secrets, artifacts and a final build/test/container-delivery
pipeline. The dated README in this folder provides the topic notes; this
file links the runnable examples.

## Exercises

| Topic | Example |
| --- | --- |
| CI vs CD | [`01-ci-vs-cd/`](./01-ci-vs-cd%2010-33-34-211/) |
| Pipeline concepts | [`02-pipeline-concepts/`](./02-pipeline-concepts%2010-33-34-222/) |
| GitHub Actions introduction | [`03-github-actions-intro/`](./03-github-actions-intro%2010-33-34-226/) |
| Workflows and triggers | [`04-workflows/`](./04-workflows%2010-33-34-230/) |
| Jobs and steps | [`05-jobs-steps/`](./05-jobs-steps%2010-33-34-238/) |
| Runners | [`06-runners/`](./06-runners%2010-33-34-242/) |
| Secrets | [`07-secrets/`](./07-secrets%2010-33-34-248/) |
| Artifacts | [`08-artifacts/`](./08-artifacts%2010-33-34-260/) |
| Build and test | [`09-build-test-pipeline/`](./09-build-test-pipeline%2010-33-34-262/) |
| Final CI/CD demo | [`10-final-cicd-pipeline/`](./session-16-github-actions/10-final-cicd-pipeline/) |

The final demo is wired to this repository by the root workflow
[`session16-cicd.yml`](../.github/workflows/session16-cicd.yml). GitHub only
loads workflow definitions from the repository-root `.github/workflows/`
directory; the workflow file inside the teaching project is useful when that
project is copied into its own repository.

## Final pipeline

The active workflow runs tests and the repository's basic sensitive-file
check on pushes and pull requests that change the final demo. It builds a
Docker image on both event types and publishes to GHCR only for a push.

To run the app locally:

```bash
cd session-16-github-actions/session-16-github-actions/10-final-cicd-pipeline
python3 -m pip install -r requirements.txt
pytest -v
docker build -t session16-calculator:local .
docker run --rm -it session16-calculator:local
```

For this repository, the image is published as
`ghcr.io/<repository-owner>/session16-calculator:sha-<commit>`. Add no
registry password: the workflow uses its scoped `GITHUB_TOKEN`. The package
will only be visible according to the repository/package visibility settings.
Publishing the tested image to GHCR is the continuous-delivery handoff; the
calculator is an interactive CLI, so this demo does not deploy it as a
long-running Kubernetes service.

Inspect a run and capture real evidence from GitHub Actions:

```bash
gh run list --workflow=session16-cicd.yml
gh run view <run-id> --log
```

Do not describe an expected workflow result as a successful run until the
corresponding GitHub Actions job has actually completed.
