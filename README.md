
## README_part2.md (Deux backends : back-end1 Express middleware + back-end2 FastAPI DB)
# Full-Stack Three-Tier Application — Partie 2 (2 backends)

> Architecture :
> - Frontend Next.js (client)
> - **back-end1** (Express, Node 20) : middleware / proxy, exposé en **NodePort** (ex: 30080)
> - **back-end2** (FastAPI, Python 3.11) : service ClusterIP, parle avec Postgres
> - Postgres (StatefulSet)

---
## Variables d'environnement

**back-end1/.env**
PORT=4000
BACKEND2_URL=http://back-end2-service:5000


**back-end2/.env**
PORT=5000
DB_HOST=db-service
DB_PORT=5432
DB_USER=labuser
DB_PASSWORD=labpass
DB_NAME=labdb

**frontend/.env.local**
NEXT_PUBLIC_API_URL=http://<node-ip>:30080 # back-end1 NodePort

---

## Code résumé

- **back-end1** (Express) : reçoit `/api/submissions` et `/api/submit` du frontend, fait proxied requests vers `http://back-end2-service:5000/api/...` via `axios`.
- **back-end2** (FastAPI) : se connecte à Postgres via `asyncpg`, endpoints `/api/submissions` (GET) et `/api/submit` (POST).

(Le code complet est placé dans les dossiers `back-end1/` et `back-end2/`.)

---

## Docker (local)

### Build images

docker build -t back-end1:latest ./back-end1
docker build -t back-end2:latest ./back-end2
docker build -t front-end:latest ./frontend


Kubernetes — manifests importants

k8s/backends.yaml (extraits clés) :

back-end2 Deployment + Service (ClusterIP: back-end2-service, port 5000)

back-end1 Deployment + Service (NodePort: back-end1-service, nodePort 30080) — BACKEND2_URL=http://back-end2-service:5000

Appliquer :

kubectl apply -f k8s/postgres.yaml
kubectl apply -f k8s/backends.yaml
kubectl apply -f k8s/frontend.yaml   # si frontend dans cluster

Checks & debug

Vérifier pods :

kubectl get pods -o wide
kubectl logs deployment/back-end2
kubectl logs deployment/back-end1


Captures d'écran:

![Form](captures/form.png)
![Listpods](captures/listpods2.png)

