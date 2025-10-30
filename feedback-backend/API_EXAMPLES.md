# API Usage Examples

## Using cURL

### Submit Feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "feedback": "Excellent service!"
  }'
```

### Get All Feedback
```bash
curl http://localhost:5000/api/feedback
```

### Get Feedback with Pagination
```bash
curl "http://localhost:5000/api/feedback?limit=5&offset=10"
```

### Get Specific Feedback
```bash
curl http://localhost:5000/api/feedback/1
```

### Delete Feedback
```bash
curl -X DELETE http://localhost:5000/api/feedback/1
```

### Get Statistics
```bash
curl http://localhost:5000/api/stats
```

## Using Python Requests

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Submit feedback
response = requests.post(f"{BASE_URL}/feedback", json={
    "name": "Python User",
    "email": "user@python.com",
    "feedback": "Great API!"
})
print(response.json())

# Get all feedback
response = requests.get(f"{BASE_URL}/feedback")
print(response.json())

# Get statistics
response = requests.get(f"{BASE_URL}/stats")
print(response.json())
```

## Using JavaScript (Fetch API)

```javascript
// Submit feedback
fetch('http://localhost:5000/api/feedback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        name: 'JS User',
        email: 'user@js.com',
        feedback: 'Awesome API!'
    })
})
.then(response => response.json())
.then(data => console.log(data));

// Get all feedback
fetch('http://localhost:5000/api/feedback')
    .then(response => response.json())
    .then(data => console.log(data));
```

## Using Postman

1. Import collection from `postman_collection.json`
2. Set base URL to `http://localhost:5000`
3. Run requests from the collection

## Error Examples

### Invalid Email
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid","feedback":"Test"}'

# Response: {"error": "Invalid email format"}
```

### Missing Feedback
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"name":"Test"}'

# Response: {"error": "Feedback content is required"}
```

### Feedback Too Long
```bash
curl -X POST http://localhost:5000/api/feedback \
  -H "Content-Type: application/json" \
  -d '{"feedback":"'$(printf 'x%.0s' {1..1001})'"}'

# Response: {"error": "Feedback text too long (max 1000 characters)"}
```
