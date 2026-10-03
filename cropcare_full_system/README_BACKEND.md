# Backend + Model Training Guide

## Step 1 - Train the model (Google Colab, FREE GPU)
1. Go to https://colab.research.google.com and create a new notebook
2. Runtime -> Change runtime type -> GPU (T4, free)
3. Upload the PlantVillage dataset. Easiest way (Kaggle):
   ```
   !pip install kaggle
   # upload your kaggle.json (Kaggle -> Account -> API -> Create New Token)
   !mkdir -p ~/.kaggle && cp kaggle.json ~/.kaggle/ && chmod 600 ~/.kaggle/kaggle.json
   !kaggle datasets download -d emmarex/plantdisease
   !unzip plantdisease.zip -d dataset
   ```
   (Alternative: upload a zip of your own leaf-image folders)
4. Upload `train.py` to Colab, then run:
   ```
   !python train.py --data dataset/PlantVillage --epochs 12 --out model
   ```
5. When done, download TWO files from the `model/` folder:
   - `crop_disease_model.h5`
   - `labels.json`
   Place them in `backend/model/`.

## Step 2 - Run the backend
```
cd backend
pip install -r requirements.txt
python app.py
```
Server starts at http://localhost:5000

- http://localhost:5000/health  -> check if model loaded
- http://localhost:5000/predict -> POST an image, get crop/disease/confidence/advice

If the model files are missing the server still runs and answers in
simulation mode (so nothing breaks during your demo).

## Step 3 - Connect the website
Open `website/demo.html` and click Analyze. The frontend first tries the
real backend (http://localhost:5000/predict); if it is unreachable it
falls back to the built-in simulation. To point it at a hosted backend,
edit the `API_URL` constant at the top of `website/js/demo.js`.

## Step 4 - Host backend + site together (optional)
Deploy the Flask app to Render / Railway (free tier), put the site URL
in `demo.js` API_URL, and the whole system works live for your demo.

## API response example
```json
{
  "crop": "Tomato",
  "disease": "Early Blight",
  "confidence": 94.3,
  "desc": "...",
  "fertilizer": "...",
  "nutrients": "...",
  "care": ["...", "..."],
  "simulated": false
}
```
