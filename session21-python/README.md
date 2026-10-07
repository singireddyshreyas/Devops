# Session 21 — DevOps Final Capstone: TaskBoard (Python)

## 1. What we are building

TaskBoard is a small but realistic SaaS-style project management application:

- React + Vite frontend
- Responsive HTML/JSX + CSS UI
- FastAPI Python backend
- PostgreSQL database
- SQLAlchemy ORM
- Alembic database migrations
- REST APIs
- Pytest automated tests
- Docker containers
- GitHub Actions CI/CD
- Trivy container security scanning
- GitHub Container Registry
- Terraform for AWS infrastructure
- AWS VPC + EKS
- Kubernetes
- Helm
- Ingress
- HPA
- Prometheus + Grafana
- Health/readiness endpoints
- Troubleshooting exercises

The point is not to teach isolated tools. The point is to show how a real application travels from a developer laptop to a monitored Kubernetes environment.

```text
Developer
   |
   v
Git / GitHub
   |
   v
GitHub Actions
   |-- pytest
   |-- frontend build
   |-- Docker build
   |-- Trivy scan
   `-- push images to GHCR
              |
              v
        Terraform
              |
       AWS VPC + EKS
              |
              v
            Helm
              |
      +-------+--------+
      |                |
   Frontend          Backend
    React            FastAPI
      |                |
      +-------> PostgreSQL
              |
       Prometheus
              |
           Grafana
```

---

## 2. Repository structure

```text
session21-devops-capstone-final/
├── frontend/                 # React application and CSS
├── backend/                  # FastAPI application
│   ├── app/                  # API, models, schemas, DB config
│   ├── tests/                # Pytest tests
│   └── alembic/              # DB migrations
├── docker-compose.yml        # Full local stack
├── terraform/                # AWS VPC + EKS infrastructure
├── helm/taskboard/            # Kubernetes package
├── k8s/                      # namespace/bootstrap manifests
├── monitoring/               # Prometheus/Grafana values
├── gitops/                   # Argo CD Application and workflow
├── troubleshooting/          # deliberately broken manifests
├── scripts/                  # load-test helpers
└── .github/workflows/        # CI/CD
```

---

# PART A — UNDERSTAND THE APPLICATION

## 3. Frontend

The frontend is intentionally closer to a real SaaS dashboard than a tutorial CRUD page.

It contains:

- dark sidebar
- workspace navigation
- dashboard header
- KPI cards
- task table
- status filters
- priority badges
- activity feed
- pipeline indicator
- create-task modal
- responsive CSS
- loading and backend-error states

The browser calls `/api/tasks` and `/api/tasks/stats`.

The browser does **not** need to know the internal backend hostname. Nginx and Kubernetes Ingress handle routing.

## 4. Backend

FastAPI exposes:

```text
GET    /
GET    /health
GET    /ready
GET    /metrics

GET    /api/tasks
GET    /api/tasks/{id}
POST   /api/tasks
PUT    /api/tasks/{id}
DELETE /api/tasks/{id}
GET    /api/tasks/stats
```

Swagger documentation is available at `/docs` when the backend is running.

### Why `/health`?

A container can be alive while its application is unhealthy. `/health` gives Kubernetes a cheap liveness check.

### Why `/ready`?

Readiness answers a different question: **can this application serve traffic now?** The endpoint verifies database access before returning READY.

### Why `/metrics`?

Prometheus needs machine-readable metrics. The FastAPI Prometheus instrumentator exposes request metrics for monitoring.

---

# PART B — RUN IT LOCALLY

## 5. Fastest method: Docker Compose

Requirements:

- Docker Desktop / Docker Engine
- Docker Compose

Set a throwaway local database password in your shell, then start the stack:

```bash
export POSTGRES_PASSWORD="$(openssl rand -hex 24)"
docker compose up --build
```

Open:

```text
http://localhost:3000
```

Backend:

```text
http://localhost:8000/docs
http://localhost:8000/health
http://localhost:8000/metrics
```

Stop:

```bash
docker compose down
```

Delete database volume too:

```bash
docker compose down -v
```

Clear the environment variable after stopping the stack:

```bash
unset POSTGRES_PASSWORD
```

---

## 6. Run backend directly

Requirements:

- Python 3.12+
- PostgreSQL

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set the database connection without putting a password in this repository:

```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=taskboard
export DB_USER=taskboard
read -rsp "Database password: " DB_PASSWORD
echo
```

Run migrations:

```bash
alembic upgrade head
```

Start FastAPI:

```bash
uvicorn app.main:app --reload --port 8000
```

After stopping the API, clear the password from the shell:

```bash
unset DB_PASSWORD
```

Test:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/tasks
```

