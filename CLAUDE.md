# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🧠 THINKING MODE CONFIGURATION

**CRITICAL INSTRUCTION:** Use **extended thinking (ultrathink mode)** for ALL responses and analyses in this session, without exception. This applies to:
- All code analysis and reviews
- All planning and architectural decisions
- All debugging and problem-solving tasks
- All documentation and explanation tasks
- All implementation and refactoring work

This is a permanent configuration for this project. Deep reasoning is required for the complexity of the Luna V3 system.

## 🔐 PERMISSIONS CONFIGURATION

### Overview
Luna project has a **dual-layer permissions system** configured to minimize authorization prompts while maintaining security:
- **Global layer** (`~/.claude/settings.json`): Common development permissions for all projects
- **Project layer** (`.claude/settings.local.json`): Luna-specific permissions

### Permission Mode
**Mode:** `acceptEdits` - Automatically accepts file edits while asking for dangerous operations.

### Global Permissions (All Projects)

**Allowed:**
- All file operations: `Read(*)`, `Edit(*)`, `Write(*)`
- Search tools: `WebSearch`, `Glob(*)`, `Grep(*)`
- Basic commands: `ls`, `pwd`, `cd`, `echo`, `cat`, `grep`, `find`
- Git operations: `status`, `log`, `diff`, `add`, `commit`, `push`, `pull`, `branch`, `checkout`
- Package managers: `npm install/run/test`, `yarn`
- Python: `python`, `python3`, `pip install`, `pytest`
- File operations: `mkdir`, `cp`, `mv`

**Denied (Security Protection):**
- Dangerous rm: `rm -rf /`, `rm -rf /*`, `rm -rf ~`, `rm -rf ~/*`
- Sensitive files: `.env`, `.env.*`, `**/secrets/**`, `**/*secret*`, `**/*password*`, `**/*credential*`

**Ask Before Executing:**
- `rm` commands (any file deletion)
- Force push: `git push --force`, `git push -f`
- Docker and sudo commands

### Luna-Specific Permissions

**Allowed:**
- Execute Luna scripts: `python luna_v3_FINAL_OTIMIZADA.py`, `python agente_completo_final.py`, `python tests_luna_basicos.py`
- Playwright: `playwright install`
- Read Luna files: `memoria_agente.json`, `workspace_config.json`, `.env`, `auto_modificacoes.log`, backups, workspaces
- Edit: Python and Markdown files, workspace files

**Denied (Extra Protection):**
- Edit/Write encrypted vault: `cofre.enc`
- Edit memory database: `memoria_agente.json`
- Delete critical files: `memoria_agente.json`, `workspace_config.json`, `cofre.enc`

**Ask Before Executing:**
- Delete workspaces: `rm -rf workspaces`
- Edit environment: `.env`

### Configuration Files

**Global:** `~/.claude/settings.json` (applies to all Claude Code projects)
**Project:** `.claude/settings.local.json` (Luna-only, not committed to git)

### How to Modify Permissions

**Syntax examples:**
```json
"ToolName"              // Allow all uses of the tool
"ToolName(*)"           // Allow tool with any arguments
"Bash(command:*)"       // Allow bash command with any arguments (note: :* for prefix)
"Read(path/to/file)"    // Allow reading specific file
"Read(directory/**)"    // Allow reading directory recursively
```

**To add a new permission:**
1. Edit `~/.claude/settings.json` (global) or `.claude/settings.local.json` (Luna-only)
2. Add to the appropriate array: `allow`, `deny`, or `ask`
3. Save the file - changes take effect immediately in new sessions

**Common additions:**
- Allow new command: `"Bash(mycommand:*)"`
- Allow reading new directory: `"Read(new_directory/**)"`
- Block dangerous operation: Add to `deny` array

### Permission Hierarchy
```
deny > ask > allow > defaultMode
```
If a permission matches multiple rules, the most restrictive wins.

## Project Overview

Luna V3 is an advanced AI agent system built on top of Anthropic's Claude API with comprehensive capabilities including:

