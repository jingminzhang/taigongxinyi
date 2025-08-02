# Project Structure

## Directory Organization

```
liurenchaxin/
├── app/                    # Application entry points
│   ├── streamlit_app.py   # Main Streamlit application
│   └── components/        # Reusable UI components
├── src/                   # Core business logic
│   ├── jixia/            # 稷下学宫 AI debate system
│   │   ├── agents/       # AI agent implementations
│   │   ├── debates/      # Debate logic and orchestration
│   │   └── personalities/ # Historical figure personalities
│   ├── database/         # Database connection and models
│   │   ├── postgres/     # PostgreSQL specific code
│   │   ├── mongo/        # MongoDB specific code
│   │   └── zilliz/       # Vector database code
│   └── api/              # External API integrations
│       ├── openrouter/   # OpenRouter API client
│       ├── anthropic/    # Anthropic API client
│       └── openai/       # OpenAI API client
├── config/               # Configuration management
│   ├── doppler_config.py # Doppler integration
│   ├── settings.py       # Application settings
│   └── environments/     # Environment-specific configs
├── tests/                # Test suite
│   ├── unit/            # Unit tests
│   ├── integration/     # Integration tests
│   └── fixtures/        # Test data and fixtures
├── docs/                 # Documentation
│   ├── api/             # API documentation
│   ├── deployment/      # Deployment guides
│   └── development/     # Development guides
├── scripts/              # Utility scripts
│   ├── setup.sh         # Environment setup
│   ├── migrate.py       # Data migration scripts
│   └── deploy.sh        # Deployment scripts
└── .kiro/               # Kiro AI assistant configuration
    ├── specs/           # Feature specifications
    └── steering/        # AI guidance rules
```

## File Naming Conventions

### Python Files
- **snake_case** for all Python files and modules
- **PascalCase** for class names
- **UPPER_CASE** for constants
- Descriptive names that indicate purpose

### Configuration Files
- Use `.py` for Python configuration files
- Use `.yaml` or `.json` for data configuration
- Environment-specific suffixes: `_dev.py`, `_prod.py`

### Documentation
- **README.md** in each major directory explaining its purpose
- **CHANGELOG.md** for tracking changes
- **API.md** for API documentation

## Code Organization Principles

### Separation of Concerns
- **app/**: UI and presentation layer only
- **src/**: Business logic and core functionality
- **config/**: Configuration and settings management
- **tests/**: All testing code isolated

### Module Structure
Each major module should contain:
- `__init__.py`: Module initialization and public API
- `models.py`: Data models and schemas
- `services.py`: Business logic and operations
- `utils.py`: Helper functions and utilities
- `exceptions.py`: Custom exception classes

### Import Organization
```python
# Standard library imports
import os
import sys
from typing import Dict, List

# Third-party imports
import streamlit as st
from sqlalchemy import create_engine

# Local imports
from src.jixia.agents import DebateAgent
from config.settings import get_settings
```

## Security Structure

### Configuration Security
- **No secrets in code**: All sensitive data in Doppler or environment variables
- **Environment separation**: Clear boundaries between dev/staging/prod
- **Access control**: Proper authentication for all external services

### File Security
- **`.gitignore`**: Comprehensive exclusion of sensitive files
- **`.env.example`**: Template for required environment variables
- **Pre-commit hooks**: Automated security scanning before commits

## Documentation Requirements

### Required Documentation
- **README.md**: Project overview and quick start
- **INSTALLATION.md**: Detailed setup instructions
- **API.md**: API endpoints and usage
- **CONTRIBUTING.md**: Development guidelines

### Code Documentation
- **Docstrings**: All public functions and classes must have docstrings
- **Type hints**: Use Python type hints for better code clarity
- **Comments**: Explain complex business logic and AI model interactions

## Migration Guidelines

### Legacy Code Handling
- **Selective migration**: Only migrate proven, working code
- **Clean slate approach**: Rewrite rather than copy-paste when possible
- **Documentation first**: Document before migrating

### Quality Gates
- All migrated code must pass security scans
- All migrated code must have tests
- All migrated code must follow new structure conventions