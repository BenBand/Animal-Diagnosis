"""
Real-Time Data Service Module
Fetches live weather, market prices, and other external data
"""
import os
import json
import requests
from typing import Optional, Dict, Any, List
from datetime import datetime
from config import OPENWEATHERMAP_API_KEY


class WeatherService:
    """
    Fetches weather data for farm planning
    Uses OpenWeatherMap API (free tier available)
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or OPENWEATHERMAP_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_current_weather(self, location: str = None, lat: float = None, lon: float = None) -> Optional[Dict]:
        """
        Get current weather for location
        
        Args:
            location: City name (e.g., "Lusaka,ZM")
            lat: Latitude
            lon: Longitude
            
        Returns:
            Weather data dict or None
        """
        if not self.is_available():
            return None
        
        try:
            params = {'appid': self.api_key, 'units': 'metric'}
            
            if location:
                params['q'] = location
            elif lat and lon:
                params['lat'] = lat
                params['lon'] = lon
            else:
                return None
            
            response = requests.get(f"{self.base_url}/weather", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_weather(data)
            return None
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None
    
    def get_forecast(self, location: str = None, lat: float = None, lon: float = None, days: int = 5) -> Optional[List[Dict]]:
        """Get weather forecast"""
        if not self.is_available():
            return None
        
        try:
            params = {'appid': self.api_key, 'units': 'metric', 'cnt': days * 8}
            
            if location:
                params['q'] = location
            elif lat and lon:
                params['lat'] = lat
                params['lon'] = lon
            else:
                return None
            
            response = requests.get(f"{self.base_url}/forecast", params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._format_forecast(data)
            return None
        except Exception as e:
            print(f"Weather Forecast Error: {e}")
            return None
    
    def _format_weather(self, data: Dict) -> Dict:
        """Format weather data for response"""
        return {
            'location': data.get('name', 'Unknown'),
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'icon': data['weather'][0]['icon'],
            'wind_speed': data['wind'].get('speed', 0),
            'timestamp': datetime.now().isoformat()
        }
    
    def _format_forecast(self, data: Dict) -> List[Dict]:
        """Format forecast data"""
        forecasts = []
        for item in data['list']:
            forecasts.append({
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            })
        return forecasts
    
    def get_farming_advice(self, weather_data: Dict) -> str:
        """Generate farming advice based on weather"""
        if not weather_data:
            return "Weather data unavailable. Please check local forecasts."
        
        temp = weather_data.get('temperature', 0)
        humidity = weather_data.get('humidity', 0)
        description = weather_data.get('description', '').lower()
        
        advice_parts = []
        
        # Temperature-based advice
        if temp > 35:
            advice_parts.append("⚠️ High temperature alert! Ensure animals have ample shade and clean water. Consider misting systems for cooling.")
        elif temp > 30:
            advice_parts.append("🌡️ Warm weather: Increase water availability and provide shaded areas. Monitor for heat stress signs.")
        elif temp < 5:
            advice_parts.append("❄️ Cold weather: Ensure livestock has warm shelter and dry bedding. Increase feed for energy.")
        
        # Humidity advice
        if humidity > 80:
            advice_parts.append("💧 High humidity may increase disease risk. Ensure proper ventilation in housing.")
        
        # Rain-based advice
        if 'rain' in description:
            advice_parts.append("🌧️ Rain expected: Check drainage in pens. Move animals to shelter if needed.")
        elif 'clear' in description or 'sun' in description:
            advice_parts.append("☀️ Good weather for drying hay and outdoor activities.")
        
        return " | ".join(advice_parts) if advice_parts else "Normal weather conditions. Continue regular farming activities."


class MarketPriceService:
    """
    Fetches market prices for livestock and produce
    Note: Real implementation would connect to actual market APIs
    For now, provides structured placeholder with guidance
    """
    
    def __init__(self):
        # In production, these would be real API endpoints
        self.mock_data = self._init_mock_data()
    
    def _init_mock_data(self) -> Dict:
        """Initialize sample market data with Zambian prices (in ZMW)"""
        return {
            # Live cattle prices (ZMW per kg)
            'cattle': {
                'beef_per_kg': 45.00,  # ZMW
                'live_weight_per_kg': 28.00,
                'milk_per_liter': 8.00,
                'weaner_6months': 3500.00,  # ZMW per head
                'cow_milking': 8000.00,
                'bull_breeding': 12000.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            # Poultry prices
            'poultry': {
                'broiler_per_kg': 35.00,
                'layer_per_bird': 120.00,
                'eggs_per_tray': 45.00,  # 30 eggs
                'eggs_per_dozen': 18.00,
                'day_old_chicks': 12.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            # Small ruminants
            'sheep': {
                'live_weight_per_kg': 40.00,
                'mutton_per_kg': 55.00,
                'lamb_per_head': 2500.00,
                'ewe_breeding': 3000.00,
                'ram': 4500.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            'goats': {
                'live_weight_per_kg': 42.00,
                'chevon_per_kg': 60.00,
                'kid_per_head': 800.00,
                'doe_breeding': 1500.00,
                'buck': 2500.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            # Feed prices (ZMW per 50kg bag)
            'feed': {
                'maize_brand': 350.00,
                'soybean_meal': 450.00,
                'concentrate_layer': 520.00,
                'concentrate_broiler': 580.00,
                'salt_lick': 45.00,
                'premix_vitamin': 180.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            # Crop seeds (ZMW per kg)
            'seeds': {
                'maize_white': 25.00,
                'maize_yellow': 28.00,
                'soybean': 35.00,
                'groundnut': 40.00,
                'bean': 30.00,
                'sunflower': 32.00,
                'wheat': 22.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            },
            # Fertilizer (ZMW per 50kg)
            'fertilizer': {
                'urea': 450.00,
                'dap': 520.00,
                'compound_l': 380.00,
                'compound_d': 400.00,
                'lime': 150.00,
                'currency': 'ZMW',
                'last_updated': datetime.now().isoformat()
            }
        }
    
    def get_prices(self, category: str = None) -> Dict:
        """Get market prices"""
        if category:
            return self.mock_data.get(category, {})
        return self.mock_data
    
    def get_price_summary(self) -> str:
        """Get formatted price summary"""
        lines = ["📊 Current Market Prices (Sample):", ""]
        
        for category, prices in self.mock_data.items():
            lines.append(f"**{category.upper()}:**")
            for item, price in prices.items():
                if item != 'last_updated':
                    if item == 'currency':
                        continue
                    unit = 'per kg' if 'per_kg' in item else 'per liter' if 'per_liter' in item else 'per dozen' if 'per_dozen' in item else 'per bale'
                    lines.append(f"  • {item.replace('_', ' ').title()}: ${price} {unit}")
            lines.append("")
        
        lines.append(f"_Last updated: {self.mock_data['cattle']['last_updated']}_")
        lines.append("_Note: Prices vary by region. Contact local markets for accurate quotes._")
        
        return "\n".join(lines)


class DiseaseAlertService:
    """
    Fetches disease alerts from veterinary databases
    Provides information on common livestock diseases
    """
    
    def __init__(self):
        self.disease_database = self._init_disease_database()
    
    def _init_disease_database(self) -> Dict:
        """Initialize common livestock diseases database"""
        return {
            'foot_and_mouth': {
                'species': ['cattle', 'sheep', 'goats', 'pigs'],
                'symptoms': ['blisters on mouth and feet', 'limping', 'drooling', 'fever'],
                'severity': 'High',
                'transmission': 'Direct contact, contaminated equipment',
                'prevention': 'Vaccination, quarantine new animals, disinfect equipment'
            },
            'bovine_tuberculosis': {
                'species': ['cattle'],
                'symptoms': ['weight loss', 'coughing', 'enlarged lymph nodes', 'weakness'],
                'severity': 'High (zoonotic)',
                'transmission': 'Airborne, contaminated milk',
                'prevention': 'Testing and culling, pasteurize milk'
            },
            'mastitis': {
                'species': ['cattle', 'goats', 'sheep'],
                'symptoms': ['swollen udder', 'abnormal milk', 'fever', 'loss of appetite'],
                'severity': 'Medium-High',
                'transmission': 'Bacterial infection through teat canal',
                'prevention': 'Clean milking equipment, proper milking hygiene, dry cow therapy'
            },
            'newcastle_disease': {
                'species': ['poultry'],
                'symptoms': ['respiratory distress', 'green diarrhea', 'twisted neck', 'sudden death'],
                'severity': 'High',
                'transmission': 'Direct contact, contaminated feed, equipment',
                'prevention': 'Vaccination, biosecurity measures'
            },
            'anthrax': {
                'species': ['cattle', 'sheep', 'goats'],
                'symptoms': ['sudden death', 'blood from orifices', 'no signs of struggle'],
                'severity': 'High (zoonotic)',
                'transmission': 'Spores in soil, contaminated feed',
                'prevention': 'Annual vaccination, do not open carcass'
            },
            # Add more common livestock diseases
            'lumpy_skin': {
                'species': ['cattle'],
                'symptoms': ['skin nodules', 'fever', 'swollen lymph nodes', 'lethargy'],
                'severity': 'Medium-High',
                'transmission': 'Mosquitoes, ticks, direct contact',
                'prevention': 'Vaccination, control insects, isolate affected animals'
            },
            'blue_tongue': {
                'species': ['sheep', 'cattle', 'goats'],
                'symptoms': ['fever', 'swollen face', 'bluish tongue', 'lameness'],
                'severity': 'Medium',
                'transmission': 'Midges (Culicoides)',
                'prevention': 'Vaccination, control midges, move animals to high ground'
            },
            'fmd': {  # Foot and Mouth shorthand
                'species': ['cattle', 'sheep', 'goats', 'pigs'],
                'symptoms': ['blisters on mouth and feet', 'limping', 'drooling', 'fever'],
                'severity': 'High',
                'transmission': 'Direct contact, contaminated equipment, animals',
                'prevention': 'Vaccination, quarantine, disinfect, report to vet'
            },
            'peste_des_petits_ruminants': {
                'species': ['sheep', 'goats'],
                'symptoms': ['fever', 'diarrhea', 'pneumonia', 'mouth sores'],
                'severity': 'High',
                'transmission': 'Direct contact, respiratory droplets',
                'prevention': 'Vaccination, isolation, biosecurity'
            }
        }
    
    def get_disease_info(self, disease_name: str = None) -> Dict:
        """Get disease information"""
        if disease_name:
            return self.disease_database.get(disease_name.lower().replace(' ', '_'), {})
        return self.disease_database
    
    def search_by_symptoms(self, symptoms: List[str]) -> List[Dict]:
        """Search diseases by symptoms"""
        results = []
        for disease, info in self.disease_database.items():
            disease_symptoms = [s.lower() for s in info['symptoms']]
            match_count = sum(1 for s in symptoms if any(s.lower() in ds for ds in disease_symptoms))
            if match_count > 0:
                results.append({
                    'disease': disease,
                    'match_score': match_count,
                    **info
                })
        
        return sorted(results, key=lambda x: x['match_score'], reverse=True)
    
    def get_prevention_summary(self) -> str:
        """Get general prevention tips"""
        return """
