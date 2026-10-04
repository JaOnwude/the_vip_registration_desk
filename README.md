# The VIP Registration Desk

A FastAPI microservice providing a secure registration endpoint for VIP staff members and a personalized greeting system for returning visitors using custom header and cookie model validations.

## Features

* **Header Validation**: Enforces custom header models (`X-Union-Pass` and `X-Client-Version`).
* **Schema Stripping (Security)**: Returns complete user models internally while automatically filtering out sensitive fields (like `password`) via Pydantic response models.
* **Interactive Documentation Examples**: Pre-configured schema examples directly rendered on Swagger UI (`/docs`).
* **Cookie Parameter Parsing**: Models incoming HTTP cookies (`session_id` and `language`) with automatic validation and fallback responses.
* **Localization**: Custom dynamic greeting support (`en`, `pidgin`, and standard fallback).

## Quick Start

### 1. Prerequisites & Installation

Ensure you have Python 3.10+ installed. Install the required dependencies:

```bash
pip install fastapi uvicorn pydantic
```

### 2. Running the Application

Start the development server using Uvicorn:

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`.

---

## Endpoints & API Reference

### 1. Register VIP Staff Member

* **Method**: `POST`
* **Path**: `/staff`
* **Status Code**: `201 Created`

#### Required Headers

| Header Key | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `X-Union-Pass` | `string` | **Yes** | Must equal `UNION-2026-VIP` |
| `X-Client-Version` | `string` | No | Defaults to `1.0` |

#### Request Body Example

```json
{
  "username": "JaOnwude",
  "full_name": "Onwude James Uchenna",
  "password": "James@123456",
  "station": "Terminal A1 - VIP"
}
```

#### Curl Example

```bash
curl -X POST "http://127.0.0.1:8000/staff" \
     -H "X-Union-Pass: UNION-2026-VIP" \
     -H "X-Client-Version: 1.0" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "JaOnwude",
       "full_name": "Onwude James Uchenna",
       "password": "James@123456",
       "station": "Terminal A1 - VIP"
     }'
```

---

### 2. Greet Returning Visitor

* **Method**: `GET`
* **Path**: `/desk/greeting`
* **Status Code**: `200 OK`

#### Required Cookies

| Cookie Name | Type | Required | Default | Description |
| :--- | :--- | :--- | :--- | :--- |
| `session_id` | `string` | **Yes** | — | Unique visitor session ID |
| `language` | `string` | No | `"en"` | Language option (`"en"`, `"pidgin"`) |

#### Curl Examples

**Valid Request (Pidgin Greeting):**

```bash
curl -b "session_id=abc123; language=pidgin" http://127.0.0.1:8000/desk/greeting
```

*Response:*
```json
{
  "greeting": "How far, you don come again!",
  "session_id": "abc123"
}
```

**Missing Required Session Cookie (Fails automatically with 422):**

```bash
curl http://127.0.0.1:8000/desk/greeting
```

---

## Interactive Documentation

Access the interactive API documentation directly in your browser:

* **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