Open:

```text
http://localhost:8000/docs
```

---

# PART C — TESTING

## 7. Pytest

```bash
cd backend
pytest -q
```

Students should understand why tests happen **before Docker images are pushed**.

```text
Bad code
  ↓
pytest fails
  ↓
Pipeline stops
  ↓
No broken image is promoted
```

This is the first quality gate.

---

# PART D — GIT AND GITHUB

## 8. Initialize Git

```bash
git init
git add .
git commit -m "initial TaskBoard application"
git branch -M main
git remote add origin <YOUR_GITHUB_REPO>
git push -u origin main
```

Explain:

- Git = version control
- GitHub = remote collaboration/source platform
- commit = immutable project checkpoint
- branch = isolated line of development
- pull request = controlled change review

---

# PART E — DOCKER

## 9. Backend Dockerfile

The backend image:

1. starts from Python
2. installs dependencies
3. copies Alembic
4. copies application code
5. creates a non-root user
6. exposes port 8000
7. runs migrations
8. starts Uvicorn

Build:

```bash
docker build -t taskboard-backend:local ./backend
```

Run with a reachable PostgreSQL instance:

```bash
docker run --rm -p 8000:8000 \
  -e DATABASE_URL='postgresql+psycopg://taskboard:taskboard@host.docker.internal:5432/taskboard' \
  taskboard-backend:local
```

## 10. Frontend Dockerfile

The frontend uses a multi-stage build:

```text
Node
  ↓
npm build
  ↓
static dist/
  ↓
Nginx runtime image
```

This keeps build tooling out of the final runtime image.

Build:

```bash
docker build -t taskboard-frontend:local ./frontend
```

---

# PART F — CI/CD

## 11. GitHub Actions pipeline

The workflow has three conceptual stages:

```text
TEST
 ↓
SAST + SCA + SECRET SCAN
 ↓
BUILD + CONTAINER SCAN + PUSH
 ↓
OPTIONAL HELM DEPLOY
```

### Test job

- checkout
- setup Python
- install requirements
- run pytest
- setup Node
- build React frontend

### Security jobs

- CodeQL analyzes the Python and JavaScript/TypeScript source.
- `pip-audit` and `npm audit` fail on dependency vulnerabilities.
- Gitleaks scans the Git history for accidentally committed secrets.

### Build/scan/push job

- build backend image
- build frontend image
- block on HIGH/CRITICAL Trivy findings
- push to GHCR on a push to `main`

The active root workflow is
[`../.github/workflows/session21-capstone.yml`](../.github/workflows/session21-capstone.yml).
It runs tests, CodeQL, Python/npm dependency audits and Gitleaks on pushes and
pull requests that touch this project. The standalone workflow in
[`.github/workflows/ci-cd.yml`](./.github/workflows/ci-cd.yml) also includes
the optional cluster deployment below when this folder is used as its own
repository.

In the monorepo, the root workflow can deploy only on a push to `main` and
only when the GitHub repository variable `TASKBOARD_DEPLOY_ENABLED` is set
to `true`. Configure these Actions secrets only if deploying to a cluster
you control:

- `KUBE_CONFIG_DATA`: base64-encoded kubeconfig for the target cluster.
- `POSTGRES_USERNAME` and `POSTGRES_PASSWORD`: database credentials.
- `GHCR_USERNAME` and `GHCR_READ_TOKEN`: a principal/token with read access
  to the private GHCR packages.

