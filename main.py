"""
Nexora v2.0 — FastAPI + Mistral + Supabase
Adapté aux vraies tables Supabase de Paul Allan Junior MEYE SIKA
Tables: leads (name,email,phone) | conversations (lead_id,message,sender) | subscribers (email)
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
import json, os, httpx
from datetime import datetime

app = FastAPI(title="Nexora API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
MISTRAL_URL     = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL   = "mistral-tiny"
SUPABASE_URL    = os.getenv("SUPABASE_URL", "https://wmhduwjkvbngmawzsgjb.supabase.co")
SUPABASE_KEY    = os.getenv("SUPABASE_KEY", "sb_publishable_k1P2HbAYmsuuQC7kkSj-Gg_CNPKDYQB")
ADMIN_PASSWORD  = os.getenv("ADMIN_PASSWORD", "nexora2025")

# ── KNOWLEDGE BASE
def load_knowledge():
    with open("knowledge.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_system_prompt(k):
    e = k["entreprise"]
    chambres = "\n".join(f"  - {c['type']} : {c['prix']} — {c['description']}" for c in k.get("chambres", []))
    services = "\n".join(f"  - {s}" for s in k.get("services", []))
    faq      = "\n".join(f"  Q: {f['question']}\n  R: {f['reponse']}" for f in k.get("faq", []))
    return f"""Tu es l assistant IA officiel de {e['nom']}, {e['type']} situe a {e['ville']}.
INFOS: Tel: {e['telephone']} | Email: {e['email']} | Horaires: {e['horaires']}
{k['description']}
CHAMBRES: {chambres}
SERVICES: {services}
FAQ: {faq}
REGLES: Reponds en francais, sans Markdown (pas de **, pas de #, pas de tirets listes).
Sois concis (max 3 phrases). Si reservation: collecte nom, email, telephone, dates, type chambre.
Sinon redirige vers {e['telephone']}. Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

# ── SUPABASE HELPERS
def supa_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

async def db_insert(table: str, data: dict):
    if not SUPABASE_URL or not SUPABASE_KEY:
        return None
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.post(
                f"{SUPABASE_URL}/rest/v1/{table}",
                headers=supa_headers(), json=data
            )
        return r.json() if r.status_code in [200, 201] else None
    except:
        return None

async def db_select(table: str, limit=50):
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(
                f"{SUPABASE_URL}/rest/v1/{table}?order=created_at.desc&limit={limit}",
                headers=supa_headers()
            )
        return r.json() if r.status_code == 200 else []
    except:
        return []

# Fallback mémoire
_leads, _convs, _subs = [], [], []

# ── ROUTES
@app.get("/")
def root(): return FileResponse("index.html")

@app.get("/admin")
def admin(): return FileResponse("admin.html")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "supabase": bool(SUPABASE_URL),
        "mistral": bool(MISTRAL_API_KEY)
    }

@app.post("/chat")
async def chat(req: Request):
    body    = await req.json()
    message = body.get("message", "").strip()
    history = body.get("history", [])
    session = body.get("session_id", "anon")

    if not message:
        return JSONResponse({"error": "Message vide"}, status_code=400)

    k    = load_knowledge()
    msgs = [{"role": "system", "content": build_system_prompt(k)}]
    for m in history[-10:]:
        msgs.append({"role": m["role"], "content": m["content"]})
    msgs.append({"role": "user", "content": message})

    try:
        async with httpx.AsyncClient(timeout=30) as c:
            r = await c.post(
                MISTRAL_URL,
                headers={"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"},
                json={"model": MISTRAL_MODEL, "messages": msgs, "max_tokens": 400, "temperature": 0.7}
            )
        reply = r.json()["choices"][0]["message"]["content"]

        # Sauvegarde message user dans conversations
        user_conv = {
            "lead_id": None,
            "message": message,
            "sender": "user"
        }
        bot_conv = {
            "lead_id": None,
            "message": reply,
            "sender": "bot"
        }
        saved_u = await db_insert("conversations", user_conv)
        saved_b = await db_insert("conversations", bot_conv)
        if not saved_u:
            _convs.append({**user_conv, "created_at": datetime.now().isoformat()})
            _convs.append({**bot_conv,  "created_at": datetime.now().isoformat()})

        return {"reply": reply, "session_id": session}

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/leads")
async def save_lead(req: Request):
    """
    Reçoit: {name, email, phone, message}
    Table leads: name, email, phone
    """
    b = await req.json()
    name  = b.get("name") or b.get("nom", "Inconnu")
    email = b.get("email", "")
    phone = b.get("phone") or b.get("telephone", "")

    lead = {"name": name, "email": email, "phone": phone}
    saved = await db_insert("leads", lead)
    if not saved:
        _leads.append({**lead, "created_at": datetime.now().isoformat()})

    # Si un message accompagne, on le sauvegarde en conversation
    if b.get("message"):
        conv = {"lead_id": None, "message": b.get("message"), "sender": "user"}
        await db_insert("conversations", conv)

    return {"status": "success", "message": f"Lead {name} enregistré !"}


@app.post("/subscribe")
async def subscribe(req: Request):
    """
    Reçoit: {email}
    Table subscribers: email
    """
    b = await req.json()
    email = b.get("email", "").strip()
    if not email or "@" not in email:
        return JSONResponse({"error": "Email invalide"}, status_code=400)

    sub = {"email": email}
    saved = await db_insert("subscribers", sub)
    if not saved:
        _subs.append({"email": email, "subscribed_at": datetime.now().isoformat()})

    return {"status": "success", "message": "Inscription enregistrée !"}


# ── ADMIN
@app.post("/admin/login")
async def admin_login(req: Request):
    b = await req.json()
    if b.get("password") == ADMIN_PASSWORD:
        return {"status": "ok", "token": "nexora-admin-2025"}
    return JSONResponse({"error": "Mot de passe incorrect"}, status_code=401)

@app.get("/admin/data")
async def admin_data(token: str = ""):
    if token != "nexora-admin-2025":
        return JSONResponse({"error": "Non autorisé"}, status_code=401)

    leads = await db_select("leads", 50)         or _leads
    convs = await db_select("conversations", 50) or _convs
    subs  = await db_select("subscribers", 50)   or _subs

    return {
        "stats": {
            "leads":         len(leads),
            "conversations": len(convs),
            "subscribers":   len(subs)
        },
        "leads":         leads[:20],
        "conversations": convs[:20],
        "subscribers":   subs[:10]
    }