🐄 **General Livestock Health Tips:**

1. **Biosecurity**
   - Limit farm access to essential personnel
   - Disinfect boots and equipment
   - Quarantine new animals for 2-4 weeks

2. **Vaccination**
   - Follow local veterinary recommendations
   - Keep vaccination records
   - Maintain cold chain for vaccines

3. **Nutrition**
   - Provide clean, fresh water always
   - Ensure balanced feed
   - Check feed for mold/contamination

4. **Early Detection**
   - Observe animals daily for behavior changes
   - Check appetite and water intake
   - Monitor milk production (dairy)

5. **Veterinary Care**
   - Establish relationship with local vet
   - Have emergency contact numbers ready
   - Don't delay treatment when animals show signs of illness
"""


# Service instances
_weather_service = None
_market_service = None
_disease_service = None


def get_weather_service(api_key: str = None) -> WeatherService:
    global _weather_service
    if _weather_service is None:
        _weather_service = WeatherService(api_key)
    return _weather_service


def get_market_service() -> MarketPriceService:
    global _market_service
    if _market_service is None:
        _market_service = MarketPriceService()
    return _market_service


def get_disease_service() -> DiseaseAlertService:
    global _disease_service
    if _disease_service is None:
        _disease_service = DiseaseAlertService()
    return _disease_service


if __name__ == "__main__":
    # Test services
    weather = get_weather_service()
    print("Weather service available:", weather.is_available())
    
    market = get_market_service()
    print(market.get_price_summary())
    
    disease = get_disease_service()
    print(disease.get_prevention_summary())