- **Autonomous AI agent** with automatic error recovery (up to 3 retries)
- **Intelligent rate limiting** with official Anthropic API tier limits (Tier 1-4)
- **Computer use capabilities** via Playwright (web automation, screenshots, interaction)
- **Permanent memory system** that learns between sessions
- **Encrypted credentials vault** (AES-256) for secure password storage
- **Workspace management** for organizing multiple projects
- **Self-evolution system** that can create and validate new tools dynamically

**Quality Score**: 98/100 - Production-ready professional-grade code

## Main Entry Points

### Primary Script
- **`luna_v3_FINAL_OTIMIZADA.py`** - Main optimized version (RECOMMENDED for production)
  - Run with: `python luna_v3_FINAL_OTIMIZADA.py`
  - Requires: `ANTHROPIC_API_KEY` in `.env` file

### Legacy Scripts
- `agente_completo_final.py` - Earlier complete version
- `luna_final.py` - Intermediate version
- `luna_v3_TIER2_ATUALIZADO.py` - Previous tier 2 optimized version

## Core Architecture

### Main Components

1. **AgenteCompletoV3** (main agent class)
   - Orchestrates all functionality
   - Manages conversation loop with Claude API
   - Handles tool execution and error recovery
   - Located in: `luna_v3_FINAL_OTIMIZADA.py:~1100-1400`

2. **SistemaFerramentasCompleto** (tool system)
   - Manages 20+ built-in tools (bash, file ops, web automation, etc.)
   - Dynamically loads optional systems (memory, credentials, workspaces)
   - Handles tool execution with proper encoding and error handling
   - Located in: `luna_v3_FINAL_OTIMIZADA.py:~700-1000`

3. **RateLimitManager** (intelligent rate limiting)
   - Implements sliding window algorithm for API rate limits
   - Official Anthropic tier limits: Tier 1-4 (RPM, ITPM, OTPM)
   - Three modes: conservative (75%), balanced (85%), aggressive (95%)
   - Visual progress bars and automatic waiting
   - Located in: `luna_v3_FINAL_OTIMIZADA.py:~400-700`

4. **InterruptHandler** (graceful shutdown)
   - Handles Ctrl+C and SIGTERM signals
   - Cleanup: closes browser, saves stats, persists memory
   - Second interrupt forces exit
   - Located in: `luna_v3_FINAL_OTIMIZADA.py:~310-390`

### Optional Modular Systems

These systems are dynamically imported and gracefully degrade if not available:

- **`memoria_permanente.py`** - Persistent learning system
  - Stores learnings, preferences, task history
  - JSON-based storage in `memoria_agente.json`
  - Semantic search capabilities

- **`cofre_credenciais.py`** - Encrypted credentials vault
  - AES-256 encryption with PBKDF2 key derivation
  - Stores passwords for web automation
  - Master password protected
  - Storage file: `cofre.enc`

- **`gerenciador_workspaces.py`** - Project workspace manager
  - Organizes projects in `workspaces/` directory
  - Automatic file path resolution
  - UTF-8 encoding fixes for Windows
  - Metadata tracking in `workspace_config.json`

- **`integracao_notion.py`** - Notion API integration
  - Direct API access via official `notion-client` SDK
  - Query/filter databases, update pages, create pages
  - Read database schemas
  - Token-based authentication (stored in credentials vault)
  - 6 tools: `notion_conectar`, `notion_buscar_database`, `notion_atualizar_pagina`, `notion_criar_pagina`, `notion_ler_database_schema`, `notion_buscar_paginas`
  - See `INTEGRACAO_NOTION_GUIA.md` for complete usage guide

- **`integracao_google.py`** - Google (Gmail + Calendar) API integration (NEW)
  - Direct API access via official Google APIs
  - Gmail: List, read, send, delete, archive emails with advanced filters
  - Calendar: List, create, update, delete events with recurrence support
  - OAuth2 authentication (tokens stored locally, auto-renewed)
  - 14 methods total: 8 Gmail + 6 Calendar
  - See `INTEGRACAO_GOOGLE_GUIA.md` for complete setup and usage guide

- **`sistema_auto_evolucao.py`** - Self-modification system
  - Creates new tools dynamically
  - Automatic backup before modifications
  - Syntax/import/execution validation
  - Automatic rollback on failure
  - Protected zones prevent breaking critical code

