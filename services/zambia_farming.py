"""
Zambia Agricultural Module
Provides Zambia-specific farming information for Bena
"""
from typing import Dict, List, Optional


class ZambiaFarming:
    """
    Zambia-specific agricultural knowledge base
    Covers provinces, crops, livestock, markets, and government programs
    """
    
    def __init__(self):
        self._load_zambia_data()
    
    def _load_zambia_data(self):
        """Load Zambia-specific farming data"""
        
        # Agricultural Zones by Province
        self.provinces = {
            'southern': {
                'name': 'Southern Province',
                'main_crops': ['Maize', 'Sugarcane', 'Vegetables', 'Wheat', 'Soya beans'],
                'main_livestock': ['Cattle', 'Dairy goats', 'Poultry'],
                'climate': 'Subtropical, rainfall 800-1000mm/year',
                'farming_systems': 'Mixed crop-livestock, irrigation for sugarcane',
                'key_towns': ['Mazabuka', 'Chikankata', 'Livingstone', 'Kalomo'],
                'specialties': 'Dairy farming (Mazabuka Dairy), Sugarcane (Zambia Sugar)'
            },
            'central': {
                'name': 'Central Province',
                'main_crops': ['Maize', 'Tobacco', 'Wheat', 'Soybeans', 'Cassava'],
                'main_livestock': ['Cattle', 'Goats', 'Poultry'],
                'climate': 'Subtropical, rainfall 900-1100mm/year',
                'farming_systems': 'Tobacco rotation with maize, cattle ranching',
                'key_towns': ['Kabwe', 'Serenje', 'Mkushi', 'Kapiri Mposhi'],
                'specialties': 'Tobacco farming, Beef cattle'
            },
            'copperbelt': {
                'name': 'Copperbelt Province',
                'main_crops': ['Maize', 'Vegetables', 'Cassava', 'Sweet potatoes'],
                'main_livestock': ['Poultry', 'Pigs', 'Goats', 'Cattle'],
                'climate': 'Subtropical, rainfall 1000-1200mm/year',
                'farming_systems': 'Small-scale market gardening, urban livestock',
                'key_towns': ['Kitwe', 'Mufulira', 'Chingola', 'Ndola'],
                'specialties': 'Market gardening for urban centers, pig farming'
            },
            'eastern': {
                'name': 'Eastern Province',
                'main_crops': ['Maize', 'Tobacco', 'Groundnuts', 'Cassava', 'Beans'],
                'main_livestock': ['Cattle', 'Goats', 'Poultry'],
                'climate': 'Subtropical, rainfall 1000-1200mm/year',
                'farming_systems': 'Tobacco-maize rotation, groundnut-legume systems',
                'key_towns': ['Chipata', 'Lundazi', 'Petauke', 'Katete'],
                'specialties': 'Tobacco, Groundnuts, Bean exports'
            },
            'northern': {
                'name': 'Northern Province',
                'main_crops': ['Coffee', 'Beans', 'Maize', 'Cassava', 'Rice'],
                'main_livestock': ['Cattle', 'Goats', 'Poultry', 'Pigs'],
                'climate': 'Tropical, rainfall 1200-1400mm/year',
                'farming_systems': 'Coffee agroforestry, rice in valleys',
                'key_towns': ['Kasama', 'Mpika', 'Luwingu', 'Mpulungu'],
                'specialties': 'Zambia coffee (Arabica), Rice paddies'
            },
            'western': {
                'name': 'Western Province',
                'main_crops': ['Maize', 'Cassava', 'Sorghum', 'Millet', 'Rice'],
                'main_livestock': ['Cattle', 'Goats', 'Sheep'],
                'climate': 'Subtropical, rainfall 800-1000mm/year',
                'farming_systems': 'Barotse floodplain systems, cattle ranching',
                'key_towns': ['Mongu', 'Kalabo', 'Senanga', 'Lukulu'],
                'specialties': 'Barotse floodplain rice, Barotse cattle (Sable)'
            },
            'luapula': {
                'name': 'Luapula Province',
                'main_crops': ['Cassava', 'Maize', 'Beans', 'Groundnuts', 'Rice'],
                'main_livestock': ['Cattle', 'Goats', 'Poultry', 'Fish'],
                'climate': 'Tropical, rainfall 1100-1300mm/year',
                'farming_systems': 'Cassava-based, lake fisheries, valley rice',
                'key_towns': ['Mansa', 'Kawambwa', 'Samfya', 'Mwense'],
                'specialties': 'Lake fisheries (Lake Mweru), Cassava processing'
            },
            'muchinga': {
                'name': 'Muchinga Province',
                'main_crops': ['Maize', 'Soybeans', 'Wheat', 'Tobacco', 'Cassava'],
                'main_livestock': ['Cattle', 'Goats', 'Poultry'],
                'climate': 'Subtropical, rainfall 900-1100mm/year',
                'farming_systems': 'Tobacco, wheat, cattle ranching',
                'key_towns': ['Mbala', 'Isoka', 'Chinsali', 'Mwinilunga'],
                'specialties': 'Wheat farming (Kateshi), Cattle ranching'
            }
        }
        
        # Zambian Seasonal Calendar
        self.seasonal_calendar = {
            'october': {
                'activity': 'Land preparation begins',
                'crops': 'Plant early maize in low rainfall areas',
                'livestock': 'Vaccination programs, dip tank treatment'
            },
            'november': {
                'activity': 'Main planting season starts',
                'crops': 'Plant maize, soybeans, tobacco',
                'livestock': 'Move animals to fresh pastures'
            },
            'december': {
                'activity': 'Weed control critical',
                'crops': 'Top dressing fertilizer for maize',
                'livestock': 'Check water availability'
            },
            'january': {
                'activity': 'Peak rainfall season',
                'crops': 'Late planting continues, scout for pests',
                'livestock': 'Watch for disease outbreaks in wet season'
            },
            'february': {
                'activity': 'Mid-season management',
                'crops': 'Pest control (armyworm), sidedress nitrogen',
                'livestock': 'Foot rot common - check hooves'
            },
            'march': {
                'activity': 'Early harvest begins',
                'crops': 'Harvest early maize, groundnuts',
                'livestock': 'Start supplementary feeding'
            },
            'april': {
                'activity': 'Main harvest season',
                'crops': 'Harvest maize, soybeans, tobacco',
                'livestock': 'Market livestock before dry season'
            },
            'may': {
                'activity': 'Post-harvest, land clearing',
                'crop': 'Stalk borer control in maize residue',
                'livestock': 'Prepare for dry season, cull old animals'
            },
            'june': {
                'activity': 'Dry season begins',
                'crop': 'Post-harvest storage, sell surplus',
                'livestock': 'Supplementary feeding, water management'
            },
            'july': {
                'activity': 'Dry season peaks',
                'crop': 'Plan next season, buy inputs',
                'livestock': 'Critical water shortage period'
            },
            'august': {
                'activity': 'Late dry season',
                'crop': 'Soil testing, conservation planning',
                'livestock': 'Most critical period - monitor closely'
            },
            'september': {
                'activity': 'Land preparation begins',
                'crop': 'Buy seeds, fertilizer for new season',
                'livestock': 'Vaccination, dip programs restart'
            }
        }
        
        # Major Markets in Zambia
        self.markets = {
            'soweto_market': {
                'name': 'Soweto Market',
                'location': 'Lusaka',
                'description': 'Largest wholesale market in Zambia',
                'products': 'All fresh produce, cereals, livestock',
                'note': 'Prices fluctuate daily - go early morning'
            },
            'kabwe_central': {
                'name': 'Kabwe Central Market',
                'location': 'Kabwe',
                'description': 'Main market for Central Province',
                'products': 'Maize, tobacco, vegetables, cattle'
            },
            'kasumbalesa': {
                'name': 'Kasumbalesa Border',
                'location': 'Copperbelt/Congo border',
                'description': 'Major export point to DRC',
                'products': 'Vegetables, maize, beans, chickens'
            },
            'chinsali': {
                'name': 'Chinsali Market',
                'location': 'Muchinga',
                'description': 'Northern trading hub',
                'products': 'Wheat, soy, cattle, goats'
            },
            'mongu': {
                'name': 'Mongu Market',
                'location': 'Western Province',
                'description': 'Barotse floodplain produce',
                'products': 'Rice, fish, cattle, maize'
            }
        }
        
        # Government Programs
        self.govt_programs = {
            'frdp': {
                'name': 'Farm Input Support Programme (FISP)',
                'description': 'Subsidized fertilizer and seeds for smallholder farmers',
                'eligibility': 'Registered farmers, vulnerable households',
                'benefits': '50% subsidy on fertilizer, free seeds',
                'how_to_apply': 'Through agricultural camps in your district'
            },
            'livestock_program': {
                'name': 'Livestock Development Programme',
                'description': 'Support for cattle, goat, and poultry farmers',
                'eligibility': 'Registered livestock farmers',
                'benefits': 'Veterinary services, dip tanks, AI services',
                'how_to_apply': 'Contact District Veterinary Officer'
            },
            'fisheries': {
                'name': 'Fisheries Development Programme',
                'description': 'Support for fish farmers and fisherfolk',
                'eligibility': 'Fish farmers, fishing communities',
                'benefits': 'Fingerlings, pond construction, training',
                'how_to_apply': 'Through Department of Fisheries'
            },
            'farmer_training': {
                'name': 'Farmers Training Institute (FTI)',
                'description': 'Agricultural extension and training services',
                'services': 'Crop management, livestock care, business skills',
                'how_to_apply': 'Contact local agricultural camp'
            },
            'climate_smart': {
                'name': 'Climate Smart Agriculture',
                'description': 'Drought-resistant techniques and irrigation',
                'eligibility': 'All farmers, especially in drought-prone areas',
                'benefits': 'Conservation farming, irrigation kits',
                'how_to_apply': 'Through Ministry of Agriculture'
            }
        }
        
        # Common Challenges
        self.challenges = {
            'drought': {
                'description': 'Irregular rainfall, especially in Southern and Western provinces',
                'solutions': [
                    'Practice conservation farming',
                    'Use drought-tolerant varieties',
                    'Install irrigation where possible',
                    'Diversify crops (include cassava, sorghum)'
                ]
            },
            'market_access': {
                'description': 'Poor roads, lack of storage, low prices',
                'solutions': [
                    'Form farmer cooperatives',
                    'Use solar drying for preservation',
                    'Sell at multiple markets',
                    'Contract farming with buyers'
                ]
            },
            'veterinary_access': {
                'description': 'Limited vets in rural areas',
                'solutions': [
                    'Use veterinary camps',
                    'Learn basic animal health',
                    'Use community livestock helpers',
                    'Report diseases early'
                ]
            },
            'post_harvest': {
                'description': 'Storage losses, spoilage, pests',
                'solutions': [
                    'Proper drying before storage',
                    'Use hermetic bags (PICS bags)',
                    'Build raised storage structures',
                    'Process into higher-value products'
                ]
            }
        }
    
    def get_province_info(self, province: str = None) -> Dict:
        """Get information about a specific province or all provinces"""
        if province:
            return self.provinces.get(province.lower(), {})
        return self.provinces
    
    def get_season_info(self, month: str = None) -> Dict:
        """Get seasonal activities for a month"""
        if month:
            return self.seasonal_calendar.get(month.lower(), {})
        return self.seasonal_calendar
    
    def get_market_info(self, market: str = None) -> Dict:
        """Get market information"""
        if market:
            return self.markets.get(market.lower().replace(' ', '_'), {})
        return self.markets
    
    def get_program_info(self, program: str = None) -> Dict:
        """Get government program information"""
        if program:
            return self.govt_programs.get(program.lower(), {})
        return self.govt_programs
    
    def get_challenge_info(self, challenge: str = None) -> Dict:
        """Get challenge solutions"""
        if challenge:
            return self.challenges.get(challenge.lower(), {})
        return self.challenges
    
    def get_zambia_response(self, query: str) -> Optional[str]:
        """Generate response for Zambia-specific queries"""
        query_lower = query.lower()
        responses = []
        
        # Province queries
        province_keywords = ['province', 'region', 'where', 'in zambia']
        for kw in province_keywords:
            if kw in query_lower:
                # Check which crops/livestock are mentioned in query
                for prov, info in self.provinces.items():
                    for item in info['main_crops'] + info['main_livestock']:
                        if item.lower() in query_lower:
                            responses.append(f"**{info['name']}:** Crops: {', '.join(info['main_crops'][:3])} | Livestock: {', '.join(info['main_livestock'][:2])} | Key Town: {info['key_towns'][0]}")
        
        # Market queries
        if 'market' in query_lower or 'sell' in query_lower or 'price' in query_lower:
            responses.append("**Main Markets in Zambia:**")
            for market_key, market_info in self.markets.items():
                responses.append(f"  - {market_info['name']} ({market_info['location']})")
        
        # Season/when queries
        if 'when' in query_lower or 'season' in query_lower or 'plant' in query_lower:
            responses.append("**Key Planting Season:** November-January (rainy season)")
            responses.append("**Harvest:** March-June")
        
        # Government program queries
        if 'program' in query_lower or 'subsidy' in query_lower or 'government' in query_lower or 'support' in query_lower:
            responses.append("**Government Programs:**")
            for prog_key, prog_info in self.govt_programs.items():
                responses.append(f"  - {prog_info['name']}: {prog_info['description'][:60]}...")
        
        # Challenge queries
        if 'problem' in query_lower or 'challenge' in query_lower or 'help' in query_lower or 'drought' in query_lower:
            responses.append("**Common Challenges & Solutions:**")
            for chal_key, chal_info in self.challenges.items():
                responses.append(f"  - {chal_key.title()}: {chal_info['solutions'][0]}")
        
        return "\n\n".join(responses) if responses else None


# Singleton
_zambia_farming = None


def get_zambia_farming() -> ZambiaFarming:
    global _zambia_farming
    if _zambia_farming is None:
        _zambia_farming = ZambiaFarming()
    return _zambia_farming


if __name__ == "__main__":
    # Test the module
    zf = get_zambia_farming()
    
    print("=== Testing Zambia Farming Module ===\n")
    
    # Test province
    print("Southern Province:")
    print(zf.get_province_info('southern'))
    
    print("\n=== Seasonal Calendar (October) ===")
    print(zf.get_season_info('october'))
    
    print("\n=== Market Info ===")
    print(zf.get_market_info('soweto_market'))
    
    print("\n=== Government Programs ===")
    print(zf.get_program_info('frdp'))