# LLM Workflows

## File structure
```
/configs
/tests
/logs
/src
    /memory  # Agent Memory
    /pre_retrieval  # RAG Pre-retrieval Tools 
    /tracing  # Tracing clients
    /util
/workflows
    /chatbot_memory  # Chat Agent with Memory Demo
    /query_transform  # Pre-retrieval Query Transformation Demo
```


## How to run
Note: run with Gemini API, local llm too small to behave correctly. (tested up to 8b)

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

4. Run individual workflow
```
uv run -m workflows/chatbot_memory/main.py
```