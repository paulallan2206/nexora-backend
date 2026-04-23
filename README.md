# Nexora — AI Chatbot SaaS Platform 🤖

<div align="center">

![Nexora Banner](https://img.shields.io/badge/Nexora-AI%20Chatbot%20SaaS-00e5ff?style=for-the-badge&labelColor=080810)
![Version](https://img.shields.io/badge/Version-4.0.0-9d6fff?style=for-the-badge&labelColor=080810)
![Python](https://img.shields.io/badge/Python-3.14+-00e5ff?style=for-the-badge&logo=python&labelColor=080810)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-9d6fff?style=for-the-badge&logo=fastapi&labelColor=080810)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-Powered-00e5ff?style=for-the-badge&labelColor=080810)
![License](https://img.shields.io/badge/License-MIT-00e676?style=for-the-badge&labelColor=080810)

**Plateforme SaaS de chatbot IA pour les PME africaines**

[🌐 Demo Live](https://nexora-ai-btob.onrender.com) · [📊 Dashboard](https://nexora-ai-btob.onrender.com/dashboard) · [📖 API Docs](https://nexora-ai-btob.onrender.com/docs)

</div>

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Stack technique](#-stack-technique)
- [Installation locale](#-installation-locale)
- [Configuration](#-configuration)
- [Déploiement](#-déploiement)
- [Structure du projet](#-structure-du-projet)
- [API Reference](#-api-reference)
- [Roadmap](#-roadmap)
- [Auteur](#-auteur)

---

## 🎯 À propos

**Nexora** est une plateforme SaaS complète qui permet à n'importe quelle entreprise africaine de déployer un assistant IA intelligent sur son site web en moins de 5 minutes — sans aucune compétence technique.

> *"L'IA ne devrait pas être réservée aux entreprises occidentales. Elle peut résoudre des problèmes concrets, ici, en Afrique."*

### Pourquoi Nexora ?

Des milliers de PME en Afrique perdent des clients chaque nuit faute de support disponible. Nexora répond à ce problème en offrant un assistant IA personnalisable, accessible 24h/24, qui :

- Répond aux questions fréquentes des clients
- Collecte automatiquement les leads (nom, email, téléphone)
- Présente les produits et services
- Prend des rendez-vous
- Notifie le propriétaire par email à chaque nouveau lead

---

## ✨ Fonctionnalités

### Pour les clients (PME)
- 🔐 **Inscription & Connexion** — Système d'authentification sécurisé avec tokens
- 🤖 **Configuration assistant** — Personnalisation nom, couleur, message d'accueil
- 📊 **Dashboard analytics** — Stats leads, conversations, activité en temps réel
- 🔗 **Widget intégrable** — Code prêt à copier-coller sur n'importe quel site
- 📧 **Notifications email** — Alerte instantanée à chaque nouveau lead
- 📁 **Knowledge Base** — Configuration du contenu via interface graphique

### Pour l'administrateur (vous)
- 📊 **Dashboard Admin** — Vue globale tous clients, graphiques, exports CSV
- 👥 **Gestion clients** — Liste de tous les abonnés avec leurs stats
- 💬 **Historique conversations** — Toutes les conversations par client
- ⚙️ **Configuration globale** — Gestion de la knowledge base par défaut

### Technique
- ⚡ **API REST FastAPI** — Documentation Swagger automatique sur `/docs`
- 🧠 **Mistral AI** — Modèle open source, sans dépendance à OpenAI
- 🗄️ **Supabase PostgreSQL** — Base de données temps réel
- 📨 **Resend API** — Emails transactionnels automatiques
- 🌍 **Multi-clients** — Chaque client a sa propre knowledge base isolée

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    NEXORA PLATFORM                       │
├─────────────────┬───────────────────┬───────────────────┤
│   Site Vitrine  │  Dashboard Client │  Dashboard Admin  │
│   index.html    │  dashboard.html   │   admin.html      │
│   register.html │  login.html       │                   │
└────────┬────────┴─────────┬─────────┴─────────┬─────────┘
         │                  │                   │
         └──────────────────▼───────────────────┘
                    FastAPI Backend
                      main.py
         ┌─────────────────────────────────────┐
         │           API Routes                │
         │  /chat  /leads  /subscribe          │
         │  /auth/register  /auth/login        │
         │  /client/me  /client/stats          │
         │  /client/knowledge  /admin/data     │
         └──────────┬──────────────┬───────────┘
                    │              │
          ┌─────────▼──────┐  ┌───▼──────────┐
          │   Mistral AI   │  │   Supabase   │
          │  mistral-tiny  │  │  PostgreSQL  │
          │   (chat IA)    │  │  (données)   │
          └────────────────┘  └──────────────┘
```

---

## 🛠️ Stack technique

| Composant | Technologie | Description |
|-----------|-------------|-------------|
| **Backend** | FastAPI 0.111 | Framework Python async haute performance |
| **IA** | Mistral AI (mistral-tiny) | Modèle de langage open source |
| **Base de données** | Supabase (PostgreSQL) | BDD temps réel avec API REST |
| **Frontend** | HTML / CSS / JavaScript | Vanilla JS, sans framework |
| **Emails** | Resend API | Emails transactionnels (3000/mois gratuit) |
| **Déploiement** | Render.com | Hébergement cloud avec CI/CD GitHub |
| **Versioning** | GitHub | Dépôt public open source |

---

## 💻 Installation locale

### Prérequis

- Python 3.11+
- Un compte [Mistral AI](https://console.mistral.ai) (gratuit)
- Un compte [Supabase](https://supabase.com) (gratuit)
- Un compte [Resend](https://resend.com) (optionnel, pour les emails)

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/paulallan2206/Nexora-AI.git
cd Nexora-AI

# 2. Créer un environnement virtuel
python -m venv venv

# 3. Activer l'environnement
# Windows
venv\Scripts\activate
# Mac / Linux
source venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt

# 5. Configurer les variables d'environnement
cp .env.example .env
# Remplir les valeurs dans .env

# 6. Lancer le serveur
uvicorn main:app --reload --port 8000
```

L'application est disponible sur **http://localhost:8000**

---

## ⚙️ Configuration

Créez un fichier `.env` à la racine du projet :

```env
# ── IA
MISTRAL_API_KEY=votre_clé_mistral

# ── Base de données Supabase
SUPABASE_URL=https://VOTRE_ID.supabase.co
SUPABASE_KEY=votre_clé_supabase_publique

# ── Admin Dashboard
ADMIN_PASSWORD=votre_mot_de_passe_admin_sécurisé

# ── Emails (optionnel)
RESEND_API_KEY=votre_clé_resend
FROM_EMAIL=noreply@votredomaine.com
```

### Tables Supabase à créer

```sql
-- Table clients (utilisateurs de la plateforme)
CREATE TABLE clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  client_id TEXT UNIQUE,
  email TEXT UNIQUE,
  password TEXT,
  company TEXT,
  plan TEXT DEFAULT 'starter',
  token TEXT,
  assistant_name TEXT,
  assistant_color TEXT DEFAULT '#00e5ff',
  welcome_msg TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table leads (contacts collectés par les chatbots)
CREATE TABLE leads (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT,
  email TEXT,
  phone TEXT,
  client_id TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table conversations (historique des chats)
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lead_id UUID,
  client_id TEXT,
  message TEXT,
  sender TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table subscribers (inscriptions via site vitrine)
CREATE TABLE subscribers (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE,
  subscribed_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🚀 Déploiement

### Sur Render.com (recommandé — gratuit)

1. Fork ou push ce dépôt sur votre GitHub
2. Créez un compte sur [render.com](https://render.com)
3. **New Web Service** → connectez votre repo GitHub
4. Configurez :

| Paramètre | Valeur |
|-----------|--------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |

5. Ajoutez les variables d'environnement dans **Environment** :
   - `MISTRAL_API_KEY`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `ADMIN_PASSWORD`
   - `RESEND_API_KEY` (optionnel)

6. Cliquez **Deploy** — en 3 minutes votre API est en ligne ✅

---

## 📁 Structure du projet

```
Nexora-AI/
│
├── main.py              # API FastAPI principale — toutes les routes
├── knowledge.json       # Knowledge base par défaut (démo hôtel)
│
├── index.html           # Site vitrine Nexora
├── register.html        # Page d'inscription client
├── login.html           # Page de connexion client
├── dashboard.html       # Dashboard client (config assistant, leads, widget)
├── admin.html           # Dashboard administrateur
│
├── requirements.txt     # Dépendances Python
├── Procfile             # Configuration Render/Heroku
├── .env.example         # Template variables d'environnement
│
└── README.md            # Ce fichier
```

---

## 📡 API Reference

| Méthode | Route | Description | Auth |
|---------|-------|-------------|------|
| `GET` | `/` | Site vitrine | Public |
| `GET` | `/health` | Status API + version | Public |
| `POST` | `/chat` | Envoyer un message au chatbot | Public |
| `POST` | `/leads` | Sauvegarder un lead | Public |
| `POST` | `/subscribe` | Inscription newsletter | Public |
| `POST` | `/auth/register` | Créer un compte client | Public |
| `POST` | `/auth/login` | Connexion client | Public |
| `GET` | `/client/me` | Infos du client connecté | Token |
| `GET` | `/client/stats` | Stats du client (leads, convs) | Token |
| `POST` | `/client/update` | Mettre à jour l'assistant | Token |
| `GET` | `/client/knowledge` | Lire la knowledge base | Token |
| `POST` | `/client/knowledge` | Mettre à jour la knowledge base | Token |
| `POST` | `/admin/login` | Connexion admin | Password |
| `GET` | `/admin/data` | Toutes les données (admin) | Admin Token |
| `GET` | `/docs` | Documentation Swagger interactive | Public |

### Exemple d'appel — Chat

```bash
curl -X POST https://nexora-ai-btob.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Bonjour, quels sont vos tarifs ?",
    "history": [],
    "client_id": "votre_client_id"
  }'
```

**Réponse :**
```json
{
  "reply": "Bonjour ! Nos chambres Standard sont à partir de 45 000 FCFA par nuit...",
  "session_id": "anon"
}
```

### Exemple — Inscription client

```bash
curl -X POST https://nexora-ai-btob.onrender.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "contact@monentreprise.com",
    "password": "motdepasse123",
    "company": "Mon Entreprise",
    "plan": "starter"
  }'
```

---

## 🗺️ Roadmap

- [x] API FastAPI + Mistral AI
- [x] Site vitrine dark luxury
- [x] Base de données Supabase
- [x] Système d'authentification clients
- [x] Dashboard client complet
- [x] Dashboard admin avec graphiques
- [x] Widget intégrable personnalisé
- [x] Emails automatiques (bienvenue + notification leads)
- [x] Knowledge Base configurable par client
- [ ] Intégration paiement Paydunya (Afrique)
- [ ] Widget multilingue (Français, Anglais, Fang, Lingala)
- [ ] Application mobile (React Native)
- [ ] Expansion Cameroun, Congo, Côte d'Ivoire
- [ ] Modèle IA fine-tuné sur les PME africaines

---

## 👤 Auteur

**Paul Allan Junior MEYE SIKA**

Étudiant en Licence 3 — Intelligence Artificielle & Business
SUP'RH School of Management and Artificial Intelligence · Libreville, Gabon

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Paul_Allan_Junior_MEYE_SIKA-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/paul-allan-junior-meye-sika)
[![GitHub](https://img.shields.io/badge/GitHub-paulallan2206-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/paulallan2206)

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

Conçu avec ❤️ à Libreville, Gabon 🇬🇦

**[nexora-ai-btob.onrender.com](https://nexora-ai-btob.onrender.com)**

</div>
