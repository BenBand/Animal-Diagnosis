# Crop Detection Service for Zambia
# Recommends favorable crops based on province, weather, soil type, and rainfall patterns

# Zambia Provinces
PROVINCES = [
    {"id": "lusaka", "name": "Lusaka", "region": "Central"},
    {"id": "copperbelt", "name": "Copperbelt", "region": "North"},
    {"id": "southern", "name": "Southern", "region": "South"},
    {"id": "eastern", "name": "Eastern", "region": "East"},
    {"id": "western", "name": "Western", "region": "West"},
    {"id": "northern", "name": "Northern", "region": "North"},
    {"id": "luapula", "name": "Luapula", "region": "North"},
    {"id": "muchinga", "name": "Muchinga", "region": "North"},
    {"id": "north_western", "name": "North-Western", "region": "North-West"},
    {"id": "central", "name": "Central", "region": "Central"},
]

# Soil Types with descriptions
SOIL_TYPES = {
    "sandy": {
        "name": "Sandy Soil",
        "description": "Light, warm, drains quickly, low nutrient retention",
        "characteristics": ["Low water retention", "High drainage", "Warms quickly in spring", "Low fertility"]
    },
    "sandy_loam": {
        "name": "Sandy Loam",
        "description": "Mix of sand, silt, and clay - good for most crops",
        "characteristics": ["Good drainage", "Moderate water retention", "Easy to work", "Good fertility"]
    },
    "loam": {
        "name": "Loam",
        "description": "Ideal balance of sand, silt, and clay",
        "characteristics": ["Excellent water retention", "Good drainage", "High fertility", "Easy to work"]
    },
    "clay_loam": {
        "name": "Clay Loam",
        "description": "Heavy soil with good nutrient retention",
        "characteristics": ["Good water retention", "High fertility", "Can become compacted", "Slow to warm"]
    },
    "clay": {
        "name": "Clay Soil",
        "description": "Heavy, nutrient-rich but drains poorly",
        "characteristics": ["Excellent water retention", "High fertility", "Poor drainage", "Hard to work when wet"]
    },
    "black_cotton": {
        "name": "Black Cotton Soil",
        "description": "Dark, organic-rich soil found in valleys",
        "characteristics": ["Very high water retention", "High organic matter", "Good fertility", "Swells when wet"]
    }
}

# Rainfall categories
RAINFALL_LEVELS = {
    "low": {"min": 0, "max": 400, "description": "Low rainfall (0-400mm per season)"},
    "medium": {"min": 400, "max": 800, "description": "Medium rainfall (400-800mm per season)"},
    "high": {"min": 800, "max": 2000, "description": "High rainfall (800mm+ per season)"}
}

