# Bus Ticket Booking API

This Django application provides endpoints for searching buses, blocking seats, and booking seats for a bus journey. It uses Django REST framework for the API implementation and JWT authentication for secure access.

## API Endpoints

### 1. Search Buses

**URL**: `/api/search-buses/`  
**Method**: `GET`  
**Auth**: JWT Bearer Token required

**Description**: Searches for buses based on the source and destination.

**Request Body**:
```json
{
  "source": "City A",
  "destination": "City D"
}
