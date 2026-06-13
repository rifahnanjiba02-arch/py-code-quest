# Py Code Quest

Py Code Quest is a Python project centered around a Groq-backed service layer and configurable runtime settings.

The repository appears to be organized for local development with a Dev Container, making it easier to get a consistent environment up and running.

## What’s Included

- Python application code
- Groq service integration
- Centralized configuration modules
- Dependency list in `requirements.txt`
- Dev Container setup for reproducible development

## Project Structure

- `config.py` - top-level configuration
- `services/` - service code
- `services/groq_service.py` - Groq integration logic
- `services/config.py` - service-specific configuration
- `requirements.txt` - Python dependencies
- `.devcontainer/` - containerized development setup

## Getting Started

### Prerequisites

- Python 3.10+ recommended
- A Groq API key, if the service requires one

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create or update your local environment variables as needed for the service.

Common variables you may need:

- `GROQ_API_KEY`
- any app-specific config values defined in `config.py` or `services/config.py`

If you are using the Dev Container, add the same values to your container environment or `.env` file as appropriate for your setup.

## Running the Project

Because the repository may be wired to a specific entry point, start the app using the project’s main script or framework command.

If you are unsure where to start, check:

- `config.py`
- `services/groq_service.py`
- your application entry file, if one exists

## Development Notes

- Keep secrets out of version control.
- Prefer environment variables for API keys and runtime settings.
- Use the Dev Container if you want a repeatable setup across machines.


