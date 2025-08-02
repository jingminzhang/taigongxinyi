# Root Directory Documentation Cleanup Plan

## Current State
- 28 markdown files in root directory
- Makes the project structure hard to navigate
- Mix of different types of documentation

## Organization Strategy

### Keep in Root (Core Project Docs)
- README.md - Main project overview
- CLAUDE.md - AI assistant instructions  
- PROJECT_STRUCTURE.md - High-level architecture

### Move to docs/ (Technical Documentation)
- Anti_Reasoning_Monologue_Solution.md → docs/technical/
- Final_Baxian_Sanqing_Model_Configuration.md → docs/technical/
- Reasoning_Pattern_Detection_And_Filtering.md → docs/technical/
- Sanqing_Baxian_OpenRouter_Model_Assignment.md → docs/technical/
- Xiantian_Bagua_Debate_System_Design.md → docs/technical/
- GAMEFI_SYSTEM_SUMMARY.md → docs/systems/
- Platform_Specific_Avatar_Strategy.md → docs/strategies/

### Move to docs/setup/ (Setup & Deployment)
- CLAUDE_ACTION_SETUP.md → docs/setup/
- doppler-migration-guide.md → docs/setup/
- env_standardization_plan.md → docs/setup/
- github_deployment_plan.md → docs/setup/
- SETUP_WITH_PROXY.md → docs/setup/

### Move to docs/mcp/ (MCP Related)
- MCP_MANAGEMENT_SOLUTION.md → docs/mcp/
- mcp_manager_complete_package.zip.md → docs/mcp/
- mcp_manager_package.tar.md → docs/mcp/
- MCP_Driven_User_Acquisition_Funnel.md → docs/mcp/

### Move to docs/analysis/ (Analysis & Reports)
- rapidapi_mcp_analysis.md → docs/analysis/
- rapidapi_pool_analysis.md → docs/analysis/
- rapidapi_subscription_report.md → docs/analysis/
- MongoDB_to_Milvus_Fix.md → docs/analysis/
- openmanus_integration_strategies.md → docs/analysis/

### Move to docs/internal/ (Internal/Development)
- DEVELOPMENT_LOG.md → docs/internal/
- INTERNAL_NOTES.md → docs/internal/
- TODO_INTERNAL.md → docs/internal/
- file_lifecycle_policy.md → docs/internal/

## Expected Result
- Clean root directory with only 3 essential markdown files
- Well-organized documentation structure
- Easier navigation and maintenance
