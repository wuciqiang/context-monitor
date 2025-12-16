# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-12-16

### Added
- 🎉 Initial release of Claude Context Monitor
- ✅ SessionStart hook for automatic session tracking
- ✅ Context Monitor MCP server with two tools:
  - `check_context_usage` - Monitor context usage percentage
  - `save_session_state` - Save session state for recovery
- ✅ Smart alert system with 4 levels (SAFE, WARNING, HIGH, CRITICAL)
- ✅ Automatic state saving and recovery after `/clear`
- ✅ npm installation support with `npm install @claude/context-monitor`
- ✅ Comprehensive documentation:
  - README.md - Project overview
  - INSTALL.md - Installation guide
  - CONTEXT_MONITORING.md - Usage documentation
  - QUICK_START.md - 5-minute quick start
  - STATELESS_WORKFLOW_GUIDE.md - Workflow guide
  - MIGRATION_GUIDE.md - Migration guide
  - PUBLISHING.md - Publishing guide
  - GITHUB_SETUP.md - GitHub setup guide
- ✅ Test script for system verification
- ✅ Initialization script for easy setup
- ✅ Uninstall script for clean removal

### Features
- Automatic context usage monitoring
- Claude-driven intelligent alerts
- Session state persistence
- Cross-project portability
- Simple npm-based installation

### Technical Details
- Node.js 18+ support
- Python 3.7+ support
- Bash script support
- Claude Code 2.0+ compatibility
- MCP protocol integration
- Hook system integration

---

## [Unreleased]

### Planned
- More accurate token calculation using tiktoken
- Web dashboard for real-time monitoring
- Automatic state backup
- Multi-session support
- Historical usage analysis
- GitHub Actions integration
- VS Code extension

---

## Release Notes

### v1.0.0 - Initial Release

This is the first stable release of Claude Context Monitor. The system provides semi-automated context usage monitoring for Claude Code through a combination of hooks, MCP servers, and intelligent Claude instructions.

**Key Features:**
- Automatic session tracking
- Real-time usage monitoring
- Smart alerts and recommendations
- State saving and recovery
- Easy npm installation

**Installation:**
```bash
npm install @claude/context-monitor
npm run init
```

**Usage:**
Start Claude Code and the system will automatically activate. Claude will periodically check context usage and alert you when it's time to save state and clear context.

**Documentation:**
All documentation is included in the package. Start with README.md for an overview.

**Support:**
- GitHub Issues: Report bugs and request features
- npm: https://www.npmjs.com/package/@claude/context-monitor

---

**Thank you for using Claude Context Monitor!** 🚀
