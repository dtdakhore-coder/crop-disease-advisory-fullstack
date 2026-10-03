# CropCare AI — ML-Based Crop Disease Detection & Fertilizer Advisory System

A complete static website for the academic project: **"Ml-Based Crop Disease Detection and Fertilizer Advisory System"**
(Shri Sant Gajanan Maharaj College of Engineering — Anuj Parihar, Aditya Dakhore, Abhishek Gupta).

## Pages
- `index.html` — Home, problem statement, idea, benefits
- `how-it-works.html` — Steps, architecture, components
- `models.html` — Model choices, diseases covered, limitations & future scope
- `demo.html` — Live demo: upload a leaf photo -> simulated detection -> fertilizer & care advice
- `team.html` — Team, takeaway, references

## How to run locally
Just open `index.html` in any browser. No server or build step needed.

## How to host online (free options)
**GitHub Pages**
1. Create a GitHub repository and upload all files.
2. Settings -> Pages -> Source: `main` branch, `/ (root)` -> Save.
3. Your site goes live at `https://<username>.github.io/<repo>/`

**Netlify (drag & drop)**
1. Go to app.netlify.com/drop
2. Drag the project folder onto the page. Done — you get an instant link.

**Vercel**
1. Import the repo at vercel.com/new -> Deploy.

## Connecting a real model later
The demo currently uses a simulated classifier (`js/knowledgebase.js`). To use your real
MobileNetV2 / EfficientNet model, convert it to TensorFlow.js (`tensorflowjs_converter`)
and replace the prediction logic in `js/demo.js` with `model.predict()`. The advisory
knowledge base is already structured for you — just add your crop/disease entries.

## Disclaimer
This is a screening aid, not a substitute for an agronomist. Advice is general guidance
and must be validated by agricultural experts and field testing.
