# Datawise Assignment

## 🛠️ Setup Instructions

1. **Install MongoDB Atlas**  
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas/register) and create a free cluster.  
   - Create a database named `datawise`.  
   - Whitelist your IP and create a user with read/write permissions.  
   - Note your **Connection URI** (replace `<username>`, `<password>`, and `<cluster-url>` accordingly).  

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
   ```

6. **Run the Application**  
   ```bash
   python main.py
   ```

---

## ✅ Running Tests

To run the tests, use:

```bash
PYTHONPATH=$(pwd) pytest tests/
```
