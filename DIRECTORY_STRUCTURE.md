# ShellSense Directory Structure

```
shellsense/
├── docs/                          # Documentation
│   ├── api/                       # API documentation
│   ├── guides/                    # User and developer guides
│   ├── examples/                  # Example use cases
│   └── images/                    # Documentation images
│
├── shellsense/                    # Main package directory
│   ├── core/                      # Core functionality
│   │   ├── __init__.py
│   │   ├── plugin.py             # Plugin initialization and management
│   │   ├── session.py            # Session management
│   │   └── events.py             # Event handling system
│   │
│   ├── ai/                       # AI-related modules
│   │   ├── __init__.py
│   │   ├── providers/            # AI providers (moved from root)
│   │   ├── prompts/              # AI prompts (moved from root)
│   │   └── models/               # AI model configurations
│   │
│   ├── tools/                    # Tools directory (enhanced)
│   │   ├── __init__.py
│   │   ├── base.py              # Base tool class
│   │   ├── manager.py           # Tool management
│   │   ├── shell/               # Shell-related tools
│   │   ├── web/                 # Web-related tools
│   │   ├── data/                # Data processing tools
│   │   ├── media/               # Media handling tools
│   │   └── language/            # Language processing tools
│   │
│   ├── shell/                   # Shell integration (enhanced zsh)
│   │   ├── __init__.py
│   │   ├── zsh/                 # Zsh specific
│   │   ├── bash/                # Future bash support
│   │   └── fish/                # Future fish support
│   │
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── profiles/            # User profiles
│   │
│   └── utils/                   # Utility modules
│       ├── __init__.py
│       ├── logging.py           # Enhanced logging
│       ├── security.py          # Security utilities
│       └── helpers.py           # Common helpers
│
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests
│   ├── integration/             # Integration tests
│   └── fixtures/                # Test fixtures
│
├── scripts/                     # Utility scripts
│   ├── install.sh              # Installation script
│   ├── update.sh               # Update script
│   └── tools/                  # Development tools
│
├── examples/                    # Example scripts and configs
│   ├── custom_tools/           # Custom tool examples
│   └── configurations/         # Configuration examples
│
├── .github/                    # GitHub specific files
│   ├── workflows/              # GitHub Actions
│   └── ISSUE_TEMPLATE/         # Issue templates
│
├── pyproject.toml             # Modern Python project configuration
├── setup.cfg                  # Setup configuration
├── setup.py                   # Setup script
├── requirements/
│   ├── base.txt              # Base requirements
│   ├── dev.txt               # Development requirements
│   └── test.txt             # Test requirements
│
├── Makefile                  # Build and development commands
├── CHANGELOG.md             # Version history
├── CONTRIBUTING.md          # Contribution guidelines
├── LICENSE                  # License file
└── README.md               # Project documentation
```

## Key Improvements

1. **Modular Core Structure**
   - Separated core functionality into its own directory
   - Better separation of concerns with plugin, session, and event handling

2. **Enhanced AI Integration**
   - Dedicated AI directory for better organization
   - Separated providers, prompts, and model configurations

3. **Organized Tools**
   - Categorized tools by functionality
   - Better structure for adding new tools
   - Clearer separation of concerns

4. **Shell Support**
   - Structured for multi-shell support
   - Better organization of shell-specific code

5. **Modern Python Project Structure**
   - Added pyproject.toml for modern Python packaging
   - Separated requirements by purpose
   - Better development tooling

6. **Improved Documentation**
   - Dedicated docs directory
   - Better organized examples
   - Clear contribution guidelines

7. **Testing Infrastructure**
   - Separated unit and integration tests
   - Added test fixtures directory
   - Better test organization

8. **Development Tools**
   - Added utility scripts
   - Makefile for common commands
   - Better development workflow

## Benefits

1. **Scalability**
   - Easy to add new shells
   - Simple tool addition process
   - Clear upgrade path

2. **Maintainability**
   - Clear separation of concerns
   - Well-organized code
   - Easy to find and fix issues

3. **Extensibility**
   - Easy to add new features
   - Clear plugin architecture
   - Simple integration points

4. **Developer Experience**
   - Better documentation
   - Clear development process
   - Easy to contribute

5. **Testing**
   - Comprehensive test coverage
   - Easy to add new tests
   - Clear test organization

6. **Security**
   - Better security organization
   - Clear security boundaries
   - Easy to audit
