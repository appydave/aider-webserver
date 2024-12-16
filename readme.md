## Aider WebAPI

The Aider WebAPI was creating with this 1 SHOT prompt.


### Requirements Document for Aider Web API

## 1. Overview

This document outlines the requirements for building a web API to interact with the Aider scripting tool. The primary focus is on hosting Aider within a locally running web server, enabling interaction with projects on a local development machine. The API facilitates dynamic project directory management, instruction execution on files, and supports multiple configurations for enhanced usability. The implementation will use Flask as the web server framework, but the focus is on the API’s functionality rather than the specifics of the web server.

---

## 2. Functional Requirements

### 2.1 Dynamic Port Configuration

- **Description**: Allow users to specify the port for the web server when starting it.
- **Acceptance Criteria**:
  - Users can specify a port via a command-line argument.
  - Default port is 5000 if none is specified.
- **Example**:
  ```bash
  python aider_server.py --port 8080
  ```

### 2.2 Instruction Execution API

- **Description**: Execute instructions on specified files using Aider.
- **Endpoints**:
  - `POST /code_assistant`
- **Request Parameters**:
  - `instruction` (string): The instruction to execute.
  - `files` (optional array of strings): List of file names to operate on.
  - `directory` (optional string): Directory in which to execute the instruction, defaulting to the server’s current directory.
  - `model` (optional string): Specifies the model to use, defaulting to Aider’s configuration.
  - Options (optional):
    - `--auto-commits`, `--no-auto-commits`: Enable or disable auto commits of GPT changes (default: True).
    - `--dirty-commits`, `--no-dirty-commits`: Enable or disable commits when the repository is dirty (default: True).
    - `--dry-run`, `--no-dry-run`: Perform a dry run without modifying files (default: False).
- **Validation**:
  - `instruction` is required.
- **Response**:
  - Success: `{ "response": "Result of the instruction" }`
  - Error: `{ "error": "Instruction is required" }`

---

## 3. Non-Functional Requirements

### 3.1 Usability

- Simple API design with JSON-based communication.
- Clear error messages for invalid inputs.

### 3.2 Extensibility

- Support for additional endpoints in the future.
- Modular code structure for easy maintenance.

### 3.3 Performance

- Handle multiple simultaneous API requests efficiently.

### 3.4 Scalability

- Allow running multiple instances of the web server for different projects, each on a unique port.

---

## 4. Implementation Details

### 4.1 Flask Framework

- Use Flask to build the web server due to its simplicity and extensive community support.

### 4.2 Aider Integration

- Ensure the server integrates with Aider by:
  - Operating in the context of the current working directory.
  - Managing file and directory-specific chat histories.

### 4.3 Python Scripting Support

The API will also provide support for interacting with Aider through Python scripting. This enables advanced automation workflows by exposing the following features:

#### Example Python Script

```python
from aider.coders import Coder
from aider.models import Model

# This is a list of files to add to the chat
fnames = ["greeting.py"]

model = Model("gpt-4-turbo")

# Create a coder object
coder = Coder.create(main_model=model, fnames=fnames)

# Execute one instruction on those files and then return
coder.run("make a script that prints hello world")

# Send another instruction
coder.run("make it say goodbye")

# You can run in-chat "/" commands too
coder.run("/tokens")
```

- **Details**:
  - Use the `Coder.create()` and `Coder.init()` methods to configure coders.
  - Optional input parameters such as `io` can be set for additional configurations (e.g., `yes=True` to simulate `--yes` in the CLI).

#### Important Notes

- The Python scripting API is not officially supported or documented. It may change in future releases without backward compatibility.

---

### 4.4 Handling Directory Parameters

- The server dynamically uses the directory provided in each request or defaults to its running directory.
- Caveats:
  - Ensure Aider’s Git operations and chat history handling remain functional within the specified directory.

### 4.5 Command-Line Arguments

- `--port`: Specify the port to run the server.
- Example:
  ```bash
  python web_server.py --port 8080
  ```

---

## 5. Example Use Cases

### 5.1 Running an Instruction with Default Directory

- **Request**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"instruction": "create a script"}' http://localhost:5000/code_assistant
  ```
- **Response**:
  ```json
  { "response": "Instruction executed successfully" }
  ```

### 5.2 Running an Instruction with Specific Directory

- **Request**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"instruction": "create a script", "directory": "/new/project/path"}' http://localhost:5000/code_assistant
  ```
- **Response**:
  ```json
  { "response": "Instruction executed successfully" }
  ```

### 5.3 Running an Instruction with Additional Options

- **Request**:
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"instruction": "modify code", "options": {"auto-commits": false, "dry-run": true}}' http://localhost:5000/code_assistant
  ```
- **Response**:
  ```json
  { "response": "Dry run completed successfully" }
  ```

---

## 6. Key Decisions and Trade-Offs

### 6.1 Single vs. Multiple Server Instances

#### Option 1: Single Server with Dynamic Directory Switching

- **Pros**:
  - Simpler to manage.
  - Lower resource usage.
- **Cons**:
  - Risk of losing session context during directory switches.

#### Option 2: Multiple Server Instances

- **Pros**:
  - Complete isolation between projects.
  - Independent chat histories and file contexts.
- **Cons**:
  - More resource-intensive.
  - Higher management overhead.

---

## 7. Testing Plan

### 7.1 Functional Testing

- Test all API endpoints for valid and invalid inputs.
- Verify correct behavior for directory switching and instruction execution.

---

