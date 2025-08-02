# Documentation Restructure Plan

## 🎯 Goal
Reorganize docs/ for GitHub Pages to help potential collaborators quickly understand and join the project, while keeping internal docs in internal/.

## 📋 Current Issues
- Too many technical documents in public docs/
- Complex structure overwhelming for newcomers  
- Missing clear project vision presentation
- Three-tier system (炼妖壶/降魔杵/打神鞭) not clearly presented

## 🏗️ New Public Docs Structure

### Root Level (Welcome & Quick Start)
```
docs/
├── index.md                    # Project overview & three-tier vision
├── README.md                   # Quick start guide
├── CONTRIBUTING.md             # How to contribute
└── roadmap.md                  # Development roadmap
```

### Core Sections
```
├── getting-started/            # New contributor onboarding
│   ├── quick-start.md         # 5-minute setup
│   ├── architecture-overview.md # High-level architecture
│   └── first-contribution.md  # How to make first contribution
├── vision/                     # Project vision & philosophy
│   ├── three-tiers.md         # 炼妖壶/降魔杵/打神鞭 system
│   ├── manifesto.md           # Project manifesto
│   └── why-anti-gods.md       # Philosophy behind the project
├── features/                   # What the system can do
│   ├── ai-debate-system.md    # Jixia Academy features
│   ├── financial-analysis.md  # Market analysis capabilities
│   └── mcp-integration.md     # MCP service features
└── api/                       # API documentation
    ├── endpoints.md           # API reference
    └── examples.md            # Usage examples
```

## 📦 Move to Internal (Not for GitHub Pages)

### Development & Internal Docs → docs/internal/
- Technical implementation details
- Internal development logs
- Private strategy documents
- Detailed configuration guides
- Debug and troubleshooting docs
- Internal analysis reports

### Files to Move to internal/
```
technical/ → internal/technical/
setup/ → internal/setup/
mcp/ → internal/mcp/
analysis/ (some files) → internal/analysis/
strategies/ → internal/strategies/
```

## 🎯 Key Public Documentation Goals

### 1. Clear Project Vision
- Highlight the three-tier system prominently
- Explain the grand vision without overwhelming details
- Show progression path: 炼妖壶 → 降魔杵 → 打神鞭

### 2. Easy Onboarding
- 5-minute quick start guide
- Clear setup instructions
- Simple first contribution guide

### 3. Showcase Innovation
- AI debate system (Jixia Academy)
- Multi-agent financial analysis
- MCP integration architecture
- Mathematical foundations (accessible version)

### 4. Community Building
- Contributing guidelines
- Code of conduct
- Communication channels
- Recognition system

## 🚀 Implementation Plan

1. **Create new structure** - Set up clean public docs organization
2. **Move internal docs** - Transfer non-public docs to internal/
3. **Write newcomer docs** - Create accessible onboarding materials
4. **Highlight vision** - Emphasize three-tier system and grand vision
5. **Add community docs** - Contributing guidelines and community info
