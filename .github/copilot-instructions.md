# Coding Guidelines
- Always write extremely comprehensive, simple comments for LITERALLY EVERY SINGLE LINE, method, and function.
- Explain the purpose of standard Python built-ins or library functions in plain English.
- Keep comments simple enough for a non-technical 10-year-old child to understand.
- When importing from sibling packages, always append parent folders to sys.path at the top:
  sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))