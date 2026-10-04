# docker-jenkins-tp

Code source du TP du tutoriel **« Intégration de Docker avec Jenkins — Du
premier build à une pipeline CI/CD professionnelle »** (EFIlearn).

## Application de démonstration

Une application Flask volontairement minimale : le sujet du tutoriel est
l'intégration Jenkins + Docker, pas le framework applicatif.

- `GET /` → `Jenkins + Docker CI/CD Demo` / `Version: <APP_VERSION>`
- `GET /health` → `OK` (utilisé par les stages *Health Check* des pipelines)

```
app/
├── app.py
└── requirements.txt
Dockerfile
```

## Jenkinsfile principal

Le `Jenkinsfile` à la racine est la **pipeline professionnelle** du
Chapitre 9 : Checkout, Build & Unit Tests, Docker Build, Image Scan, Docker
Push, Deploy (SSH + Credentials), Health Check, Cleanup, avec blocs
`options`/`environment`/`parameters`/`post`.

C'est celui que référencent les chapitres Multibranch Pipeline et Webhook du
tutoriel (`Script Path: Jenkinsfile`).

## Autres Jenkinsfiles (`jenkinsfiles/`)

Chaque variante correspond à un chapitre ou à une section du tutoriel —
utile pour tester une méthode en particulier sans repartir de la pipeline
complète :

| Fichier | Chapitre | Méthode de déploiement |
|---|---|---|
| `Jenkinsfile.ch3-simple-build` | Chapitre 3 | Aucune — juste `docker build` + `docker images` |
| `Jenkinsfile.ch4-publish-over-ssh` | Chapitre 4 | Publish Over SSH (plugin) |
| `Jenkinsfile.tp-solution-a-publish-over-ssh` | TP final — Solution A | Publish Over SSH |
| `Jenkinsfile.tp-solution-b-ssh-credentials` | TP final — Solution B | SSH + Jenkins Credentials (`withCredentials`) |
| `Jenkinsfile.tp-solution-c-docker-remote-api` | TP final — Solution C | Docker Remote API sécurisée (TCP/TLS) |
| `Jenkinsfile.bonus-rollback` | Bonus — Rollback | SSH + Credentials, avec rollback automatique sur échec du Health Check |

## Valeurs à adapter

Tous les Jenkinsfiles utilisent les valeurs d'exemple du tutoriel — à
remplacer par les vôtres :

| Placeholder | Exemple utilisé | À remplacer par |
|---|---|---|
| `192.168.1.10` | Jenkins Controller | l'IP de votre Jenkins |
| `192.168.1.20` | Docker Server 1 (SSH) | l'IP de votre serveur de déploiement |
| `192.168.1.30` | Docker Server 2 (API distante) | l'IP de votre serveur Docker Remote API |
| `registry.example.com` | Registry générique | votre registry (Docker Hub, Harbor, GitLab...) |
| `docker-registry-credentials` | ID du Credential Jenkins pour le registry | l'ID que vous créez dans Manage Jenkins → Credentials |
| `docker-deploy-ssh` | ID du Credential Jenkins (clé SSH) | idem |
| `docker-prod` | Nom du serveur SSH déclaré dans Publish Over SSH | idem |

## Construire et tester l'image localement

```bash
docker build -t demo-app:local .
docker run --rm -p 8080:8080 demo-app:local
curl http://localhost:8080
curl http://localhost:8080/health
```

Voir le tutoriel complet pour le détail de chaque chapitre, les captures/
schémas d'interface Jenkins, le troubleshooting et les règles de sécurité.