# Crop Database for Zambia
CROPS = {
    "maize": {
        "name": "Maize (Corn)",
        "suitable_soil": ["loam", "clay_loam", "clay"],
        "rainfall_min": 500,
        "rainfall_max": 800,
        "provinces": "all",
        "season": "November - March (Summer)",
        "description": "Staple crop in Zambia, widely grown across all provinces",
        "yield_per_hectare": "6-8 tons",
        "planting_tips": "Plant after first rains, use hybrid seeds for best results",
        "notes": "Most popular crop in Zambia"
    },
    "soybeans": {
        "name": "Soybeans",
        "suitable_soil": ["sandy_loam", "loam"],
        "rainfall_min": 600,
        "rainfall_max": 900,
        "provinces": ["lusaka", "central", "southern", "copperbelt"],
        "season": "November - February",
        "description": "High protein legume, good for soil nitrogen fixation",
        "yield_per_hectare": "1.5-2.5 tons",
        "planting_tips": "Inoculate seeds before planting for better nitrogen fixation",
        "notes": "Growing in popularity due to export demand"
    },
    "wheat": {
        "name": "Wheat",
        "suitable_soil": ["clay_loam", "loam"],
        "rainfall_min": 450,
        "rainfall_max": 650,
        "provinces": ["lusaka", "copperbelt", "central"],
        "season": "May - September (Winter)",
        "description": "Winter crop grown in cooler highland areas",
        "yield_per_hectare": "4-6 tons",
        "planting_tips": "Requires cool temperatures, irrigate if rainfall is low",
        "notes": "Mainly grown for commercial flour production"
    },
    "cassava": {
        "name": "Cassava",
        "suitable_soil": ["sandy", "sandy_loam", "loam"],
        "rainfall_min": 800,
        "rainfall_max": 1200,
        "provinces": ["northern", "luapula", "muchinga", "eastern", "western"],
        "season": "Year-round (plant in rainy season)",
        "description": "Drought-tolerant root crop, staple in northern provinces",
        "yield_per_hectare": "15-25 tons",
        "planting_tips": "Plant cuttings horizontally, needs well-drained soil",
        "notes": "Important food security crop"
    },
    "groundnuts": {
        "name": "Groundnuts (Peanuts)",
        "suitable_soil": ["sandy_loam", "loam"],
        "rainfall_min": 500,
        "rainfall_max": 700,
        "provinces": ["southern", "eastern", "central", "western"],
        "season": "November - February",
        "description": "High-value legume, good rotation crop",
        "yield_per_hectare": "1.5-2 tons",
        "planting_tips": "Plant in rows, requires good drainage",
        "notes": "Popular for both consumption and oil production"
    },
    "sorghum": {
        "name": "Sorghum",
        "suitable_soil": ["sandy", "sandy_loam", "loam"],
        "rainfall_min": 350,
        "rainfall_max": 500,
        "provinces": ["western", "southern", "eastern", "central"],
        "season": "November - February",
        "description": "Drought-resistant grain, good for dry areas",
        "yield_per_hectare": "2-4 tons",
        "planting_tips": "Can be planted late in the season",
        "notes": "Good for food security in drought-prone areas"
    },
    "sunflower": {
        "name": "Sunflower",
        "suitable_soil": ["loam", "sandy_loam", "clay_loam"],
        "rainfall_min": 400,
        "rainfall_max": 600,
        "provinces": ["central", "southern", "lusaka", "eastern"],
        "season": "November - February",
        "description": "Oilseed crop, good for crop rotation",
        "yield_per_hectare": "1.5-2.5 tons",
        "planting_tips": "Plant in full sun, thin seedlings to 30cm apart",
        "notes": "Growing demand for cooking oil"
    },
    "cotton": {
        "name": "Cotton",
        "suitable_soil": ["clay_loam", "loam"],
        "rainfall_min": 600,
        "rainfall_max": 900,
        "provinces": ["eastern", "luapula", "northern", "central"],
        "season": "November - March",
        "description": "Cash crop for export and textile industry",
        "yield_per_hectare": "1-1.5 tons (lint)",
        "planting_tips": "Requires pest management, harvest when bolls open",
        "notes": "Important export crop"
    },
    "rice": {
        "name": "Rice",
        "suitable_soil": ["clay", "clay_loam", "black_cotton"],
        "rainfall_min": 1200,
        "rainfall_max": 1800,
        "provinces": ["luapula", "northern", "eastern", "muchinga"],
        "season": "November - March",
        "description": "Grown in wetland areas and floodplains",
        "yield_per_hectare": "3-5 tons",
        "planting_tips": "Requires flooded fields or irrigation",
        "notes": "Traditional crop in northern region"
    },
    "sweet_potatoes": {
        "name": "Sweet Potatoes",
        "suitable_soil": ["sandy", "sandy_loam", "loam"],
        "rainfall_min": 500,
        "rainfall_max": 800,
        "provinces": "all",
        "season": "October - March",
        "description": "Easy to grow root crop, high vitamin content",
        "yield_per_hectare": "15-20 tons",
        "planting_tips": "Plant vine cuttings, harvest after 4-5 months",
        "notes": "Good for household food security"
    },
    "beans": {
        "name": "Beans (Common Beans)",
        "suitable_soil": ["sandy_loam", "loam", "clay_loam"],
        "rainfall_min": 400,
        "rainfall_max": 700,
        "provinces": "all",
        "season": "November - February",
        "description": "Protein-rich legume, good for rotation",
        "yield_per_hectare": "1-1.5 tons",
        "planting_tips": "Plant in rows, inoculate for nitrogen fixation",
        "notes": "Important protein source"
    },
    "cowpeas": {
        "name": "Cowpeas",
        "suitable_soil": ["sandy", "sandy_loam"],
        "rainfall_min": 300,
        "rainfall_max": 600,
        "provinces": ["southern", "western", "eastern", "central"],
        "season": "November - February",
        "description": "Drought-tolerant legume, dual-purpose (food + fodder)",
        "yield_per_hectare": "0.8-1.2 tons",
        "planting_tips": "Can be intercropped with maize",
        "notes": "Good for dry areas"
    }
}

