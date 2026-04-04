"""
Services Package
External AI and data services for the Livestock AI Assistant
"""

from .external_ai_service import (
    ExternalAIService,
    FallbackResponseGenerator,
    get_ai_service,
    get_fallback_generator
)

from .data_service import (
    WeatherService,
    MarketPriceService,
    DiseaseAlertService,
    get_weather_service,
    get_market_service,
    get_disease_service
)

from .knowledge_base import (
    KnowledgeBase,
    get_knowledge_base
)

from .zambia_farming import (
    ZambiaFarming,
    get_zambia_farming
)

__all__ = [
    # External AI
    'ExternalAIService',
    'FallbackResponseGenerator', 
    'get_ai_service',
    'get_fallback_generator',
    # Data Services
    'WeatherService',
    'MarketPriceService',
    'DiseaseAlertService',
    'get_weather_service',
    'get_market_service',
    'get_disease_service',
    # Knowledge Base
    'KnowledgeBase',
    'get_knowledge_base',
    # Zambia
    'ZambiaFarming',
    'get_zambia_farming'
]
