
# FastAPI Server API Documentation

This document provides a guide to the available API endpoints for the FastAPI server running at `http://baculum.i234.me:8509`. Each endpoint's purpose and the corresponding `curl` command to interact with it are provided below.

## Base URL
All requests should be made to the following base URL:
```
http://baculum.i234.me:8509
```

## Authorization
All requests require an API key for authorization. The API key should be provided in the `Authorization` header.

---

## 1. `GET /`

### Description
A simple ping endpoint to check if the server is running.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/" -H "Authorization: user1_api_key"
```

### Response
- **200 OK**: Returns `{"message": "pong"}` if the server is running.

---

## 2. `POST /filelist/`

### Description
Returns a list of all files in the upload directory.

### `curl` Command
```bash
curl -X POST "http://baculum.i234.me:8509/filelist/" -H "Authorization: user1_api_key"
```

### Response
- **200 OK**: Returns a JSON array of filenames in the upload directory.

---

## 3. `POST /sendfile/`

### Description
Fetches the contents of a specified file from the upload directory.

### `curl` Command
```bash
curl -X POST "http://baculum.i234.me:8509/sendfile/" -H "Authorization: user1_api_key" -H "Content-Type: application/json" -d "{\"filename\": \"mapping_tree.json\"}"
```

### Request Body
- `filename`: The name of the file you want to retrieve.

### Response
- **200 OK**: Returns the contents of the specified file as JSON.
- **404 Not Found**: If the specified file does not exist.
- **500 Internal Server Error**: If there is an error reading the file.

---

## 4. `GET /latestfile/`

### Description
Fetches the contents of the latest file (by creation time) in the upload directory.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/latestfile/" -H "Authorization: user1_api_key"
```

### Response
- **200 OK**: Returns the contents of the latest file as JSON.
- **404 Not Found**: If no files are found in the directory.
- **500 Internal Server Error**: If there is an error reading the latest file.

---

## 5. `GET /step/{step}`

### Description
Fetches metadata for a specific simulation step.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/step/1" -H "Authorization: user1_api_key"
```

### Path Parameters
- `step`: The step number for which metadata is being requested.

### Response
- **200 OK**: Returns the metadata for the specified step as JSON.
- **404 Not Found**: If the specified step does not exist.

---

## 6. `GET /piece/image_url/{image_location}`

### Description
Fetches an image file based on its location identifier.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/piece/image_url/image_location_example" -H "Authorization: user1_api_key"
```

### Path Parameters
- `image_location`: The identifier for the image location.

### Response
- **200 OK**: Returns the image file as a JPEG.
- **404 Not Found**: If the specified image is not found.

---

## 7. `GET /piece/`

### Description
Fetches a list of image coordinates and their corresponding URLs.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/piece/" -H "Authorization: user1_api_key"
```

### Response
- **200 OK**: Returns a JSON object containing image coordinates and URLs.

---

## 8. `GET /user_interrupt/`

### Description
Allows interaction with an NPC at a specific simulation timestamp.

### `curl` Command
```bash
curl -X GET "http://baculum.i234.me:8509/user_interrupt/?query=Hello&npc_name=NPC1&cur_timestamp=10" -H "Authorization: user1_api_key"
```

### Query Parameters
- `query`: The user's query to the NPC.
- `npc_name`: The name of the NPC to interact with.
- `cur_timestamp`: The current simulation timestamp.
- `num_memory` (optional): The number of memory steps the NPC can use (default is 999).

### Response
- **200 OK**: Returns the NPC's response based on the provided query and timestamp.

---

## Notes
- Replace `user1_api_key` with the actual API key you are using.
- Ensure that the server is running and accessible at `http://baculum.i234.me:8509`.