# Province-specific climate data
PROVINCE_CLIMATE = {
    "lusaka": {
        "avg_temp": "20-28°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "800-1000mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "copperbelt": {
        "avg_temp": "18-26°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "1000-1200mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "southern": {
        "avg_temp": "22-30°C",
        "rainfall_season": "November - March",
        "typical_rainfall": "600-800mm",
        "best_season": "Summer (Nov-Feb)"
    },
    "eastern": {
        "avg_temp": "20-28°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "900-1100mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "western": {
        "avg_temp": "22-30°C",
        "rainfall_season": "November - March",
        "typical_rainfall": "500-700mm",
        "best_season": "Summer (Nov-Feb)"
    },
    "northern": {
        "avg_temp": "18-26°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "1000-1300mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "luapula": {
        "avg_temp": "18-26°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "1100-1400mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "muchinga": {
        "avg_temp": "18-25°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "900-1100mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "north_western": {
        "avg_temp": "20-28°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "900-1100mm",
        "best_season": "Summer (Nov-Mar)"
    },
    "central": {
        "avg_temp": "20-28°C",
        "rainfall_season": "November - April",
        "typical_rainfall": "800-1000mm",
        "best_season": "Summer (Nov-Mar)"
    }
}


def get_provinces():
    """Return list of all Zambia provinces"""
    return PROVINCES


def get_soil_types():
    """Return all soil types with descriptions"""
    return SOIL_TYPES


def get_rainfall_levels():
    """Return rainfall level categories"""
    return RAINFALL_LEVELS


def get_crops():
    """Return all crops"""
    return CROPS


def get_province_climate(province_id):
    """Get climate data for a specific province"""
    return PROVINCE_CLIMATE.get(province_id, {})


def calculate_suitability(crop, province, soil_type, rainfall_level, weather_conditions=None):
    """
    Calculate how suitable a crop is for the given conditions
    
    Returns: tuple (suitability_score, reasons)
    """
    score = 0
    reasons = []
    
    # Check soil compatibility (40% weight)
    if soil_type in crop.get("suitable_soil", []):
        soil_index = list(CROPS[crop].get("suitable_soil", [])).index(soil_type)
        if soil_index == 0:  # Best soil
            score += 40
            reasons.append(f"Optimal soil type: {SOIL_TYPES.get(soil_type, {}).get('name', soil_type)}")
        else:
            score += 25
            reasons.append(f"Acceptable soil type: {SOIL_TYPES.get(soil_type, {}).get('name', soil_type)}")
    else:
        # Check if any soil in the crop's suitable list matches better
        suitable_soils = crop.get("suitable_soil", [])
        if suitable_soils:
            score += 10
            reasons.append(f"Suboptimal soil - crop prefers {suitable_soils[0]}")
    
    # Check rainfall compatibility (30% weight)
    rainfall_range = RAINFALL_LEVELS.get(rainfall_level, {})
    rainfall_min = rainfall_range.get("min", 500)
    rainfall_max = rainfall_range.get("max", 800)
    crop_min = crop.get("rainfall_min", 500)
    crop_max = crop.get("rainfall_max", 800)
    
    # Check if rainfall falls within crop needs
    if rainfall_min <= crop_min and rainfall_max >= crop_max:
        score += 30
        reasons.append(f"Rainfall level matches crop needs")
    elif rainfall_min >= crop_min * 0.8 and rainfall_max <= crop_max * 1.2:
        score += 20
        reasons.append(f"Rainfall is within acceptable range")
    else:
        score += 5
        reasons.append(f"Rainfall may be suboptimal for this crop")
    
    # Check province compatibility (20% weight)
    province_list = crop.get("provinces", [])
    if province == "all" or province in province_list:
        score += 20
        reasons.append(f"Grown successfully in this province")
    elif province_list and len(province_list) > 0:
        # Check neighboring provinces or similar regions
        score += 5
        reasons.append(f"Crop may grow with extra care in this province")
    
    # Weather conditions bonus (10% weight)
    if weather_conditions:
        temp = weather_conditions.get("temperature", "").lower()
        humidity = weather_conditions.get("humidity", "").lower()
        
        # Temperature preferences
        if "warm" in temp or "hot" in temp:
            if crop.get("name") in ["Maize", "Sorghum", "Groundnuts", "Sunflower"]:
                score += 10
                reasons.append(f"Weather conditions are favorable")
        elif "cool" in temp or "mild" in temp:
            if crop.get("name") in ["Wheat", "Beans"]:
                score += 10
                reasons.append(f"Weather conditions are favorable")
        
        # Humidity preferences
        if "high" in humidity and crop.get("name") in ["Rice", "Cassava"]:
            score += 5
            reasons.append(f"High humidity suits this crop")
    
    return score, reasons


def get_crop_recommendations(province, soil_type, rainfall_level, weather_conditions=None, max_results=5):
    """
    Get crop recommendations based on input conditions
    
    Args:
        province: Province ID (e.g., "southern", "lusaka")
        soil_type: Soil type ID (e.g., "sandy_loam", "clay")
        rainfall_level: "low", "medium", or "high"
        weather_conditions: Optional dict with temperature and humidity
        max_results: Maximum number of recommendations
    
    Returns:
        List of recommended crops with suitability scores and reasons
    """
    recommendations = []
    
    for crop_id, crop_data in CROPS.items():
        score, reasons = calculate_suitability(
            crop_id, province, soil_type, rainfall_level, weather_conditions
        )
        
        if score > 20:  # Only include crops with at least 20% suitability
            # Get province climate info
            climate = get_province_climate(province)
            
            recommendation = {
                "crop": crop_data["name"],
                "crop_id": crop_id,
                "suitability": min(100, score),  # Cap at 100%
                "reasons": reasons,
                "season": crop_data["season"],
                "yield": crop_data["yield_per_hectare"],
                "planting_tips": crop_data["planting_tips"],
                "description": crop_data["description"],
            }
            recommendations.append(recommendation)
    
    # Sort by suitability score (highest first)
    recommendations.sort(key=lambda x: x["suitability"], reverse=True)
    
    return recommendations[:max_results]


def get_crop_by_name(crop_name):
    """Get crop details by name"""
    crop_name_lower = crop_name.lower()
    for crop_id, crop_data in CROPS.items():
        if crop_name_lower in crop_data["name"].lower() or crop_name_lower in crop_id:
            return crop_data
    return None