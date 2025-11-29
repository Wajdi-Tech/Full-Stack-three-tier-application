# Full-Stack Three-Tier Application — Partie 1 (1 backend)

> Version : Frontend Next.js (Next 16) + Tailwind, Backend Express (Node 20), Postgres.
> Ce README explique comment builder localement, avec Docker, et déployer en local Kubernetes.

---

---

## Variables d'environnement importantes

**backend/.env**
PORT=4000
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=labdb

bash
Copier le code

**frontend/.env.local**
NEXT_PUBLIC_API_URL=http://localhost:4000

yaml
Copier le code

> ⚠️ Ne commente pas tes secrets dans le dépôt public — utilise un secret manager ou `.gitignore`.

---

## Docker (local)

### Build images
```bash
# depuis la racine du projet
docker build -t back-end:latest ./backend
docker build -t front-end:latest ./frontend
Lancer via docker-compose
bash
Copier le code
docker compose up --build



Appliquer manifests
kubectl apply -f . k8s/

Vérification
kubectl get pods -o wide
kubectl get svc
kubectl logs deployment/back-end
kubectl logs deployment/front-end

Tests rapides

API GET submissions:

curl http://<node-ip>:30080/api/submissions   # si backend exposé en NodePort (30080)



Captures d'écran

![Form submission](https://raw.githubusercontent.com/Wajdi-Tech/Full-Stack-three-tier-application/main/docs/screenshots/form.png)

![Liste pods soumissions](https://raw.githubusercontent.com/Wajdi-Tech/Full-Stack-three-tier-application/main/docs/screenshots/listpods.png)


