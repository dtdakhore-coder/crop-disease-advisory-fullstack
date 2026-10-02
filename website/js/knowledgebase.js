
// Knowledge base: crop + disease -> fertilizer / nutrient / care advice
// (Rule-based advisory module — matches the project report, Section 6)
const KNOWLEDGE_BASE = {
  "Tomato": {
    "Early Blight": {
      desc: "Dark concentric-ring spots on older leaves, yellowing around lesions; caused by Alternaria solani.",
      fertilizer: "Apply balanced NPK 10-10-10 at recommended dose; avoid excess nitrogen which worsens foliage disease.",
      nutrients: "Ensure adequate potassium and calcium for stronger leaf tissue. Foliar spray of potassium silicate may help.",
      care: ["Remove and destroy infected lower leaves.", "Mulch around plants to prevent soil splash.", "Water at the base, avoid wetting leaves.", "Rotate crops — do not plant tomato/potato in the same spot for 2 years."]
    },
    "Late Blight": {
      desc: "Water-soaked lesions that turn brown/black; white mold under leaf in humid weather; caused by Phytophthora infestans.",
      fertilizer: "Avoid heavy nitrogen. Use phosphorus-rich fertilizer to support root strength.",
      nutrients: "Maintain potassium levels; stressed plants are more susceptible.",
      care: ["Destroy infected plants immediately.", "Improve air circulation by spacing plants.", "Apply recommended fungicide at first sign.", "Avoid overhead irrigation."]
    },
    "Leaf Mold": {
      desc: "Yellow spots on upper leaf surface with olive-green mold underneath; favored by high humidity.",
      fertilizer: "Moderate nitrogen only; excess makes leaves soft and prone to mold.",
      nutrients: "Calcium and boron support leaf integrity.",
      care: ["Ventilate greenhouse / space field plants.", "Water early in the day so leaves dry quickly.", "Remove infected leaves carefully.", "Resistant varieties help in future seasons."]
    },
    "Healthy": {
      desc: "No visible disease symptoms. Leaves are uniformly green and vigorous.",
      fertilizer: "Continue regular balanced fertilization as per growth stage.",
      nutrients: "Maintain NPK balance; add compost for soil health.",
      care: ["Continue weekly monitoring.", "Water consistently.", "Scout for early signs of pests."]
    }
  },
  "Potato": {
    "Early Blight": {
      desc: "Brown spots with concentric rings ('target board') on lower leaves first.",
      fertilizer: "Apply NPK based on soil test; avoid late nitrogen top-dressing.",
      nutrients: "Potassium strengthens resistance; ensure sufficient magnesium.",
      care: ["Remove infected leaves.", "Hill soil around plants properly.", "Maintain even soil moisture.", "Practice 3-year crop rotation."]
    },
    "Late Blight": {
      desc: "Rapid-spreading dark lesions; tubers show brown rot; severe in cool wet weather.",
      fertilizer: "Phosphorus and potassium focused feeding; avoid lush nitrogen growth.",
      nutrients: "Balanced micronutrients (Zn, Mn) improve plant immunity.",
      care: ["Remove infected foliage urgently.", "Harvest in dry conditions.", "Store tubers dry and cool.", "Use resistant varieties and certified seed."]
    },
    "Healthy": {
      desc: "No visible disease symptoms. Canopy looks normal and green.",
      fertilizer: "Follow standard schedule: basal NPK + earthing-up top dressing.",
      nutrients: "Monitor for potassium deficiency (leaf edge scorching).",
      care: ["Regular field scouting.", "Irrigate at critical tuber-initiation stage.", "Keep field weed-free."]
    }
  },
  "Corn (Maize)": {
    "Gray Leaf Spot": {
      desc: "Rectangular gray-tan lesions running parallel to leaf veins; reduces photosynthesis badly.",
      fertilizer: "Avoid excess nitrogen; split applications reduce severity.",
      nutrients: "Adequate potassium improves resistance.",
      care: ["Rotate with non-cereal crops.", "Till in crop residue where practical.", "Plant resistant hybrids.", "Apply fungicide if lesions reach ear leaf."]
    },
    "Common Rust": {
      desc: "Small reddish-brown pustules scattered on both leaf surfaces.",
      fertilizer: "Balanced NPK; avoid stress from nutrient deficiency.",
      nutrients: "Sufficient sulfur and magnesium support leaf health.",
      care: ["Scout from early vegetative stage.", "Fungicide if rust appears before silking.", "Choose tolerant hybrids for next season."]
    },
    "Healthy": {
      desc: "No visible disease symptoms.",
      fertilizer: "Standard NPK with split nitrogen (basal + knee-high stage).",
      nutrients: "Zinc is often deficient in Indian soils — soil test recommended.",
      care: ["Monitor weekly.", "Ensure drainage in heavy rains.", "Weed control in early stages."]
    }
  },
  "Rice": {
    "Brown Spot": {
      desc: "Oval brown spots with yellow halo on leaves; linked to nutrient deficiency stress.",
      fertilizer: "Correct nutrient imbalance — this disease is often a sign of potassium/nitrogen deficiency.",
      nutrients: "Apply potash and silica; maintain proper N:K ratio.",
      care: ["Use disease-free seed.", "Avoid drought stress with proper water management.", "Spray recommended fungicide if severe.", "Improve soil fertility long-term."]
    },
    "Leaf Blast": {
      desc: "Diamond-shaped lesions with gray centers and brown margins; spreads fast in cloudy humid weather.",
      fertilizer: "Avoid excessive nitrogen — split application reduces blast risk.",
      nutrients: "Silicon fertilization (e.g., calcium silicate) significantly reduces blast.",
      care: ["Maintain proper water level — avoid prolonged leaf wetness.", "Use resistant varieties.", "Apply fungicide at early panicle stage.", "Burn/bury infected stubble after harvest."]
    },
    "Healthy": {
      desc: "No visible disease symptoms.",
      fertilizer: "Follow recommended dose based on soil test (Leaf Color Chart based N is ideal).",
      nutrients: "Ensure zinc in deficient soils.",
      care: ["Weekly monitoring.", "Proper water management.", "Weed control."]
    }
  },
  "Grape": {
    "Black Rot": {
      desc: "Brown circular leaf spots with black fruiting bodies; berries shrivel into hard black mummies.",
      fertilizer: "Balanced fertility; avoid stress from over/under feeding.",
      nutrients: "Potassium and calcium support berry skin strength.",
      care: ["Remove mummified berries — main source of infection.", "Prune for airflow.", "Protectant fungicide from bloom onwards.", "Manage leaf wetness in vineyard."]
    },
    "Healthy": {
      desc: "No visible disease symptoms.",
      fertilizer: "Standard vineyard nutrition program by growth stage.",
      nutrients: "Monitor potassium before ripening.",
      care: ["Regular canopy management.", "Disease scouting weekly."]
    }
  }
};

// Simulated classifier output pool (until the real MobileNetV2/EfficientNet model is connected)
const SIM_DISEASE_POOL = Object.entries(KNOWLEDGE_BASE).flatMap(([crop, diseases]) =>
  Object.keys(diseases).map(disease => ({ crop, disease }))
);
