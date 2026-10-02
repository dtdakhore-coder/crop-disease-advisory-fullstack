// ============================================================
// CropCare AI - Demo logic
// Tries the real Flask backend first; falls back to simulation
// if the backend is unreachable (e.g. static-only deployment).
// ============================================================
const API_URL = "http://localhost:5000/predict";

document.addEventListener('DOMContentLoaded', () => {
  const zone = document.getElementById('uploadZone');
  const fileInput = document.getElementById('fileInput');
  const previewBox = document.getElementById('previewBox');
  const previewImg = document.getElementById('previewImg');
  const analyzeBtn = document.getElementById('analyzeBtn');
  const progressWrap = document.getElementById('progressWrap');
  const progressBar = document.getElementById('progressBar');
  const resultCard = document.getElementById('resultCard');
  const placeholder = document.getElementById('placeholder');
  let imageLoaded = false;
  let currentFile = null;

  if (!zone) return;

  zone.addEventListener('click', () => fileInput.click());
  zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
  zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
  zone.addEventListener('drop', e => {
    e.preventDefault(); zone.classList.remove('dragover');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', () => { if (fileInput.files.length) handleFile(fileInput.files[0]); });

  function handleFile(file) {
    if (!file.type.startsWith('image/')) { alert('Please upload an image file (JPG / PNG).'); return; }
    currentFile = file;
    const reader = new FileReader();
    reader.onload = e => {
      previewImg.src = e.target.result;
      previewBox.style.display = 'block';
      imageLoaded = true;
      analyzeBtn.disabled = false;
      resultCard.classList.remove('show');
      if (placeholder) placeholder.style.display = 'block';
    };
    reader.readAsDataURL(file);
  }

  // Sample leaf chips (quick test without uploading)
  document.querySelectorAll('.sample-chip').forEach(chip => {
    chip.addEventListener('click', () => {
      fetch(chip.dataset.img).then(r => r.blob()).then(blob => {
        currentFile = new File([blob], 'sample.png', { type: 'image/png' });
        previewImg.src = chip.dataset.img;
        previewBox.style.display = 'block';
        imageLoaded = true;
        analyzeBtn.disabled = false;
        resultCard.classList.remove('show');
        if (placeholder) placeholder.style.display = 'block';
      });
    });
  });

  analyzeBtn.addEventListener('click', async () => {
    if (!imageLoaded) return;
    resultCard.classList.remove('show');
    if (placeholder) placeholder.style.display = 'none';
    progressWrap.style.display = 'block';
    progressBar.style.width = '0%';
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = 'Analyzing...';

    try {
      // ---- Try the REAL backend first ----
      const formData = new FormData();
      formData.append('image', currentFile);
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 6000); // 6s grace
      const resp = await fetch(API_URL, { method: 'POST', body: formData, signal: controller.signal });
      clearTimeout(timeout);
      if (!resp.ok) throw new Error('backend error');
      progressBar.style.width = '100%';
      const data = await resp.json();
      setTimeout(() => showResult(data, !data.simulated), 400);
    } catch (err) {
      // ---- Fallback: simulated classification ----
      let pct = 0;
      await new Promise(resolve => {
        const timer = setInterval(() => {
          pct += Math.random() * 14 + 4;
          if (pct >= 100) { pct = 100; clearInterval(timer); setTimeout(resolve, 300); }
          progressBar.style.width = pct + '%';
        }, 180);
      });
      const pick = SIM_DISEASE_POOL[Math.floor(Math.random() * SIM_DISEASE_POOL.length)];
      const entry = KNOWLEDGE_BASE[pick.crop][pick.disease];
      showResult({
        crop: pick.crop, disease: pick.disease,
        confidence: (72 + Math.random() * 26).toFixed(1),
        desc: entry.desc, fertilizer: entry.fertilizer,
        nutrients: entry.nutrients, care: entry.care, simulated: true
      }, false);
    }
  });

  function showResult(d, fromModel) {
    progressWrap.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = 'Analyze Leaf Photo';

    document.getElementById('resCrop').textContent = d.crop || '—';
    document.getElementById('resDisease').textContent = d.disease || '—';
    document.getElementById('resConfidence').textContent = (d.confidence || 0) + '%';
    document.getElementById('resDesc').textContent = d.desc || '—';
    document.getElementById('resFertilizer').textContent = d.fertilizer || '—';
    document.getElementById('resNutrients').textContent = d.nutrients || '—';
    document.getElementById('resCare').innerHTML = (d.care || []).map(c => '<li>' + c + '</li>').join('');

    const badge = document.querySelector('.badge-sim');
    if (badge) {
      if (d.is_plant === false) {
        badge.textContent = '⚠️ NON-CROP DETECTED';
        badge.style.background = '#fee2e2';
        badge.style.color = '#991b1b';
      } else {
        badge.textContent = fromModel ? 'MODEL PREDICTION' : 'SIMULATED OUTPUT';
        badge.style.background = fromModel ? '#dcfce7' : '#fef3c7';
        badge.style.color = fromModel ? '#166534' : '#92400e';
      }
    }
    resultCard.classList.add('show');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
});
