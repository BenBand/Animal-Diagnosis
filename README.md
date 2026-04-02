# Livestock AI Assistant 🐄🐔🐐

An AI-powered chatbot for farmers and livestock owners that provides real-time, dynamic responses about cattle, poultry, sheep, goats, and general farming practices.

## Features

- **Hybrid Response System**: Combines local ML model with external AI and real-time data
- **Real-time Weather**: Weather-based farming advice
- **Market Prices**: Current livestock and feed prices
- **Disease Database**: Common livestock diseases with symptoms and prevention tips
- **Knowledge Base**: Structured agricultural information
- **External AI Integration**: OpenAI GPT or HuggingFace LLM for detailed answers

## Installation

### 1. Create Virtual Environment
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install torch requests
```

### 3. Download NLTK Data
```bash
python
>>> import nltk
>>> nltk.download('punkt')
```

## Configuration

### API Keys (Optional but Recommended)

1. **Copy the env file:**
```bash
copy .env.example .env
```

2. **Edit `.env`** and add your API keys:

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| OpenAI | $5 credit | https://platform.openai.com/api-keys |
| HuggingFace | Yes | https://huggingface.co/settings/tokens |
| OpenWeatherMap | Yes | https://openweathermap.org/api |

- Leave keys blank if not using that service
- At least ONE AI provider recommended for full functionality

## Usage

### Option 1: Web Interface
```bash
python app.py
```
Then open http://localhost:5000 in your browser

### Option 2: Console Chat
```bash
python -c "from chat import get_response; print(get_response('What do cows eat?'))"
```

### Train the Model
```bash
python train.py
```
This will retrain the model with the updated intents in `intents.json`

## Project Structure

```
animal_ai/
├── app.py              # Flask web app
├── chat.py             # Hybrid response system
├── model.py            # Neural network model
├── train.py            # Training script
├── nltk_utils.py       # NLP utilities
├── intents.json        # Expanded intents (30+ topics)
├── config.py           # Configuration loader
├── .env                # API keys (create from .env.example)
├── services/           # External services
│   ├── external_ai_service.py   # OpenAI/HuggingFace
│   ├── data_service.py           # Weather, market, disease
│   └── knowledge_base.py         # Agricultural knowledge
└── static/             # Frontend assets
```

## Supported Topics

- Cattle (dairy, beef, breeding)
- Poultry (chickens, eggs, diseases)
- Sheep & Goat farming
- Animal nutrition & feeding
- Disease detection & prevention
- Weather & climate advice
- Market prices & costs
- Housing & facilities
- Pasture management
- Breeding & reproduction

## API Endpoints (Web App)

- `GET /` - Web interface
- `POST /predict` - Chat endpoint
- `GET /api/health` - Health check
- `GET /api/topics` - Available topics

## License

MIT
