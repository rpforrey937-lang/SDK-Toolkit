# Contributing to Agentic Commerce Toolkit

We welcome contributions! Here's how to get started.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/agentic-commerce-toolkit.git
   cd agentic-commerce-toolkit
   ```

2. Set up Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r sdk-python/setup.py
   pip install -r gateway/requirements.txt
   pip install -r mcp-server/requirements.txt
   ```

4. Or use Docker:
   ```bash
   docker-compose up
   ```

## Code Style

- Follow PEP 8 for Python code
- Use 4 spaces for indentation
- Add docstrings to functions and classes
- Keep lines under 100 characters

## Submitting Changes

1. Create a feature branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit:
   ```bash
   git commit -am "Add your change description"
   ```

3. Push to the branch:
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a pull request

## Reporting Issues

Please use the GitHub Issues page to report bugs or request features. Include:

- A clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs. actual behavior
- Your environment details (OS, Python version, etc.)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
