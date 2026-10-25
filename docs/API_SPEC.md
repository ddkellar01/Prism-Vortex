# PrismVortex API Specification

Base URL: `http://localhost:8080`

## Endpoints

### 1. Health Check
* **URL:** `/health`
* **Method:** `GET`
* **Response:** Returns service health status and active environment.

### 2. Execute Scout Operation
* **URL:** `/v1/scout`
* **Method:** `POST`
* **Request Body:**
```json
{
  "target_identifier": "Facility_9_Gateway",
  "coordinates": [34.0522, -118.2437],
  "objective": "Scout for perimeter threats, supply chain risks, and access anomalies."
}
