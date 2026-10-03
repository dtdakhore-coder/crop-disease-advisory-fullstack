// ============================================================
// CropCare AI - Enhanced Live Demo Logic
// Features: Camera capture, Top-3 Probability, Multi-language (EN/HI/MR), Print Report
// ============================================================

// Smart API URL Detection:
// Automatically uses relative /predict on Render or Flask server
const API_URL = (window.location.origin.includes("onrender.com") || window.location.port === "5000")
  ? "/predict"
  : (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
      ? "http://localhost:5000/predict"
      : "/predict");

// Multi-language translation dictionary
const I18N = {
  en: {
    nav_home: "Home", nav_how: "How It Works", nav_models: "Models", nav_demo: "Live Demo", nav_team: "Team",
    title_demo: "Smart Crop Health Diagnosis",
    sub_demo: "Upload a leaf photo or use your device camera to instantly identify crop diseases, get nutrient guidance, and receive customized fertilizer recommendations.",
    drop_title: "Drop leaf photo here", drop_sub: "or click to browse from device (JPG / PNG)",
    sample_1: "🍃 Sample: Early Blight", sample_2: "🍂 Sample: Leaf Spot",
    btn_camera: "Snap Camera", btn_analyze: "Analyze Leaf", btn_print: "Print / Download PDF Report",
    sec_about: "About This Condition", sec_fertilizer: "Fertilizer Prescription",
    sec_nutrients: "Nutrient & Soil Guidance", sec_care: "Farm Care & Management Tips",
    sec_top3: "Top Probability Predictions",
    ph_title: "Your Detection Result Will Appear Here", ph_sub: "Crop identification · Disease severity · Fertilizer & care guide",
    cam_title: "Position Leaf in Camera", cam_cancel: "Cancel", cam_capture: "Capture Photo"
  },
  hi: {
    nav_home: "होम", nav_how: "कार्यप्रणाली", nav_models: "मॉडल्स", nav_demo: "लाइव डेमो", nav_team: "टीम",
    title_demo: "स्मार्ट फसल रोग निदान एवं सलाह",
    sub_demo: "फसल की पत्ती की फोटो अपलोड करें या कैमरे से खींचे। रोग की पहचान, पोषक तत्व और सटीक खाद की सिफारिश पाएं।",
    drop_title: "यहाँ पत्ती की फोटो डालें", drop_sub: "या गैलरी से चुनें (JPG / PNG)",
    sample_1: "🍃 नमूना: अगेती झुलसा", sample_2: "🍂 नमूना: पत्ती धब्बा",
    btn_camera: "कैमरा खोलें", btn_analyze: "रोग की जांच करें", btn_print: "रिपोर्ट प्रिंट / पीडीएफ डाउनलोड करें",
    sec_about: "रोग के बारे में जानकारी", sec_fertilizer: "खाद एवं उर्वरक सिफारिश",
    sec_nutrients: "पोषक तत्व व मृदा प्रबंधन", sec_care: "देखभाल और उपचार के उपाय",
    sec_top3: "संभावित शीर्ष रोग",
    ph_title: "जांच का परिणाम यहाँ दिखाई देगा", ph_sub: "फसल पहचान · रोग का प्रकार · खाद और देखभाल की जानकारी",
    cam_title: "पत्ती को कैमरे के सामने रखें", cam_cancel: "रद्द करें", cam_capture: "फोटो खींचें"
  },
  mr: {
    nav_home: "मुख्यपृष्ठ", nav_how: "कसे कार्य करते", nav_models: "मॉडेल्स", nav_demo: "थेट प्रात्यक्षिक", nav_team: "आमची टीम",
    title_demo: "स्मार्ट पीक रोग निदान व सल्ला",
    sub_demo: "पिकाच्या पानाचा फोटो अपलोड करा किंवा कॅमेऱ्याने काढा. रोग निदान, खतांचे योग्य व्यवस्थापन आणि उपाययोजना मिळवा.",
    drop_title: "येथे पानाच्या फोटोची प्रत टाका", drop_sub: "किंवा डिव्हाइसमधून निवडा (JPG / PNG)",
    sample_1: "🍃 नमुना: करपा रोग", sample_2: "🍂 नमुना: पानांवरील ठिपके",
    btn_camera: "कॅमेरा सुरू करा", btn_analyze: "पानाचे विश्लेषण करा", btn_print: "अहवाल प्रिंट / पीडीएफ डाउनलोड करा",
    sec_about: "रोगाविषयी माहिती", sec_fertilizer: "खतांचा डोस व शिफारस",
    sec_nutrients: "अन्नद्रव्य व माती व्यवस्थापन", sec_care: "पिकाची काळजी व व्यवस्थापन",
    sec_top3: "संभाव्य रोग शक्यता",
    ph_title: "तपासणीचा निकाल येथे दिसेल", ph_sub: "पीक ओळख · रोगाचे स्वरूप · खत व कीड व्यवस्थापन",
    cam_title: "पान कॅमेऱ्यासमोर व्यवस्थित धरा", cam_cancel: "रद्द करा", cam_capture: "फोटो काढा"
  }
};

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
  const cameraBtn = document.getElementById('cameraBtn');
  const cameraModal = document.getElementById('cameraModal');
  const cameraVideo = document.getElementById('cameraVideo');
  const cameraCanvas = document.getElementById('cameraCanvas');
  const captureBtn = document.getElementById('captureBtn');
  const closeCameraBtn = document.getElementById('closeCameraBtn');
  const printBtn = document.getElementById('printBtn');
  const langSelect = document.getElementById('langSelect');

  let imageLoaded = false;
  let currentFile = null;
  let stream = null;

  // Language Switcher
  if (langSelect) {
    langSelect.addEventListener('change', (e) => {
      const lang = e.target.value;
      const dict = I18N[lang] || I18N.en;
      document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (dict[key]) el.textContent = dict[key];
      });
    });
  }

  // File Upload Handlers
  if (zone) {
    zone.addEventListener('click', () => fileInput.click());
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('dragover'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));
    zone.addEventListener('drop', e => {
      e.preventDefault(); zone.classList.remove('dragover');
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', () => {
      if (fileInput.files.length) handleFile(fileInput.files[0]);
    });
  }

  function handleFile(file) {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (JPG / PNG).');
      return;
    }
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

  // Sample Chips
  document.querySelectorAll('.sample-chip').forEach(chip => {
    chip.addEventListener('click', (e) => {
      e.stopPropagation();
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

  // Camera Integration
  if (cameraBtn) {
    cameraBtn.addEventListener('click', async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' }
        });
        cameraVideo.srcObject = stream;
        cameraModal.classList.add('show');
      } catch (err) {
        alert('Could not access camera. Please allow camera permissions or browse an image.');
      }
    });
  }

  if (closeCameraBtn) {
    closeCameraBtn.addEventListener('click', () => {
      stopCamera();
      cameraModal.classList.remove('show');
    });
  }

  if (captureBtn) {
    captureBtn.addEventListener('click', () => {
      cameraCanvas.width = cameraVideo.videoWidth || 640;
      cameraCanvas.height = cameraVideo.videoHeight || 480;
      const ctx = cameraCanvas.getContext('2d');
      ctx.drawImage(cameraVideo, 0, 0, cameraCanvas.width, cameraCanvas.height);
      cameraCanvas.toBlob(blob => {
        handleFile(new File([blob], 'camera-leaf.jpg', { type: 'image/jpeg' }));
        stopCamera();
        cameraModal.classList.remove('show');
      }, 'image/jpeg', 0.95);
    });
  }

  function stopCamera() {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      stream = null;
    }
  }

  // Analyze Button Click
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', async () => {
      if (!imageLoaded || !currentFile) return;
      resultCard.classList.remove('show');
      if (placeholder) placeholder.style.display = 'none';
      progressWrap.style.display = 'block';
      progressBar.style.width = '0%';
      analyzeBtn.disabled = true;
      analyzeBtn.textContent = 'Analyzing Leaf...';

      try {
        const formData = new FormData();
        formData.append('image', currentFile);
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 7000);

        const resp = await fetch(API_URL, { method: 'POST', body: formData, signal: controller.signal });
        clearTimeout(timeout);
        if (!resp.ok) throw new Error('backend error');
        progressBar.style.width = '100%';
        const data = await resp.json();
        setTimeout(() => showResult(data, !data.simulated), 300);
      } catch (err) {
        // Fallback simulation
        let pct = 0;
        await new Promise(resolve => {
          const timer = setInterval(() => {
            pct += Math.random() * 18 + 8;
            if (pct >= 100) { pct = 100; clearInterval(timer); setTimeout(resolve, 200); }
            progressBar.style.width = pct + '%';
          }, 100);
        });
        const pick = SIM_DISEASE_POOL[Math.floor(Math.random() * SIM_DISEASE_POOL.length)];
        const entry = KNOWLEDGE_BASE[pick.crop][pick.disease];
        showResult({
          crop: pick.crop, disease: pick.disease,
          confidence: (85 + Math.random() * 13).toFixed(1),
          desc: entry.desc, fertilizer: entry.fertilizer,
          nutrients: entry.nutrients, care: entry.care, simulated: true
        }, false);
      }
    });
  }

  function showResult(d, fromModel) {
    progressWrap.style.display = 'none';
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = 'Analyze Leaf';

    document.getElementById('resCrop').textContent = d.crop || '—';
    document.getElementById('resDisease').textContent = d.disease || '—';
    document.getElementById('resConfidence').textContent = (d.confidence || 0) + '%';
    document.getElementById('resDesc').textContent = d.desc || '—';
    document.getElementById('resFertilizer').textContent = d.fertilizer || '—';
    document.getElementById('resNutrients').textContent = d.nutrients || '—';
    document.getElementById('resCare').innerHTML = (d.care || []).map(c => '<li>' + c + '</li>').join('');

    // Top 3 Probabilities
    const top3Wrap = document.getElementById('top3Wrap');
    const top3List = document.getElementById('top3List');
    if (d.top3 && d.top3.length > 0 && top3Wrap && top3List) {
      top3List.innerHTML = d.top3.map(item => `
        <div class="top3-row">
          <div class="top3-labels">
            <span>${item.label.replace(/___/g, ' - ').replace(/_/g, ' ')}</span>
            <span>${item.prob}%</span>
          </div>
          <div class="top3-bar-bg">
            <div class="top3-bar-fill" style="width:${item.prob}%"></div>
          </div>
        </div>
      `).join('');
      top3Wrap.style.display = 'block';
    } else if (top3Wrap) {
      top3Wrap.style.display = 'none';
    }

    const badge = document.querySelector('.badge-sim');
    if (badge) {
      if (d.is_plant === false) {
        badge.textContent = '⚠️ NON-CROP DETECTED';
        badge.style.background = '#fee2e2';
        badge.style.color = '#991b1b';
      } else {
        badge.textContent = fromModel ? '✨ MODEL PREDICTION' : '⚡ SIMULATED OUTPUT';
        badge.style.background = fromModel ? '#dcfce7' : '#fef3c7';
        badge.style.color = fromModel ? '#166534' : '#92400e';
      }
    }

    resultCard.classList.add('show');
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // Print PDF Report Handler
  if (printBtn) {
    printBtn.addEventListener('click', () => {
      window.print();
    });
  }
});
