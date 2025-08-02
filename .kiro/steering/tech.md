# Technology Stack

## Core Technologies
- **Python 3.x**: Primary programming language
- **Streamlit**: Web interface framework for the main application
- **FastAPI**: API framework for backend services (if applicable)

## AI & ML Stack
- **OpenRouter**: Multi-model AI API gateway
- **Anthropic Claude**: Primary AI model for debates
- **OpenAI GPT**: Alternative AI model support
- **Vector Databases**: Zilliz for semantic search and embeddings

## Database Technologies
- **PostgreSQL**: Primary relational database
- **MongoDB**: Document database for flexible data storage
- **Zilliz**: Vector database for AI embeddings and semantic search

## Configuration & Security
- **Doppler**: Centralized secrets and configuration management
- **Environment Variables**: Local configuration override
- **GitGuardian**: Automated secret scanning and security

## Development Tools
- **Git**: Version control
- **Pre-commit Hooks**: Automated code quality and security checks
- **Virtual Environment**: Python dependency isolation

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### Application Commands
```bash
# Start Streamlit application
streamlit run app/streamlit_app.py

# Run with specific port
streamlit run app/streamlit_app.py --server.port 8501
```

### Development Commands
```bash
# Run tests
python -m pytest tests/

# Code quality checks
pre-commit run --all-files

# Security scan
doppler secrets download --no-file --format env > .env.local
```

### Database Commands
```bash
# PostgreSQL connection test
python -c "from src.database import test_postgres_connection; test_postgres_connection()"

# MongoDB connection test  
python -c "from src.database import test_mongo_connection; test_mongo_connection()"
```

## Security Requirements
- **Zero Hardcoded Secrets**: All secrets must come from Doppler or environment variables
- **Environment Isolation**: Development, staging, and production environments must be separate
- **Automated Scanning**: All commits must pass GitGuardian security checks
- **Access Control**: Database and API access through proper authentication only

## Performance Considerations
- **Async Operations**: Use async/await for AI API calls to prevent blocking
- **Connection Pooling**: Implement database connection pooling for better performance
- **Caching**: Cache frequently accessed data and AI responses when appropriate
- **Resource Limits**: Set appropriate timeouts and rate limits for external API calls