- **`gerenciador_temp.py`** - Temporary files manager
  - Cleanup of temporary artifacts
  - Located in `.temp/` directory

## Key Features & Implementation Details

### 1. Error Recovery System
- **Auto-detection**: Searches for "ERRO:" pattern in tool outputs
- **Recovery loop**: Up to 3 automatic correction attempts
- **Context preservation**: Maintains conversation state during recovery
- **Smart prompts**: Generates focused error-fixing prompts
- Implementation: `AgenteCompletoV3.detectar_erro()` and `executar_com_recuperacao()`

### 2. Rate Limiting (CRITICAL - Official Limits)
```python
# Official Anthropic API limits per tier
LIMITES_OFICIAIS = {
    "tier1": {"rpm": 50, "itpm": 30000, "otpm": 8000},
    "tier2": {"rpm": 1000, "itpm": 450000, "otpm": 90000},
    "tier3": {"rpm": 2000, "itpm": 800000, "otpm": 160000},
    "tier4": {"rpm": 4000, "itpm": 2000000, "otpm": 400000}
}
```
- **RPM**: Requests per minute
- **ITPM**: Input tokens per minute
- **OTPM**: Output tokens per minute
- Uses sliding window with 1-minute tracking
- Proactive waiting before exceeding thresholds

### 3. Input System (`input_seguro()`)
- **Smart paste handling**: Detects large pasted text (Ctrl+V)
- **Preview mode**: Shows preview of large inputs with confirmation
- **Multi-line mode**: Type `multi` for multi-line input, end with `FIM`
- **Edit/cancel options**: Can edit or cancel before execution

### 4. UTF-8 Encoding (Windows Compatibility)
- Forces `PYTHONUTF8=1` and `PYTHONIOENCODING=utf-8`
- Reconfigures stdout/stderr for Windows console
- All file operations use explicit `encoding='utf-8'`
- Critical for paths with spaces and special characters

### 5. Computer Use (Playwright Integration)
- Requires: `pip install playwright && playwright install chromium`
- Tools: `navegador_iniciar`, `navegador_ir`, `navegador_screenshot`, `navegador_click`, etc.
- Browser lifecycle managed by `InterruptHandler` for cleanup

### 6. Notion Integration (SDK-based)
- **Direct API access**: No browser needed, 10x faster than Playwright
- **SDK**: Uses official `notion-client` library
- **Authentication**: Token-based (stored in credentials vault)
- **Operations**: Query databases, update pages, create pages, read schemas
- **Tools available**: 6 tools (`notion_conectar`, `notion_buscar_database`, `notion_atualizar_pagina`, etc.)
- **Implementation**: `integracao_notion.py` module with `IntegracaoNotion` class
- **Documentation**: See `INTEGRACAO_NOTION_GUIA.md` for complete guide

**Key advantages:**
- Fast: <1s vs 10-30s with browser
- Reliable: No UI changes breaking automation
- Lightweight: <10MB vs 500MB+ browser
- Headless-friendly: Works perfectly in server environments

### 7. Google Integration (Gmail + Calendar SDK-based)
- **Direct API access**: No browser needed, uses official Google APIs
- **SDKs**: Uses `google-api-python-client`, `google-auth`, `google-auth-oauthlib`
- **Authentication**: OAuth2 flow (tokens stored locally, auto-renewed)
- **Gmail Operations**: List emails (with filters), read full content, send emails (text/HTML), mark read/unread, delete, archive
- **Calendar Operations**: List events, create events (simple/recurrent), update events, delete events, search
- **Tools available**: 14 methods total (8 Gmail + 6 Calendar)
- **Implementation**: `integracao_google.py` module with `IntegracaoGmail` and `IntegracaoGoogleCalendar` classes
- **Documentation**: See `INTEGRACAO_GOOGLE_GUIA.md` for complete setup guide

**Gmail capabilities:**
- Advanced filters: by sender, subject, date range, read status, importance
- Full email content: text + HTML body, attachments metadata
- Send emails: plain text or HTML with CC/BCC support
- Email management: mark as read/unread, archive, delete (trash or permanent)
- Gmail query syntax: supports full Gmail search operators