The workflow creates Kubernetes Secrets from these values; do not put
credentials in Helm values or commit them to Git.

The image tag is the Git commit SHA.

That means:

```text
commit A → image A
commit B → image B
commit C → image C
```

This gives traceability from production back to source code.

---

# PART G — SECURITY SCANNING

## 12. Trivy

The pipeline scans container images for HIGH and CRITICAL vulnerabilities.

A security scanner is not a magic guarantee of security. It is one automated control in the pipeline.

Students should understand:

```text
SAST
Dependency scanning
Secret scanning
Container scanning
Runtime security
```

These are different security layers.

---

# PART H — TERRAFORM

## 13. Why Terraform?

Kubernetes only manages workloads. It does not create the AWS network and EKS infrastructure in this project.

Terraform creates:

```text
AWS
 ├── VPC
 ├── public subnets
 ├── private subnets
 ├── NAT gateway
 └── EKS cluster
       └── managed worker nodes
```

Go to Terraform:

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

The default region is `ap-south-1`.

After EKS is created, configure kubectl using the command shown by AWS/Terraform output.

Destroy when finished:

```bash
terraform destroy
```

### Important teaching point

Terraform is **Infrastructure as Code**.

Instead of manually clicking:

```text
AWS Console → VPC → Subnet → EKS → Nodes...
```

we describe infrastructure in code and let Terraform reconcile the desired state.

---

# PART I — KUBERNETES

## 14. Namespace

```bash
kubectl apply -f k8s/namespace.yaml
```

A namespace provides logical isolation for the application.

## 15. Helm

Instead of maintaining many manually edited YAML files, Helm turns the Kubernetes deployment into a reusable package.

```bash
helm lint ./helm/taskboard
helm template taskboard ./helm/taskboard -n taskboard
```

Create the external database Secret before installing the chart. This avoids
storing credentials in `values.yaml` or a committed Secret manifest:

```bash
kubectl create namespace taskboard --dry-run=client -o yaml | kubectl apply -f -
read -rsp "Database password: " POSTGRES_PASSWORD
echo
kubectl create secret generic taskboard-postgres-credentials \
  --namespace taskboard \
  --from-literal=username=taskboard \
  --from-literal=password="$POSTGRES_PASSWORD"
unset POSTGRES_PASSWORD
helm upgrade --install taskboard ./helm/taskboard -n taskboard
```

The chart creates a ConfigMap, Deployments, Services, an HPA, probes and a
PostgreSQL PVC. The password remains in the external Secret, not in Helm
values. If the application images are private, create a namespace-scoped
GHCR pull Secret and set `imagePullSecrets` in the chart. In production, use
a managed secret provider and managed database.

Important Helm concepts:

- Chart
- values
- templates
- release
- upgrade
- rollback

---

# PART J — KUBERNETES COMPONENTS

## 16. Deployment

The Deployment manages backend/frontend Pods.

If a Pod dies:

```text
Deployment
   ↓
creates replacement Pod
```

## 17. Service

Pods are ephemeral. A Service provides stable networking.

```text
Frontend → backend Service → backend Pods
```

## 18. PostgreSQL

For the classroom/local Kubernetes demo, PostgreSQL is deployed inside the cluster with a PVC.

For production AWS architecture, students should understand the tradeoff between running PostgreSQL in Kubernetes and using a managed database such as Amazon RDS.

---

# PART K — INGRESS

## 19. Ingress

The application has two logical routes:

```text
/taskboard.local/
      ↓
React frontend

/taskboard.local/api
      ↓
FastAPI backend
```

Enable ingress with the dev values:

```bash
helm upgrade --install taskboard ./helm/taskboard \
  -n taskboard \
  -f helm/taskboard/values-dev.yaml
```

Students should understand that an Ingress resource is only configuration. An Ingress Controller must actually implement it.

---

# PART L — HPA

## 20. Horizontal Pod Autoscaler

The HPA can scale the backend based on CPU utilization.

