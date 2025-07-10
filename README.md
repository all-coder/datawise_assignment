# Datawise Assignment

## 🛠️ Setup Instructions

1. **Install MongoDB**
   - Download and install MongoDB on your system.
   - Allow access from your IP and create a user with read/write permissions.
   - Note your **Connection URI** with the correct username, password, and cluster URL.

2. **Clone the Repository**  
   ```bash
   git clone https://github.com/all-coder/datawise_assignment.git
   cd datawise_assignment
   ```

3. **Create a Python Virtual Environment**  
   ```bash
   python3 -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   ```

4. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**  
   Create a `.env` file in the root directory:
   ```env
   MONGODB_URI="your_mongodb_connection_uri"
   PYTHONPATH=. 
   ```

6. **Run the Application**  
   ```bash
   python main.py
   ```

---
## API Documentation

To access the Swagger UI:

1. Make sure the Flask application is running.
2. Open your browser and navigate to:

   ```text
   http://localhost:5000/apidocs/
    ```
---
### Postman Collection

A Postman collection is included in the repository for testing the API endpoints.

**File:** [`DatawiseAssignment.postman_collection.json`](./DatawiseAssignment.postman_collection.json)

You can import this file into Postman to try out all available routes with example requests.

---

## Running Tests

To run the tests, use:

```bash
dotenv -f .env run pytest tests/   
```
