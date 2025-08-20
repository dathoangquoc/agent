Note: run with Gemini API, local llm too small to behave correctly. (tested up to 8b)

# How to run
1. Set your .env
```.env
MODEL=gemini/gemini-2.0-flash-lite
API_KEY=your-api-key-here
```

2. Start Qdrant DB
```
sudo bash scripts/start.sh
```

3. Change user_id in main.py to simulate different users

4. Run main
```
uv run main.py
```