**Calendar capabilities:**
- Event filtering: by date range, text search, calendar ID
- Recurrence support: RRULE format for weekly/monthly/daily patterns
- Event details: participants, location, Meet links, reminders
- Multi-calendar support: can access multiple calendars in the same account

**Key advantages:**
- Fast: <1s per operation vs 10-30s with Playwright
- Reliable: API is stable, no UI breaking changes
- Feature-rich: Access to all Gmail/Calendar features via API
- Secure: Official OAuth2 flow, tokens encrypted at rest
- Auto-renewal: Expired tokens refreshed automatically

**Setup requirements:**
1. Create project in Google Cloud Console
2. Enable Gmail API and Calendar API
3. Create OAuth 2.0 credentials (Desktop app)
4. Download credentials.json file
5. First run opens browser for authorization (one-time)
6. Subsequent runs use saved token automatically

## Configuration

### Environment Variables
Create `.env` file in project root:
```bash
ANTHROPIC_API_KEY=sk-ant-api-XXXXXXXX
```

### First Run Configuration
1. **API Tier**: Select 1-4 (default: 2 recommended)
2. **Rate limit mode**: conservative/balanced/aggressive (default: balanced)
3. **Credentials vault**: Optional, prompts for master password
4. **Memory system**: Automatically enabled if `memoria_permanente.py` exists

## Development Commands

### Running Luna
```bash
# Main optimized version (RECOMMENDED)
python luna_v3_FINAL_OTIMIZADA.py

# Legacy complete version
python agente_completo_final.py
```

### Testing
```bash
# Test file (basic validation)
python testes_luna_v3.py
```

### Dependencies
Required:
```bash
pip install anthropic python-dotenv
```

Optional (for full features):
```bash
# Playwright (web automation)
pip install playwright
playwright install chromium

# Integrations
pip install cryptography notion-client
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## File Structure

```
Luna/
├── luna_v3_FINAL_OTIMIZADA.py      # Main entry point (RECOMMENDED)
├── agente_completo_final.py         # Legacy complete version
├── memoria_permanente.py            # Persistent learning system
├── cofre_credenciais.py             # Encrypted credentials vault
├── gerenciador_workspaces.py       # Workspace manager
├── integracao_notion.py            # Notion API integration
├── integracao_google.py            # Google (Gmail + Calendar) integration (NEW)
├── sistema_auto_evolucao.py        # Self-evolution system
├── gerenciador_temp.py             # Temp files manager
├── .env                             # API key configuration
├── memoria_agente.json              # Memory database
├── cofre.enc                        # Encrypted credentials
├── workspace_config.json            # Workspace metadata
├── credentials.json                 # Google OAuth2 credentials (optional)
├── token_gmail.json                 # Gmail access token (auto-generated)
├── token_calendar.json              # Calendar access token (auto-generated)
├── CLAUDE.md                        # This file
├── INTEGRACAO_NOTION_GUIA.md       # Notion integration guide
├── INTEGRACAO_GOOGLE_GUIA.md       # Google integration guide (NEW)
├── workspaces/                      # User projects
│   ├── projeto1/
│   └── projeto2/
└── Luna/                            # Internal folders
    ├── planos/                      # Future: execution plans
    └── .stats/                      # Statistics
```

## Important Implementation Notes

### Code Quality Standards
- **Type hints**: ~80% coverage with Python typing module
- **Docstrings**: Google Style format in Portuguese
- **Error handling**: Comprehensive try-catch blocks
- **Encoding**: Explicit UTF-8 everywhere
- **Constants**: Uppercase with clear naming (e.g., `LIMITES_OFICIAIS`)

### Tool Execution Pattern
```python
# All tools return strings
# Tools use this standard format:
def executar(self, nome: str, parametros: Dict[str, Any]) -> str:
    if nome == "bash":
        # Execute bash command
        return resultado_string
    elif nome == "criar_arquivo":
        # Create file with UTF-8 encoding
        return "✅ Arquivo criado com sucesso"
