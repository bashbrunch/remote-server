![BashBrunch](https://bashbrunch.attaditya.space/preview.png)

# BashBrunch (OTN Server)

BashBrunch OTN (Over The Network) Server is a session-based communication and logging server. It provides a REST API for managing isolated sessions, appending system logs, and exchanging messages through a buffered queue system.

## Technical Overview

The server manages multiple concurrent sessions. Each session is secured via an `Authorization` header (session key) and is identified by a `session_id`.

### Core Features
- **Session Management**: Create, verify, and delete isolated sessions.
- **Log Persistence**: Append text logs to a session and retrieve them via a reverse-order stream.
- **Message Queue**: Send messages to a session buffer and retrieve/pop them using a unique message key.

### Stack
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Middleware**: Custom CORS implementation (`src.cors`)
- **Session State**: In-memory dictionary storage

## API Reference

All requests (except the home root) require an `Authorization` header to authenticate the session.

### Session Control
- `POST /{session_id}`: Starts a new session or verifies an existing one.
- `GET /{session_id}`: Checks if a session is active and authorized.
- `DELETE /{session_id}`: Terminates the session.

### Log Management
- `POST /{session_id}/logs`: Appends raw text to the session log.
- `GET /{session_id}/logs`: Returns logs as a `StreamingResponse` in reverse chronological order (newest first).

### Messaging System
- `POST /{session_id}/message`: Adds a message to the session buffer. The server generates a unique random key for this message.
- `GET /{session_id}/message`: Retrieves the oldest message in the buffer. Returns the format: `key
content`.
- `DELETE /{session_id}/message/{key}`: Removes a specific message from the buffer if the key matches the oldest message.

## Setup

### Prerequisites
- Python 3.12+

### Installation
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution
```bash
uvicorn src.core.main:app
```
The server will be available at `http://0.0.0.0:8000`.

## Usage Example

**1. Start a Session**
```bash
curl -X POST http://localhost:8000/my-session-123 \
   -d "my-secret-key"
```

**2. Send a Log**
```bash
curl -X POST http://localhost:8000/my-session-123/logs \
     -H "Authorization: my-secret-key" \
     -d "System boot complete"
```

**3. Send a Message**
```bash
curl -X POST http://localhost:8000/my-session-123/message \
     -H "Authorization: my-secret-key" \
     -d "Hello from the user!"
```

**4. Retrieve the Message**
```bash
curl -X GET http://localhost:8000/my-session-123/message \
     -H "Authorization: my-secret-key"
```
