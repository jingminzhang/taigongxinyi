# Python Files Cleanup Plan

## Current State
- 25 Python files in root directory
- Mix of core applications, tools, examples, and utilities
- Makes project navigation difficult

## Organization Strategy

### Keep in Root (Core Applications)
- app.py - Core application entry point

### Move to scripts/ (Startup & Deployment Scripts)
- deploy_to_production.py → scripts/deploy/
- start_graphrag.py → scripts/
- start_mcp_manager.py → scripts/
- start_services.py → scripts/
- update_env_config.py → scripts/
- test_n8n_integration.py → scripts/
- debug_api.py → scripts/debug/

### Move to examples/ (Analysis & Research Tools)
- company_transcript_analyzer.py → examples/research/
- earnings_transcript_research.py → examples/research/
- interactive_transcript_analyzer.py → examples/research/
- simple_transcript_test.py → examples/research/
- tesla_earnings_call.py → examples/research/
- seekingalpha_playwright_scraper.py → examples/research/
- yahoo_matrix_demo.py → examples/research/

### Move to tools/ (API & Utility Tools)
- rapidapi_checker.py → tools/
- rapidapi_demo.py → tools/
- rapidapi_detailed_explorer.py → tools/
- rapidapi_perpetual_machine.py → tools/
- rapidapi_subscription_scanner.py → tools/

### Move to src/ (Core Engines & Systems)
- jixia_perpetual_engine.py → src/engines/
- mongodb_graphrag.py → src/engines/
- mcp_manager.py → src/managers/
- smart_api_scheduler.py → src/schedulers/
- taigong_n8n_integration.py → src/integrations/

## Expected Result
- Clean root directory with only 1 main Python file
- Well-organized code structure by functionality
- Easier maintenance and development
