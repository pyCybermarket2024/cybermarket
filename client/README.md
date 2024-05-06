# cybermarket_client

The client of a online cybermarket.

**Module goals:** Build a module that sends a binary message to cybermarket_server and responds accordingly based on the server's reply.

## Overview
This project consists of several Python files that together form an application for interacting with a server. Each file serves a specific purpose in the application.

## File Summaries

1. **`__init__.py`**
   - Purpose: Module initialization.
   - Content: Contains a docstring.

2. **`__main__.py`**
   - Purpose: Entrance to the main program.
   - Content: Defines the main entry point for the program and imports necessary modules.

3. **`lang.py`**
   - Purpose: Language configuration of server information.
   - Content: Defines language-related functionalities such as module paths.

4. **`logic.py`**
   - Purpose: Initializes the Script class.
   - Content: Contains code for initializing the Script class and interacting with the server.

5. **`request.py`**
   - Purpose: Functions that interact with the server.
   - Content: Implements functions for server communication and message handling.

6. **`settings.py`**
   - Purpose: Entrance to the interactive interface.
   - Content: Defines settings related to the interactive interface.

7. **`ui.py`**
   - Purpose: User interface.
   - Content: Defines user interface components using PyQt5.

## Usage
To use this application, run `__main__.py` to start the program. Ensure that all necessary dependencies are installed before running the program.

## Dependencies
- PyQt5
- loguru
- pandas
