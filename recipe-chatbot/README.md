# Recipe Chatbot - AI Evaluations Course

## Quick Start

1. **Clone & Setup**

   ```bash
   git clone https://github.com/Phan-ChiHieu/theory-ai
   cd recipe-chatbot
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configure Environment**

   ```bash
   cp env.example .env
   # Edit .env to add your model and API keys
   ```

3. **Run the Chatbot**
   ```bash
   uvicorn backend.main:app --reload
   # Open http://127.0.0.1:8000
   ```