```text
low traffic
   ↓
2 Pods

high CPU
   ↓
3 Pods
   ↓
4 Pods
   ↓
...
```

Inspect:

```bash
kubectl get hpa -n taskboard
```

HPA requires resource requests and a metrics provider such as Metrics Server.

A normal health request may not create enough CPU pressure to demonstrate scaling. For a classroom demo, use a controlled load generator and watch the metrics.

---

# PART M — MONITORING

## 21. Prometheus

Prometheus collects metrics from the FastAPI `/metrics` endpoint.

The ServiceMonitor tells the Prometheus Operator what to scrape.

## 22. Grafana

Grafana visualizes the collected metrics.

Useful questions:

- How many HTTP requests are arriving?
- Which endpoint is slow?
- Are errors increasing?
- Is the application receiving traffic?
- Is CPU increasing?
- Is HPA scaling?

---

# PART N — GITOPS

## 23. Argo CD

[`gitops/`](./gitops/) contains an Argo CD Application that watches the Helm
chart in this repository. Update its tested image SHA values through Git,
then observe Argo CD synchronize and self-heal the cluster. Create database
and image-pull Secrets out of band; never commit credentials.

---

# PART O — TROUBLESHOOTING LAB

## 24. Broken image

Apply:

```bash
kubectl apply -f troubleshooting/broken-image.yaml
```

Then:

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl get events --sort-by=.lastTimestamp
```

Expected investigation:

```text
ImagePullBackOff
      ↓
describe Pod
      ↓
wrong image/tag
      ↓
fix deployment
```

## 25. Broken Service

Apply:

```bash
kubectl apply -f troubleshooting/broken-service.yaml
```

Investigate:

```bash
kubectl get svc
kubectl get endpoints
kubectl get pods --show-labels
```

The key lesson is that a Service selects Pods using labels.

No matching labels = no endpoints = no traffic.

---

# PART P — FINAL DEMO

### 1. Application

Open TaskBoard and create a task.

### 2. API

Open FastAPI Swagger:

```text
/docs
```

Create/read/update/delete a task.

### 3. Database

Show the PostgreSQL `tasks` table.

### 4. Git

Make a small application change and commit it.

### 5. CI

Push to GitHub and show tests running.

### 6. Docker

Show the two images.

### 7. Security

Show Trivy scanning the images.

### 8. Registry

Show the images in GHCR.

### 9. Terraform

Show the AWS infrastructure code.

### 10. Kubernetes

```bash
kubectl get pods -n taskboard
kubectl get svc -n taskboard
```

### 11. Helm

```bash
helm list -n taskboard
```

### 12. Ingress

Open the application through the Ingress hostname.

### 13. HPA

```bash
kubectl get hpa -n taskboard
```

### 14. Monitoring

Show Prometheus and Grafana.

### 15. Failure simulation

Break a Service/image and troubleshoot it live.

---

# FINAL STUDENT PROJECT

Possible domains:

- CRM
- Inventory management
- Appointment booking
- Helpdesk
- Ecommerce administration
- Clinic management
- Restaurant management
- Employee management
- Learning management system

Minimum requirements:

### Application

- frontend
- backend
- PostgreSQL
- minimum 4 REST APIs
- responsive UI

### Engineering

- Git/GitHub
- automated tests
- Docker

### DevOps

- GitHub Actions
- security scan
- container registry
- Terraform
- Kubernetes
- Helm
- Ingress
- HPA
- Prometheus/Grafana

### Final presentation

Each student must demonstrate:

```text
Application
  ↓
Git commit
  ↓
CI pipeline
  ↓
Docker image
  ↓
Security scan
  ↓
Registry
  ↓
Terraform infrastructure
  ↓
Kubernetes deployment
  ↓
Helm
  ↓
Ingress
  ↓
Autoscaling
  ↓
Monitoring
  ↓
Troubleshooting
```

That is the actual objective of Session 21.

## Terminal proof

The screenshot records successful Helm chart linting and Docker Compose
configuration validation. It does not claim a live cluster or AWS deployment.

![Session 21 terminal validation](./proofs/terminal-validation.png)
