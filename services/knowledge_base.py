"""
Knowledge Base Module
Provides structured agricultural knowledge with search capability
Supports future RAG (Retrieval-Augmented Generation) integration
"""
from typing import List, Dict, Optional, Tuple
import json
import os


class KnowledgeBase:
    """
    Structured knowledge base for livestock, aquaculture, crops and agriculture
    Can be extended with vector embeddings for semantic search
    """
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path or 'knowledge_base/'
        self.topics = {}
        self._load_knowledge()
    
    def _load_knowledge(self):
        """Load knowledge base data"""
        self.topics = {
            # === LIVESTOCK ===
            'cattle': {
                'breeds': ['Holstein', 'Angus', 'Hereford', 'Brahman', 'Charolais', 'Jersey', 'Guernsey'],
                'uses': ['dairy', 'beef', 'dual-purpose'],
                'lifespan_years': '15-20',
                'gestation_months': 9,
                'feeding': {
                    'calves': 'Milk replacer, starter feed, hay',
                    'adults': 'Grass, hay, grains, minerals',
                    'dairy': 'Higher energy feed, protein supplements'
                },
                'common_diseases': ['mastitis', 'bovine TB', 'foot and mouth', 'anthrax'],
                'housing': 'Fenced pastures with shelter, clean water access',
                'care_tips': [
                    'Provide clean water at all times',
                    'Ensure adequate shade in hot weather',
                    'Regular hoof trimming every 6-8 weeks',
                    'Vaccinate according to local schedule',
                    'Monitor milk production daily for dairy'
                ]
            },
            'poultry': {
                'types': ['chickens', 'ducks', 'turkeys', 'geese', 'guinea fowl'],
                'uses': ['eggs', 'meat', 'pest control'],
                'feeding': {
                    'chicks': 'Starter feed (0-6 weeks)',
                    'growers': 'Grower feed (6-20 weeks)',
                    'layers': 'Layer feed with calcium',
                    'meat': 'Broiler feed'
                },
                'housing': 'Coop with nesting boxes, perches, run space',
                'common_diseases': ['Newcastle disease', 'Avian flu', 'Mareks disease', 'Coccidiosis'],
                'care_tips': [
                    'Keep coop clean and well-ventilated',
                    'Collect eggs frequently',
                    'Provide dust baths for parasites',
                    'Ensure 14-16 hours of light for layers',
                    'Quarantine new birds for 2 weeks'
                ]
            },
            'sheep': {
                'breeds': ['Merino', 'Suffolk', 'Dorper', 'Katahdin', 'Romney'],
                'uses': ['wool', 'meat', 'milk'],
                'lifespan_years': '10-12',
                'gestation_months': 5,
                'feeding': {
                    'lambs': 'Milk, creep feed, hay',
                    'adults': 'Pasture, hay, minerals',
                    'breeding': 'Increased energy before breeding'
                },
                'housing': 'Fenced pastures, shelter from rain',
                'common_diseases': ['Foot rot', 'Scrapie', 'Bluetongue', 'Pneumonia'],
                'care_tips': [
                    'Shear annually for wool production',
                    'Check feet regularly for foot rot',
                    'Provide shelter from extreme weather',
                    'Lambling requires warm, clean environment',
                    'Vaccinate for clostridial diseases'
                ]
            },
            'goats': {
                'breeds': ['Nubian', 'Boer', 'Alpine', 'Saanen', 'Kiko'],
                'uses': ['meat', 'milk', 'fiber'],
                'lifespan_years': '15-18',
                'gestation_months': 5,
                'feeding': {
                    'kids': 'Milk, starter feed',
                    'adults': 'Browse, grass, hay, grains',
                    'dairy': 'High-quality feed for milk production'
                },
                'housing': 'Fenced area with shelter, climbing structures',
                'common_diseases': ['CAE', 'CL', 'Internal parasites', 'Pneumonia'],
                'care_tips': [
                    'Goats are browsers, not grazers - provide shrubs',
                    'Ensure constant access to clean water',
                    'Hoof trim every 4-6 weeks',
                    'Separate sick animals immediately',
                    'Provide mineral supplements'
                ]
            },
            # === AQUACULTURE / FISH FARMING ===
            'fish_farming': {
                'types': {
                    'tilapia': {
                        'name': 'Tilapia',
                        'water_temp': '20-30C',
                        'feed': 'Floating pellets, vegetables, algae',
                        'harvest_months': '6-8',
                        'stocking_density': '10-15 fish per m3'
                    },
                    'catfish': {
                        'name': 'African Catfish (Clarias)',
                        'water_temp': '25-32C',
                        'feed': 'Floating pellets, fish meal, worms',
                        'harvest_months': '8-12',
                        'stocking_density': '5-10 fish per m3'
                    },
                    'carp': {
                        'name': 'Common Carp',
                        'water_temp': '15-25C',
                        'feed': 'Natural plankton, vegetables, pellets',
                        'harvest_months': '12-18',
                        'stocking_density': '5-8 fish per m3'
                    }
                },
                'pond_requirements': [
                    'Adequate water supply (year-round)',
                    'Proper drainage system',
                    'Soil with low permeability (clay)',
                    'Depth of 1.5-2 meters',
                    'Aeration for intensive systems'
                ],
                'water_quality': {
                    'ph': '6.5-8.5',
                    'dissolved_oxygen': 'Above 5 mg/L',
                    'ammonia': 'Below 0.02 mg/L',
                    'temperature': 'Species dependent'
                },
                'common_diseases': ['Fin rot', 'Ich (white spot)', 'Fungal infections', 'Bacterial gill disease'],
                'feeding_schedule': '2-3 times daily, amount based on fish weight',
                'care_tips': [
                    'Monitor water quality weekly',
                    'Avoid overstocking',
                    'Quarantine new fish for 2 weeks',
                    'Remove dead fish immediately',
                    'Provide adequate aeration',
                    'Harvest at optimal size for market'
                ]
            },
            # === CROP FARMING ===
            'crops': {
                'cereals': {
                    'maize': {
                        'planting_season': 'October-December (rainy season)',
                        'harvest_season': 'March-June',
                        'days_to_maturity': '90-120 days',
                        'spacing': '75cm between rows, 25cm between plants',
                        'fertilizer': 'NPK 200kg/ha + organic manure',
                        'water_needs': '500-600mm per season'
                    },
                    'wheat': {
                        'planting_season': 'May-July (winter)',
                        'harvest_season': 'October-December',
                        'days_to_maturity': '120-150 days',
                        'spacing': '15-20cm between rows',
                        'fertilizer': 'NPK 100-150kg/ha',
                        'water_needs': '450-650mm per season'
                    },
                    'rice': {
                        'planting_season': 'November-January',
                        'harvest_season': 'April-June',
                        'days_to_maturity': '120-150 days',
                        'spacing': '20x20cm (transplanted)',
                        'fertilizer': 'NPK 150-200kg/ha',
                        'water_needs': 'Flooded conditions'
                    }
                },
                'vegetables': {
                    'tomatoes': {
                        'planting_season': 'All year (irrigation) / March-June (rainfed)',
                        'harvest_season': '60-90 days after transplanting',
                        'days_to_maturity': '90-120 days',
                        'spacing': '60cm between rows, 45cm between plants',
                        'fertilizer': 'NPK 200kg/ha + calcium',
                        'water_needs': '400-600mm, regular watering'
                    },
                    'onions': {
                        'planting_season': 'March-June',
                        'harvest_season': '120-150 days after planting',
                        'days_to_maturity': '120-150 days',
                        'spacing': '15cm between rows, 10cm between plants',
                        'fertilizer': 'NPK 150kg/ha',
                        'water_needs': '350-550mm'
                    },
                    'cabbage': {
                        'planting_season': 'March-August',
                        'harvest_season': '90-120 days after transplanting',
                        'days_to_maturity': '90-120 days',
                        'spacing': '60cm between rows, 45cm between plants',
                        'fertilizer': 'NPK 200kg/ha',
                        'water_needs': '400-500mm'
                    }
                },
                'legumes': {
                    'beans': {
                        'planting_season': 'November-January (rainy)',
                        'harvest_season': '60-90 days after planting',
                        'days_to_maturity': '60-90 days',
                        'spacing': '50cm between rows, 10cm between plants',
                        'fertilizer': 'NPK 50kg/ha, inoculant recommended',
                        'water_needs': '300-500mm'
                    },
                    'groundnuts': {
                        'planting_season': 'November-January',
                        'harvest_season': '120-150 days after planting',
                        'days_to_maturity': '120-150 days',
                        'spacing': '45cm between rows, 15cm between plants',
                        'fertilizer': 'NPK 40kg/ha, lime if needed',
                        'water_needs': '450-600mm'
                    }
                },
                'care_tips': [
                    'Start with soil testing',
                    'Use certified seeds',
                    'Follow recommended planting densities',
                    'Apply fertilizer at right growth stages',
                    'Control weeds early',
                    'Monitor for pests and diseases',
                    'Harvest at optimal maturity'
                ]
            },
            # === GENERAL AGRICULTURE ===
            'nutrition': {
                'essential_nutrients': [
                    'Carbohydrates - energy source',
                    'Proteins - muscle growth, milk production',
                    'Fats - energy, vitamin absorption',
                    'Vitamins - A, D, E, K (fat-soluble), B complex',
                    'Minerals - calcium, phosphorus, salt, trace elements',
                    'Water - most essential nutrient'
                ],
                'feeding_practices': [
                    'Feed at regular times',
                    'Provide clean, fresh water always',
                    'Transition feed gradually',
                    'Store feed properly to prevent mold',
                    'Consider supplementary feeding in dry season'
                ],
                'common_feeds': {
                    'roughages': ['grass', 'hay', 'silage', 'legumes'],
                    'concentrates': ['corn', 'wheat', 'barley', 'soybean', 'cottonseed'],
                    'byproducts': ['bran', 'molasses', 'brewers grains']
                }
            },
            'disease_prevention': {
                'biosecurity': [
                    'Limit farm access to essential personnel',
                    'Use foot baths and disinfectant',
                    'Quarantine new animals 2-4 weeks',
                    'Control wildlife and pest access',
                    'Clean and disinfect equipment regularly'
                ],
                'vaccination_schedule': [
                    'Consult local veterinarian',
                    'Keep vaccination records',
                    'Maintain cold chain for vaccines',
                    'Vaccinate healthy animals only',
                    'Follow label directions'
                ],
                'signs_of_illness': [
                    'Lethargy or weakness',
                    'Loss of appetite',
                    'Changes in behavior',
                    'Abnormal breathing or coughing',
                    'Diarrhea or constipation',
                    'Abnormal discharge',
                    'Fever (hot ears, dry nose)'
                ]
            },
            'weather_management': {
                'heat_stress': {
                    'signs': ['panting', 'drooling', 'reduced feeding', 'seeking shade'],
                    'prevention': [
                        'Provide ample shade',
                        'Ensure constant cool water',
                        'Use fans or misters',
                        'Schedule activities for cooler hours',
                        'Provide electrolyte supplements'
                    ]
                },
                'cold_stress': {
                    'signs': ['shivering', 'huddling', 'reduced milk production'],
                    'prevention': [
                        'Provide windbreak shelter',
                        'Ensure dry, warm bedding',
                        'Increase feed for energy',
                        'Use calf jackets for young animals',
                        'Check water sources for freezing'
                    ]
                },
                'rainy_season': [
                    'Ensure good drainage in pens',
                    'Move animals to shelter',
                    'Check for flooding in low areas',
                    'Monitor for disease outbreaks',
                    'Store feed properly to prevent mold'
                ]
            },
            # === SEASONAL FARMER TIPS ===
            'seasonal_tips': {
                'october': {
                    'title': 'Land Preparation',
                    'crop_tips': ['Clear fields', 'Test soil pH', 'Buy seeds early'],
                    'livestock_tips': ['Vaccinate animals', 'Dip cattle', 'Repair fences']
                },
                'november': {
                    'title': 'Planting Season Starts',
                    'crop_tips': ['Plant early maize', 'Apply basal fertilizer', 'Control weeds'],
                    'livestock_tips': ['Move to fresh pastures', 'Check water sources']
                },
                'december': {
                    'title': 'Mid-Season',
                    'crop_tips': ['Top dress maize', 'Scout for pests', 'Replant gaps'],
                    'livestock_tips': ['Ensure shade access', 'Monitor for disease']
                },
                'january': {
                    'title': 'Peak Rainy Season',
                    'crop_tips': ['Late planting window', 'Pest monitoring', 'Drainage'],
                    'livestock_tips': ['Check for foot rot', 'Extra shelter if needed']
                },
                'february': {
                    'title': 'Pre-Harvest',
                    'crop_tips': ['Armyworm control', 'Second fertilizer', 'Prepare storage'],
                    'livestock_tips': ['Hoof trimming', 'Prepare dry season feed']
                },
                'march': {
                    'title': 'Early Harvest',
                    'crop_tips': ['Harvest early crops', 'Dry properly', 'Store safely'],
                    'livestock_tips': ['Start supplementary feeding', 'Market surplus']
                },
                'april': {
                    'title': 'Main Harvest',
                    'crop_tips': ['Harvest maize/soybeans', 'Thresh and store', 'Sell surplus'],
                    'livestock_tips': ['Sell before dry season', 'Cull weak animals']
                },
                'may': {
                    'title': 'Post-Harvest',
                    'crop_tips': ['Plant cover crops', 'Soil testing', 'Plan next season'],
                    'livestock_tips': ['Prepare winter feed', 'Build reserves']
                },
                'june': {
                    'title': 'Dry Season Begins',
                    'crop_tips': ['Irrigate if possible', 'Mulch to conserve moisture'],
                    'livestock_tips': ['Critical water management', 'Reduce herd if needed']
                },
                'july': {
                    'title': 'Mid Dry Season',
                    'crop_tips': ['Buy inputs for new season', 'Repair equipment'],
                    'livestock_tips': ['Most critical water period', 'Emergency feeding']
                },
                'august': {
                    'title': 'Late Dry Season',
                    'crop_tips': ['Soil conservation', 'Water harvesting'],
                    'livestock_tips': ['Closely monitor', 'Prepare for rains']
                },
                'september': {
                    'title': 'New Season Prep',
                    'crop_tips': ['Buy seeds/fertilizer', 'Prepare land'],
                    'livestock_tips': ['Vaccination programs', 'Dip tanks operational']
                }
            }
        }
    
    def search(self, query: str) -> List[Tuple[str, any]]:
        """Search knowledge base for relevant information"""
        query_lower = query.lower()
        results = []
        
        for topic, content in self.topics.items():
            if topic in query_lower:
                results.append((topic, content))
            elif isinstance(content, dict):
                for key, value in content.items():
                    if key in query_lower:
                        results.append((f"{topic}.{key}", value))
        
        return results
    
    def get_topic(self, topic: str) -> Optional[Dict]:
        """Get specific topic information"""
        return self.topics.get(topic.lower())
    
    def get_answer(self, question: str) -> Optional[str]:
        """Get formatted answer for a question"""
        question_lower = question.lower()
        
        # Keyword-based matching - expanded for fish and crops
        keyword_map = {
            'cattle': 'cattle',
            'cow': 'cattle',
            'cows': 'cattle',
            'chicken': 'poultry',
            'poultry': 'poultry',
            'duck': 'poultry',
            'turkey': 'poultry',
            'sheep': 'sheep',
            'goat': 'goats',
            'goats': 'goats',
            'fish': 'fish_farming',
            'tilapia': 'fish_farming',
            'catfish': 'fish_farming',
            'carp': 'fish_farming',
            'aquaculture': 'fish_farming',
            'pond': 'fish_farming',
            'maize': 'crops',
            'corn': 'crops',
            'wheat': 'crops',
            'rice': 'crops',
            'tomato': 'crops',
            'onion': 'crops',
            'cabbage': 'crops',
            'beans': 'crops',
            'groundnuts': 'crops',
            'crop': 'crops',
            'plant': 'crops',
            'planting': 'crops',
            'harvest': 'crops',
            'feed': 'nutrition',
            'nutrition': 'nutrition',
            'food': 'nutrition',
            'disease': 'disease_prevention',
            'sick': 'disease_prevention',
            'health': 'disease_prevention',
            'weather': 'weather_management',
            'heat': 'weather_management',
            'cold': 'weather_management',
            'season': 'seasonal_tips',
            'month': 'seasonal_tips',
            'when to': 'seasonal_tips',
            'tips': 'seasonal_tips',
            'advice': 'seasonal_tips',
            'farming calendar': 'seasonal_tips'
        }
        
        for keyword, topic in keyword_map.items():
            if keyword in question_lower:
                info = self.get_topic(topic)
                if info:
                    return self._format_topic(topic, info)
        
        return None
    
    def _format_topic(self, topic: str, info: any) -> str:
        """Format topic information as readable response"""
        if isinstance(info, dict):
            lines = [f"**{topic.upper().replace('_', ' ')}:**", ""]
            
            if topic == 'cattle':
                if 'breeds' in info:
                    lines.append(f"Common breeds: {', '.join(info['breeds'][:5])}")
                if 'lifespan_years' in info:
                    lines.append(f"Lifespan: {info['lifespan_years']} years")
                if 'gestation_months' in info:
                    lines.append(f"Gestation: {info['gestation_months']} months")
                if 'feeding' in info:
                    lines.append(f"Feeding: {info['feeding']}")
                if 'care_tips' in info:
                    lines.append("Care tips:")
                    for tip in info['care_tips'][:3]:
                        lines.append(f"  - {tip}")
            
            elif topic == 'fish_farming':
                if 'types' in info:
                    lines.append("Fish types available:")
                    for fish_type, details in info['types'].items():
                        lines.append(f"  - {details['name']}: Temp {details['water_temp']}, Harvest {details['harvest_months']} months")
                if 'care_tips' in info:
                    lines.append("Care tips:")
                    for tip in info['care_tips'][:4]:
                        lines.append(f"  - {tip}")
            
            elif topic == 'crops':
                if 'care_tips' in info:
                    lines.append("General crop tips:")
                    for tip in info['care_tips']:
                        lines.append(f"  - {tip}")
                else:
                    lines.append("Crop information available. Ask about specific crops like maize, wheat, rice, vegetables, or legumes.")
            
            elif topic == 'nutrition':
                if 'essential_nutrients' in info:
                    lines.append("Essential nutrients:")
                    for nutrient in info['essential_nutrients'][:4]:
                        lines.append(f"  - {nutrient}")
            
            elif topic == 'disease_prevention':
                if 'signs_of_illness' in info:
                    lines.append("Common signs of illness:")
                    for sign in info['signs_of_illness'][:4]:
                        lines.append(f"  - {sign}")
            
            elif topic == 'seasonal_tips':
                from datetime import datetime
                current_month = datetime.now().strftime('%B').lower()
                if current_month in info:
                    month_data = info[current_month]
                    lines.append(f"Current: **{month_data['title']}**")
                    lines.append("Crop: " + ", ".join(month_data.get('crop_tips', [])[:3]))
                    lines.append("Livestock: " + ", ".join(month_data.get('livestock_tips', [])[:3]))
                else:
                    lines.append("Monthly tips: " + ", ".join([m.title() for m in info.keys()]))
            
            return "\n".join(lines)
        
        return str(info)
    
    def get_farming_tips(self) -> str:
        """Get general farming tips"""
        tips = []
        
        for topic, info in self.topics.items():
            if 'care_tips' in info:
                tips.extend(info['care_tips'][:2])
        
        if tips:
            return "**General Farming Tips:**\n" + "\n".join([f"- {tip}" for tip in tips[:8]])
        return "No tips available"


# Singleton
_knowledge_base = None


def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base


if __name__ == "__main__":
    kb = get_knowledge_base()
    
    print("Testing Knowledge Base:")
    print(kb.get_answer("What do fish need in a pond?"))
    print("\n" + "="*50 + "\n")
    print(kb.get_answer("When to plant maize?"))
    print("\n" + "="*50 + "\n")
    print(kb.get_farming_tips())
