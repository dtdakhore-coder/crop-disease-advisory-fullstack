# CropCare AI - Full Stack Package
## ML-Based Crop Disease Detection & Fertilizer Advisory System

| Folder | What it is |
|---|---|
| `website/` | Complete static website (5 pages) - deploy to Netlify as-is |
| `backend/` | Flask API + model training script + advisory knowledge base |

## Quick start
1. Deploy `website/` to Netlify (drag & drop) -> public site works immediately
   (demo runs in simulation mode when backend is offline)
2. Train the model -> see `backend/README_BACKEND.md` (Google Colab, free GPU)
3. Put `crop_disease_model.h5` + `labels.json` into `backend/model/`
4. Run `python backend/app.py` -> demo now uses REAL predictions
5. (Optional) Host backend on Render/Railway and update `API_URL` in
   `website/js/demo.js` so the live Netlify site uses the real model too.

## Team
Anuj Parihar | Aditya Dakhore | Abhishek Gupta
Shri Sant Gajanan Maharaj College of Engineering

## Disclaimer
Screening aid only - not a substitute for an agronomist. Field testing and
expert review required before real-world use.
