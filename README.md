# Demo Inventory API — Bits Code Test App

API Flask minimaliste pour tester **Datadog Bits Code**.  
Elle contient **4 bugs intentionnels** qui génèrent des erreurs réelles dans Datadog.

---

## Lancement rapide

```bash
pip install -r requirements.txt

# Sans Datadog APM (local uniquement)
python app/api.py

# Avec Datadog APM (recommandé pour tester Bits Code)
DD_SERVICE=demo-inventory-api \
DD_ENV=dev \
DD_VERSION=1.0.0 \
DD_AGENT_HOST=localhost \
ddtrace-run python app/api.py
```

## Déclencher les bugs

```bash
python tests/trigger_bugs.py
```

## Lancer les tests unitaires

```bash
pytest tests/test_api.py -v
```

Les tests **échoueront** sur le code actuel (buggy). Après que Bits Code ait corrigé les bugs, ils doivent tous passer.

---

## Les 4 bugs

| # | Endpoint | Erreur actuelle | Erreur attendue |
|---|----------|----------------|-----------------|
| 1 | `GET /products/3/availability` | `500 ZeroDivisionError` | `200 {"availability_score": 0}` |
| 2 | `POST /orders` avec `discount_pct` | Mauvais total (trop bas) | Total = prix × (1 - remise) |
| 3 | `GET /products/summary` | Lent (~300ms) | Rapide (<5ms) |
| 4 | `PUT /products/1` body partiel | `500 KeyError` | `400 Bad Request` |

---

## Endpoints

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/health` | Healthcheck |
| GET | `/products` | Liste des produits |
| GET | `/products/<id>` | Détail d'un produit |
| GET | `/products/<id>/availability` | Score de disponibilité |
| GET | `/products/summary` | Résumé (lent — Bug #3) |
| POST | `/orders` | Créer une commande |
| GET | `/orders/<id>` | Détail d'une commande |
| PUT | `/products/<id>` | Modifier un produit |

---

## Tester avec Bits Code

1. Démarrez l'API avec `ddtrace-run`
2. Lancez `trigger_bugs.py` pour générer des erreurs
3. Dans Datadog → **Error Tracking** → cherchez les erreurs `ZeroDivisionError` et `KeyError`
4. Cliquez **"Fix with Bits"** sur chaque issue
5. Bits Code ouvre une session, investigate, génère un PR
6. Vérifiez le PR et mergez !
