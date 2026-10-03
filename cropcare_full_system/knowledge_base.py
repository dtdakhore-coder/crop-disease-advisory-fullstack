"""
CropCare AI - Agronomic Knowledge Base.
Supports all 38 PlantVillage crop-disease classes + Rice & Cotton extensions.
Provides structured symptoms, fertilizer recommendations, nutrient deficiencies, and field care tips.
"""

KNOWLEDGE_BASE = {
    # APPLE
    "Apple___Apple_scab": {
        "crop": "Apple", "disease": "Apple Scab",
        "desc": "Olive-green to black velvety spots on leaves and fruit caused by the fungus Venturia inaequalis.",
        "fertilizer": "Balanced NPK; avoid excessive spring nitrogen which produces tender foliage susceptible to scab.",
        "nutrients": "Calcium sprays help firm fruit and leaf cuticles. Maintain adequate potassium.",
        "care": ["Rake and destroy fallen leaves in autumn to reduce overwintering spores.",
                 "Prune trees to open canopy and improve air circulation.",
                 "Apply protective fungicides (mancozeb, captan) during green tip to petal fall stages."]
    },
    "Apple___Black_rot": {
        "crop": "Apple", "disease": "Black Rot (Frogeye Leaf Spot)",
        "desc": "Small purple specks enlarging into circular spots with tan centers and dark margins; causes fruit rot.",
        "fertilizer": "Maintain balanced fertility; avoid high nitrogen late in the season.",
        "nutrients": "Ensure proper calcium and boron levels for tissue strength.",
        "care": ["Prune out dead wood, fire blight strikes, and mummified fruits.",
                 "Burn or bury prunings.", "Apply fungicides from bloom through cover sprays."]
    },
    "Apple___Cedar_apple_rust": {
        "crop": "Apple", "disease": "Cedar Apple Rust",
        "desc": "Bright yellow-orange spots on upper leaf surfaces that develop tube-like structures on the underside.",
        "fertilizer": "Standard balanced orchard NPK based on leaf tissue analysis.",
        "nutrients": "Ensure adequate zinc and magnesium.",
        "care": ["Remove nearby red cedar or juniper hosts within 1-2 miles if feasible.",
                 "Apply preventive fungicides from pink bud through petal fall.",
                 "Plant rust-resistant apple varieties."]
    },
    "Apple___healthy": {
        "crop": "Apple", "disease": "Healthy",
        "desc": "No visible disease symptoms. Leaves are crisp, uniformly green, and vibrant.",
        "fertilizer": "Standard maintenance orchard schedule: split application of nitrogen + potassium.",
        "nutrients": "Routine foliar spray of boron and zinc before bloom.",
        "care": ["Regular pest and disease scouting.", "Consistent drip irrigation.", "Annual pruning."]
    },

    # BLUEBERRY
    "Blueberry___healthy": {
        "crop": "Blueberry", "disease": "Healthy",
        "desc": "Leaves are dark green and glossy without necrotic spots or chlorosis.",
        "fertilizer": "Acidic fertilizers (ammonium sulfate) to maintain soil pH between 4.5 and 5.2.",
        "nutrients": "Avoid nitrate-based nitrogen; supplement with chelated iron if soil pH drifts.",
        "care": ["Maintain pine bark or sawdust mulch.", "Ensure acid, well-draining soil.", "Regular watering."]
    },

    # CHERRY
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop": "Cherry", "disease": "Powdery Mildew",
        "desc": "White powdery fungal coating on leaves and young shoots, causing leaf curling and distortion.",
        "fertilizer": "Avoid excess nitrogen fertilizer which encourages lush, susceptible new growth.",
        "nutrients": "Potassium silicate foliar applications can help strengthen epidermal cells.",
        "care": ["Prune to enhance light penetration and airflow.",
                 "Apply sulfur or systemic fungicides starting at petal fall.",
                 "Scout regularly during warm, dry weather."]
    },
    "Cherry_(including_sour)___healthy": {
        "crop": "Cherry", "disease": "Healthy",
        "desc": "Vigorous healthy foliage with no signs of fungal or bacterial infection.",
        "fertilizer": "Balanced fruit-tree fertilizer applied in early spring before bud break.",
        "nutrients": "Adequate calcium to prevent fruit cracking during rains.",
        "care": ["Monitor for cherry fruit fly and aphids.", "Maintain weed-free tree basin."]
    },

    # CORN (MAIZE)
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop": "Corn (Maize)", "disease": "Gray Leaf Spot",
        "desc": "Rectangular gray to tan necrotic lesions running strictly parallel to leaf veins.",
        "fertilizer": "Balanced NPK; split nitrogen application (basal + knee-high) to reduce disease severity.",
        "nutrients": "Adequate potassium improves stalk strength and resistance.",
        "care": ["Rotate with non-host crops (soybean, peanut).",
                 "Till under infected residue where conservation tillage is not critical.",
                 "Plant resistant corn hybrids.", "Apply strobilurin/triazole fungicide if lesions reach ear leaf."]
    },
    "Corn_(maize)___Common_rust_": {
        "crop": "Corn (Maize)", "disease": "Common Rust",
        "desc": "Small, powdery reddish-brown pustules scattered across both upper and lower leaf surfaces.",
        "fertilizer": "Standard split NPK; avoid nitrogen stress which weakens plants.",
        "nutrients": "Sufficient sulfur and magnesium support chlorophyll synthesis.",
        "care": ["Plant rust-resistant or tolerant hybrids.",
                 "Apply foliar fungicide if rust appears before the silking stage."]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop": "Corn (Maize)", "disease": "Northern Leaf Blight",
        "desc": "Large, cigar-shaped grayish-green to tan lesions (1-6 inches long) caused by Exserohilum turcicum.",
        "fertilizer": "Balanced nutrition; avoid potassium deficiency.",
        "nutrients": "Ensure balanced zinc and potash.",
        "care": ["Crop rotation with broadleaf crops.", "Use resistant hybrid seeds.",
                 "Foliar fungicide application if disease threatens upper canopy before tasseling."]
    },
    "Corn_(maize)___healthy": {
        "crop": "Corn (Maize)", "disease": "Healthy",
        "desc": "Uniform dark green leaves without lesions or chlorotic striping.",
        "fertilizer": "Basal NPK at sowing + urea top-dressing at V6 and tasseling stages.",
        "nutrients": "Soil test for zinc; apply zinc sulfate if deficient.",
        "care": ["Keep field weed-free during first 45 days.", "Maintain proper drainage during monsoons."]
    },

    # GRAPE
    "Grape___Black_rot": {
        "crop": "Grape", "disease": "Black Rot",
        "desc": "Circular reddish-brown leaf spots with tiny black dots; causes grapes to shrivel into hard black mummies.",
        "fertilizer": "Moderate balanced fertilizer; avoid excess vegetative vigor.",
        "nutrients": "Ensure balanced potassium and boron for fruit set.",
        "care": ["Remove all mummified clusters and infected canes during winter pruning.",
                 "Canopy management for maximum sun and wind exposure.",
                 "Apply preventive fungicides starting from early shoot growth."]
    },
    "Grape___Esca_(Black_Measles)": {
        "crop": "Grape", "disease": "Esca (Black Measles)",
        "desc": "Interveinal tiger-stripe yellow/brown chlorosis on leaves; spotted berries; wood rot inside vines.",
        "fertilizer": "Avoid stressing vines; apply gentle organic fertilizers.",
        "nutrients": "Foliar micronutrients to support stressed vascular systems.",
        "care": ["Disinfect pruning shears between vines.",
                 "Seal large pruning wounds with wound paste.",
                 "Remove and destroy severely collapsed vines."]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop": "Grape", "disease": "Leaf Blight (Isariopsis Spot)",
        "desc": "Dark brown, angular to irregular spots on mature leaves causing premature leaf defoliation.",
        "fertilizer": "Balanced NPK with adequate potassium to support late-season leaf retention.",
        "nutrients": "Magnesium and iron foliar sprays to maintain photosynthesis.",
        "care": ["Post-harvest copper fungicide spray.", "Collect and burn fallen leaves.", "Ensure proper trellis ventilation."]
    },
    "Grape___healthy": {
        "crop": "Grape", "disease": "Healthy",
        "desc": "Vigorous green vine canopy with clean clusters and healthy leaf development.",
        "fertilizer": "Fertigation schedule with balanced NPK + micronutrient pack.",
        "nutrients": "Monitor petioles for potassium, magnesium, and boron levels.",
        "care": ["Regular shoot positioning and leaf pulling around fruit zone.", "Systematic pest scouting."]
    },

    # CITRUS / ORANGE
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop": "Orange / Citrus", "disease": "Citrus Greening (Huanglongbing)",
        "desc": "Asymmetrical blotchy mottled yellow leaves, yellow shoots, small lopsided bitter fruit; spread by psyllids.",
        "fertilizer": "Intensive foliar nutritional feeding (NPK + micronutrients) to prolong tree productivity.",
        "nutrients": "High-frequency foliar sprays of zinc, manganese, iron, and potassium phosphite.",
        "care": ["Aggressively control Asian citrus psyllid vectors using systemic insecticides.",
                 "Remove heavily infected, unproductive trees.",
                 "Plant certified disease-free nursery stock in enclosed screen houses."]
    },

    # PEACH
    "Peach___Bacterial_spot": {
        "crop": "Peach", "disease": "Bacterial Spot",
        "desc": "Angular water-soaked spots turning purple-brown and dropping out to create a 'shot-hole' effect.",
        "fertilizer": "Avoid high spring nitrogen which produces excessive soft foliage.",
        "nutrients": "Maintain good soil calcium levels.",
        "care": ["Apply dormant and bloom copper sprays.",
                 "Plant resistant cultivars.", "Avoid overhead irrigation that splashes bacteria."]
    },
    "Peach___healthy": {
        "crop": "Peach", "disease": "Healthy",
        "desc": "Clean, vibrant leaves and healthy vigorous peach canopy.",
        "fertilizer": "Early spring split application of balanced fruit tree fertilizer.",
        "nutrients": "Foliar zinc and boron post-harvest.",
        "care": ["Winter dormant pruning.", "Thin fruit to prevent branch breakage."]
    },

    # PEPPER (BELL)
    "Pepper,_bell___Bacterial_spot": {
        "crop": "Pepper (Bell)", "disease": "Bacterial Spot",
        "desc": "Small, water-soaked, circular to irregular lesions that become dark brown with yellow halos.",
        "fertilizer": "Avoid excess nitrogen. Use calcium nitrate for balanced nitrogen and calcium.",
        "nutrients": "Ensure calcium and potassium availability to reinforce plant cell walls.",
        "care": ["Use certified disease-free seed.", "Apply copper + mancozeb sprays early.",
                 "Avoid working in fields when foliage is wet.", "Rotate crops 2-3 years."]
    },
    "Pepper,_bell___healthy": {
        "crop": "Pepper (Bell)", "disease": "Healthy",
        "desc": "Deep green, glossy foliage with healthy flower and fruit development.",
        "fertilizer": "Balanced NPK (15-15-15) + calcium top-dressing during fruiting.",
        "nutrients": "Magnesium sulfate (Epsom salt) foliar spray during flowering to prevent blossom drop.",
        "care": ["Maintain consistent soil moisture.", "Stake tall plants.", "Scout for thrips and aphids."]
    },

    # POTATO
    "Potato___Early_blight": {
        "crop": "Potato", "disease": "Early Blight",
        "desc": "Brown spots with distinct concentric rings ('target-board' pattern) on older lower leaves.",
        "fertilizer": "Apply NPK based on soil test; avoid nitrogen deficiency which triggers early senescence.",
        "nutrients": "Adequate potassium improves tuber skin strength and disease tolerance.",
        "care": ["Remove infected bottom leaves.", "Maintain even soil moisture with mulch.",
                 "Rotate crops with non-solanaceous crops for 3 years.", "Apply chlorothalonil or azoxystrobin."]
    },
    "Potato___Late_blight": {
        "crop": "Potato", "disease": "Late Blight",
        "desc": "Rapidly expanding water-soaked dark lesions with white fungal mold under leaves in cool, moist weather.",
        "fertilizer": "Avoid heavy late nitrogen. Focus on potassium and phosphorus for tuber protection.",
        "nutrients": "Foliar zinc and copper enhance natural plant immunity.",
        "care": ["Urgent preventive fungicide spray (mancozeb / metalaxyl).",
                 "Destroy infected foliage before tuber harvest.",
                 "Ensure proper soil hilling to cover tubers from washing spores.", "Use certified seed tubers."]
    },
    "Potato___healthy": {
        "crop": "Potato", "disease": "Healthy",
        "desc": "Vigorous, upright canopy with lush green leaves and sturdy stems.",
        "fertilizer": "Basal NPK at planting + earthing up top-dressing of urea and potash.",
        "nutrients": "Ensure adequate sulfur and magnesium in soil.",
        "care": ["Scout fields twice weekly.", "Irrigate at critical tuber bulking stage."]
    },

    # RASPBERRY & SOYBEAN & SQUASH & STRAWBERRY
    "Raspberry___healthy": {
        "crop": "Raspberry", "disease": "Healthy",
        "desc": "Lush compound green leaves with healthy floricane and primocane growth.",
        "fertilizer": "Early spring 10-10-10 fertilizer + organic compost top-dressing.",
        "nutrients": "Maintain soil pH around 6.0 - 6.5.",
        "care": ["Trellis canes.", "Prune spent floricanes after harvest.", "Drip irrigation."]
    },
    "Soybean___healthy": {
        "crop": "Soybean", "disease": "Healthy",
        "desc": "Uniform green trifoliate leaves with nodulated root systems fixing nitrogen.",
        "fertilizer": "Phosphorus and potassium fertilization; inoculate seed with Bradyrhizobium.",
        "nutrients": "Monitor for iron deficiency chlorosis in high pH soils.",
        "care": ["Maintain weed-free canopy closure.", "Scout for pod borers and rust."]
    },
    "Squash___Powdery_mildew": {
        "crop": "Squash", "disease": "Powdery Mildew",
        "desc": "White talcum-powder-like fungal patches spreading over upper and lower leaf surfaces.",
        "fertilizer": "Moderate balanced fertilizer; avoid excess vegetative nitrogen growth.",
        "nutrients": "Potassium bicarbonate or sulfur sprays provide safe, organic control.",
        "care": ["Plant resistant squash hybrids.", "Space plants for excellent airflow.",
                 "Water at root zone with drip tape; never overhead."]
    },
    "Strawberry___Leaf_scorch": {
        "crop": "Strawberry", "disease": "Leaf Scorch",
        "desc": "Irregular purple to dark brown blotches that coalesce and turn the leaf margins dry and scorched.",
        "fertilizer": "Avoid spring nitrogen excess which makes leaves soft.",
        "nutrients": "Ensure balanced calcium and potassium for leaf resilience.",
        "care": ["Remove dry infected leaves after harvest.", "Ensure bed drainage and airflow.",
                 "Apply protective fungicides before flowering."]
    },
    "Strawberry___healthy": {
        "crop": "Strawberry", "disease": "Healthy",
        "desc": "Deep green trifoliate leaves with vibrant crown and runner development.",
        "fertilizer": "Slow-release balanced NPK or fertigation with calcium nitrate and potassium sulfate.",
        "nutrients": "Boron and zinc sprays improve fruit shape and sweetness.",
        "care": ["Straw mulch under berries.", "Regular scouting for spider mites."]
    },

    # TOMATO
    "Tomato___Bacterial_spot": {
        "crop": "Tomato", "disease": "Bacterial Spot",
        "desc": "Small, dark, water-soaked circular spots on leaves; leaves turn yellow and drop prematurely.",
        "fertilizer": "Balanced nutrition; avoid excessive nitrogen.",
        "nutrients": "Calcium nitrate helps build firmer cell walls against bacterial penetration.",
        "care": ["Apply copper hydroxide + mancozeb spray.",
                 "Avoid overhead watering; use drip lines.",
                 "Disinfect stakes and pruning tools.", "Practice 2-year crop rotation."]
    },
    "Tomato___Early_blight": {
        "crop": "Tomato", "disease": "Early Blight",
        "desc": "Dark concentric-ring 'target' spots on older lower leaves with surrounding yellow halo.",
        "fertilizer": "Apply balanced NPK 10-10-10; avoid excess vegetative nitrogen top-dressing.",
        "nutrients": "Ensure potassium and calcium are plentiful. Potassium silicate spray helps.",
        "care": ["Prune off bottom 12 inches of foliage.", "Mulch ground with straw or plastic.",
                 "Water strictly at base of plant.", "Apply preventive chlorothalonil or copper."]
    },
    "Tomato___Late_blight": {
        "crop": "Tomato", "disease": "Late Blight",
        "desc": "Greasy water-soaked lesions turning brown-black with white fuzzy sporulation on leaf undersides.",
        "fertilizer": "Avoid high nitrogen. Use phosphorus-rich feeds to support root system.",
        "nutrients": "Maintain potassium and micronutrients (copper, zinc).",
        "care": ["Urgently spray systemic fungicide (e.g. Cymoxanil + Mancozeb).",
                 "Remove heavily infected plants to protect greenhouse/field.",
                 "Maximize air circulation and keep foliage bone dry."]
    },
    "Tomato___Leaf_Mold": {
        "crop": "Tomato", "disease": "Leaf Mold",
        "desc": "Pale yellow patches on upper leaf surface with olive-green velvety mold on the underside.",
        "fertilizer": "Moderate nitrogen only; soft leaves are highly vulnerable to mold spores.",
        "nutrients": "Calcium and boron improve leaf cuticle resistance.",
        "care": ["Open greenhouse vents to keep relative humidity below 85%.",
                 "Increase plant spacing.", "Remove infected lower leaves."]
    },
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato", "disease": "Septoria Leaf Spot",
        "desc": "Numerous small circular spots with gray centers and dark brown borders; black pycnidia specks inside.",
        "fertilizer": "Standard balanced fertilizer; avoid nutrient stress.",
        "nutrients": "Potassium supplementation strengthens foliage resistance.",
        "care": ["Prune lower leaves.", "Mulch heavily to block soil rain-splash.",
                 "Spray mancozeb or copper every 7-10 days in wet seasons."]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato", "disease": "Spider Mites (Two-Spotted)",
        "desc": "Fine yellow stippling/speckling on leaves, webbing on undersides, leaves turn bronze and dry out.",
        "fertilizer": "Avoid excess nitrogen which accelerates mite reproduction rates.",
        "nutrients": "Adequate potassium and sulfur.",
        "care": ["Spray neem oil or abamectin/bifenazate miticide on leaf undersides.",
                 "Introduce predatory mites (Phytoseiulus persimilis).",
                 "Maintain humidity to deter mites."]
    },
    "Tomato___Target_Spot": {
        "crop": "Tomato", "disease": "Target Spot",
        "desc": "Brown necrotic lesions with light brown centers and distinct concentric rings; causes severe defoliation.",
        "fertilizer": "Balanced NPK; avoid nitrogen starvation.",
        "nutrients": "Calcium and magnesium support leaf vigor.",
        "care": ["Improve plant spacing for airflow.", "Apply azoxystrobin or difenoconazole fungicide.",
                 "Remove plant debris immediately."]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato", "disease": "Yellow Leaf Curl Virus (TYLCV)",
        "desc": "Severe upward leaf curling, yellowing of margins, stunted bushy plant, flower drop; spread by whiteflies.",
        "fertilizer": "Balanced feeding to support unaffected shoots.",
        "nutrients": "Foliar zinc and boron.",
        "care": ["Control whitefly vectors using yellow sticky traps and imidacloprid / neem sprays.",
                 "Use insect-proof netting in nurseries.",
                 "Plant TYLCV-resistant hybrids (e.g., US-440, Saaho)."]
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop": "Tomato", "disease": "Tomato Mosaic Virus (ToMV)",
        "desc": "Mottling with alternating light and dark green areas, leaf distortion ('shoestringing'), stunted growth.",
        "fertilizer": "Standard fertilizer; infected plants will remain infected for life.",
        "nutrients": "Maintain balanced micronutrients.",
        "care": ["Wash hands with soap/milk before handling plants (tobacco users carry virus).",
                 "Sterilize all shears and stakes with 10% bleach solution.",
                 "Rogue out and destroy infected plants."]
    },
    "Tomato___healthy": {
        "crop": "Tomato", "disease": "Healthy",
        "desc": "No visible disease symptoms. Leaves are robust, deep green, and growing vigorously.",
        "fertilizer": "Basal 10-26-26 + split top-dressing of calcium nitrate and potash at fruiting.",
        "nutrients": "Spray 0.5% micronutrient mixture (Zn, Fe, B) at flower initiation.",
        "care": ["Maintain weekly field scouting.", "Consistent drip irrigation.", "Prune suckers regularly."]
    }
}

def get_advice(label: str) -> dict:
    """Returns the agronomic advice dictionary for any crop disease label."""
    # Direct match
    if label in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[label]

    # Normalized match (handling double/triple underscores and variations)
    norm = label.replace("__", "_").replace(" ", "_")
    for key, val in KNOWLEDGE_BASE.items():
        if key.replace("__", "_").replace(" ", "_").lower() == norm.lower():
            return val

    # Fallback generic parser
    parts = label.split("___")
    crop = parts[0].replace("_", " ") if len(parts) > 0 else "Crop"
    disease = parts[1].replace("_", " ") if len(parts) > 1 else "Condition"
    return {
        "crop": crop,
        "disease": disease,
        "desc": f"Detected condition: {disease} in {crop}. Confirm with a local agronomic expert.",
        "fertilizer": "Follow soil-test based balanced NPK fertilization schedule.",
        "nutrients": "Maintain balanced macronutrients (NPK) and micronutrients (Zn, Fe, B).",
        "care": [
            "Monitor crop foliage weekly for symptom progression.",
            "Remove severely damaged leaves and maintain field sanitation.",
            "Ensure proper water drainage and avoid overhead wetting of leaves."
        ]
    }