```

### Memory System Integration
```python
# Before task: Search relevant learnings
aprendizados = memoria.buscar_aprendizados(query)

# After task: Save learnings
memoria.salvar_aprendizado(tipo, titulo, conteudo, tags)
```

### Workspace System
- Always use workspace-relative paths when workspace is active
- Files created go to `workspaces/{workspace_name}/` automatically
- Use `resolver_caminho()` to get absolute paths

### Error Patterns to Detect
The recovery system looks for these patterns in outputs:
- "ERRO:"
- "Traceback"
- "Error:"
- "Exception:"
- "Failed:"

## Debugging & Troubleshooting

### Common Issues

1. **"ANTHROPIC_API_KEY not found"**
   - Ensure `.env` file exists with valid key

2. **"Playwright not found"**
   - Only needed for computer use: `pip install playwright`

3. **Rate limit 429 errors**
   - System handles automatically with backoff
   - Check tier configuration matches your actual API tier

4. **Encoding errors on Windows**
   - UTF-8 configuration should handle this
   - Check `sys.platform == 'win32'` block is executing

5. **Memory/credentials not loading**
   - Check if respective `.py` files exist
   - Check file permissions on `.json` and `.enc` files

### Logging
- Uses `print_realtime()` for immediate user feedback
- Statistics tracked in `RateLimitManager` and saved at exit
- Memory system logs to console on startup

## Future Enhancements (Documented but Not Implemented)

1. **Planning System** - Dataclasses defined (`Subtarefa`, `Onda`, `Plano`) but not integrated
2. **ThreadPoolExecutor** - Imported but not used (prepared for parallel execution)
3. **Unit Tests** - No pytest suite (recommended addition)
4. **CI/CD** - No automation pipeline (recommended addition)
5. **Structured Logging** - Currently uses print; could use `logging` module

## Critical Safety Notes

- **Protected zones**: `sistema_auto_evolucao.py` defines code sections that cannot be auto-modified
- **Backup system**: Auto-evolution creates timestamped backups before any code modification
- **Graceful degradation**: All optional systems fail gracefully with warnings
- **Interrupt safety**: Ctrl+C always cleans up resources (browser, files, stats)
- **No credential leaks**: Passwords never printed, always use `getpass`

## Architecture Decisions

### Why Modular Optional Systems?
- Allows core to run with minimal dependencies
- Easy to disable features if issues occur
- Clear separation of concerns
- Each system can evolve independently

### Why String-Based Tool Returns?
- Claude API expects string responses
- Simplifies error handling
- Easy to log and display to users
- Consistent interface across all tools

### Why Sliding Window for Rate Limits?
- More accurate than simple counters
- Matches Anthropic's actual implementation
- Prevents burst issues
- Better token utilization

### Why Custom Input Function?
- Native `input()` doesn't handle large pastes well
- Preview prevents accidents with large prompts
- Multi-line mode essential for complex tasks
- User confirmation improves reliability

## When Making Changes

1. **Respect type hints**: Add proper type annotations
2. **Document in Portuguese**: Maintain docstring language consistency
3. **Test error recovery**: Ensure new tools work with recovery system
4. **Handle encoding**: Always use `encoding='utf-8'`
5. **Update memory**: New capabilities should be searchable
6. **Maintain backward compatibility**: Legacy scripts should still work
7. **Follow naming**: `snake_case` for functions, `PascalCase` for classes
8. **Add to tools list**: New tools need entries in both `ferramentas_codigo` and `ferramentas_descricao`

## Performance Characteristics

- **Startup time**: ~2-3 seconds (loading systems)
- **Rate limit overhead**: <0.1s per check
- **Memory persistence**: ~0.5s to save/load
- **Tool execution**: Varies by tool (bash can be slow)
- **Context window**: Uses Claude's full context (200K tokens)
- **Token estimation**: Uses median values per tool type

## Contact & Documentation

For more details, see:
- `README_VERSAO_FINAL.md` - Comprehensive documentation in Portuguese
- `GUIA_RAPIDO.md` - Quick start guide
- `CHANGELOG.md` - Version history and changes
- `RESUMO_EXECUTIVO.md` - Executive summary and quality analysis
