# Purchasing Manager

A multi-tenant web application for managing coffee purchasing operations — built with Flask and Firebase Firestore. Designed for small brokers and trading companies operating in the Brazilian coffee market.

## Features

- **Dashboard** — upcoming deliveries (next 15 days) and recent samples, plus live coffee market data (KC futures, USD/BRL)
- **Agreements** — create, edit, and print purchase/sale contracts with auto-numbered sequential IDs
- **Samples** — register coffee samples with quality attributes (sieve sizes, cup profiles, defects); auto-notify matching buyers via n8n webhook
- **Buyers** — maintain a buyer registry with purchase preferences (type, quantity, sieve, cup profile tolerances) for smart sample matching
- **Clients** — manage sellers and buyers with Brazilian address lookup (CEP)
- **Warehouses** — track origin and delivery warehouse locations
- **Multi-tenant** — data is scoped per tenant in Firestore; tenant logo is injected into every session
- **Auth** — Google OAuth 2.0 login via Authlib

## Tech Stack

| Layer | Technology |
|---|---|
| Web framework | Flask 3.x |
| Database | Firebase Firestore |
| Auth | Google OAuth 2.0 (Authlib) |
| Frontend | Bootstrap 5, Jinja2 templates |
| Automation | n8n webhook (buyer notifications) |
| Container | Docker |
| Deploy | Gunicorn |

## Project Structure

```
purchasing_manager/
├── controllers/   # Business logic
├── models/        # Firestore data access layer
├── routes/        # Flask blueprints (URL routing)
├── static/        # CSS, JS, images
└── templates/     # Jinja2 HTML templates
```

## Setup

### Prerequisites

- Python 3.12+
- A Firebase project with Firestore enabled
- A Google Cloud OAuth 2.0 client

### Local development

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. Add credentials:
   - Set `FIREBASE_CREDENTIALS` env var with your Firebase service account key JSON string.
   - Set `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` env vars from your Google OAuth client.

3. Configure environment variables (`.env`):

   ```env
   SECRET_KEY=your-flask-secret-key
   GOOGLE_CLIENT_ID=...
   GOOGLE_CLIENT_SECRET=...
   FIREBASE_CREDENTIALS=...
   N8N_WEBHOOK_URL=...         # optional, for buyer notifications
   ```

4. Run the app:

   ```bash
   flask --app purchasing_manager run
   ```

### Docker

```bash
docker build -t purchasing-manager .
docker run -p 5000:5000 \
  -e SECRET_KEY=... \
  -e GOOGLE_CLIENT_ID=... \
  -e GOOGLE_CLIENT_SECRET=... \
  -e FIREBASE_CREDENTIALS='...' \
  purchasing-manager
```

## Buyer Notification Flow

When a new sample is registered with "notify buyers" enabled, the app:

1. Queries all active buyers from Firestore.
2. Filters buyers whose preferences (coffee type, minimum quantity, sieve percentages, cup profile) match the sample.
3. Posts a webhook payload `{ sample, buyers }` to `N8N_WEBHOOK_URL` in a background thread.

The n8n workflow handles the actual WhatsApp/messaging delivery.

## Multi-Tenancy

All Firestore reads and writes go through `tenant_col(collection)`, which scopes documents under `tenants/{tenant_id}/{collection}`. The active tenant is resolved per request from the session and stored in Flask's `g`.
