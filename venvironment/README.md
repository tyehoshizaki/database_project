# Virtual Environment Management

This directory contains scripts and configuration for managing a Python virtual environment.

## Files

- `setup_venv.sh` - Script to create and set up the virtual environment
- `requirements.txt` - Python package dependencies
- `activate_venv.sh` - Quick activation script
- `.gitignore` - Git ignore file (excludes virtual environment from version control)

## Quick Start

1. **Create and activate virtual environment:**
   ```bash
   ./setup_venv.sh
   ```

2. **Manually activate virtual environment:**
   ```bash
   source venv/bin/activate
   ```

3. **Install new packages:**
   ```bash
   pip install package_name
   pip freeze > requirements.txt  # Save to requirements
   ```

4. **Deactivate virtual environment:**
   ```bash
   deactivate
   ```

## Managing Dependencies

- Add package names and versions to `requirements.txt`
- Run `pip install -r requirements.txt` to install all dependencies
- Use `pip freeze > requirements.txt` to save current installed packages

## Notes

- The virtual environment folder (`venv/`) is excluded from git
- Always activate the virtual environment before working on the project
- Use `pip list` to see currently installed packages