# File Structure
```
/
├── .env                  # Environment variables (e.g., API keys, database URLs)
├── .dockerignore         # Files/folders to ignore when building Docker image
├── Dockerfile            # Docker configuration for containerization
├── README.md             # Project description, setup instructions, etc.
├── pyproject.toml        # Project metadata and dependencies
├── uv.lock               # uv lockfile
├── setup.py              # For packaging and distributing your application (if applicable)
│
├── app/                  # Main application source code
│   ├── __init__.py       # Makes 'app' a Python package
│   ├── main.py           # Entry point of the application (e.g., FastAPI app instance)
│   │
│   ├── api/              # REST API endpoints (if your app has a web interface)
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent_routes.py    # Endpoints for interacting with agents
│   │   │   │   ├── memory_routes.py   # Endpoints for memory management
│   │   │   │   └── ...
│   │   │   ├── schemas/         # Pydantic models for request/response validation
│   │   │   │   ├── __init__.py
│   │   │   │   ├── agent_schemas.py
│   │   │   │   └── ...
│   │
│   ├── core/             # Core application logic and utilities
│   │   ├── __init__.py
│   │   ├── config.py     # Configuration management (loading .env, default settings)
│   │   ├── exceptions.py # Custom exceptions
│   │   ├── logging.py    # Logging configuration
│   │   └── utils.py      # Common utility functions
│   │
│   ├── services/         # Business logic and interactions with external libraries/APIs
│   │   ├── __init__.py
│   │   ├── agent_service.py    # Orchestrates OpenAI Agent SDK interactions, Sgland
│   │   ├── memory_service.py   # Manages Mem0 interactions
│   │   ├── mcp_service.py      # Manages FastMCP interactions
│   │   └── ...
│   │
│   ├── agents/           # Agent-specific definitions and logic (using OpenAI Agent SDK)
│   │   ├── __init__.py
│   │   ├── my_specific_agent.py # Definition of a specific agent, its tools, capabilities
│   │   ├── another_agent.py
│   │   └── tools/              # Custom tools for your agents
│   │       ├── __init__.py
│   │       ├── custom_tool_1.py
│   │       └── ...
│   │
│   ├── memory/           # Memory management specific files (Mem0 integration)
│   │   ├── __init__.py
│   │   ├── mem0_client.py      # Wrapper/client for Mem0
│   │   ├── schemas.py          # Pydantic schemas for memory structures (if custom)
│   │   └── ...
│   │
│   ├── mcp/              # FastMCP specific files
│   │   ├── __init__.py
│   │   ├── mcp_interface.py    # Interface for FastMCP (e.g., for multi-party comms)
│   │   └── ...
│   │
│   ├── sgland/           # Sgland specific files (for robust agent interaction, state management)
│   │   ├── __init__.py
│   │   ├── sgland_manager.py   # Manages Sgland sessions/state
│   │   ├── state_models.py     # Pydantic models for agent state managed by Sgland
│   │   └── ...
│   │
│   ├── db/               # Database related files (if you have a persistent DB)
│   │   ├── __init__.py
│   │   ├── database.py   # Database connection, session management
│   │   ├── models.py     # SQLAlchemy/Tortoise ORM models
│   │   ├── crud.py       # Create, Read, Update, Delete operations
│   │   └── alembic/      # For database migrations (if using Alembic)
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │           ├── __init__.py
│   │           ├── <timestamp>_initial_migration.py
│   │           └── ...
│   │
│   └── tests/            # Unit and integration tests
│       ├── __init__.py
│       ├── unit/
│       │   ├── __init__.py
│       │   ├── test_agent_service.py
│       │   ├── test_memory_service.py
│       │   └── ...
│       ├── integration/
│       │   ├── __init__.py
│       │   ├── test_api_endpoints.py
│       │   └── ...
│       └── conftest.py   # Pytest fixtures
│
├── scripts/              # Helper scripts (e.g., database seeding, setup, deployment)
│   ├── run_agent.py
│   ├── setup_db.py
│   ├── dev_setup.sh      # Example: script to setup dev environment with uv
│   └── ...
│
└── config/               # Non-code configuration files (e.g., for logging, special agents)
    ├── logging.ini
    ├── agent_profiles.json # Example: different configurations for various agents
    └── ...
```