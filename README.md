# 🍽️ Cloud Kitchen Web Application

A full-stack cloud kitchen management system built with **FastAPI (backend)** and **React (frontend)**.
This application allows users to browse menu items, place orders, and manage payments, while also supporting authentication and admin-level operations.

---

## 🚀 Features

### 👤 User Features

* User Registration & Login (JWT Authentication)
* Browse Menu Items (categorized)
* Place Orders
* Apply Discount Codes
* View Order History

### 🛠️ Admin Features

* Manage Menu Items (Add/Edit/Delete)
* Manage Discounts
* Track Orders & Payments

---

## 🧱 Tech Stack

### 🔹 Backend

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Migrations:** Alembic
* **Authentication:** JWT (python-jose)
* **Password Hashing:** Passlib (bcrypt / argon2)

### 🔹 Frontend

* **Framework:** React (Vite)
* **HTTP Client:** Axios
* **UI:** Basic React Components

---

## 📁 Project Structure

```
cloudKitchenFrontend/     # React frontend
fastapiBackend/           # FastAPI backend
│
├── app/
│   ├── api/              # Routes (auth, menu, orders)
│   ├── core/             # Config, security
│   ├── models/           # Database models
│   ├── services/         # Business logic
│
├── alembic/              # DB migrations
├── requirements.txt      # Backend dependencies
```

---

## ⚙️ Setup Instructions

### 🔹 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/cloud_kitchen.git
cd cloud_kitchen
```

---

### 🔹 2. Backend Setup

```bash
cd fastapiBackend

# Create virtual environment
python -m venv venv
venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

---

### 🔹 3. Database Setup (PostgreSQL)

Create a database:

```sql
CREATE DATABASE cloud_kitchen;
```

Update your database URL in:

```
app/core/config.py
```

Example:

```
postgresql://postgres:yourpassword@localhost:5432/cloud_kitchen
```

---

### 🔹 4. Run Migrations

```bash
alembic upgrade head
```

---

### 🔹 5. Run Backend

```bash
uvicorn app.main:app --reload
```

Backend runs at:

```
http://127.0.0.1:8000
```

API Docs:

```
http://127.0.0.1:8000/docs
```

---

### 🔹 6. Frontend Setup

```bash
cd ../cloudKitchenFrontend

npm install
npm run dev
```

Frontend runs at:

```
http://localhost:5173
```

---

## 🔗 API Integration

Make sure frontend API base URL is set to:

```js
http://127.0.0.1:8000
```

---

## 🧪 Testing the Application

1. Open Swagger Docs
2. Register a user
3. Login to get token
4. Use frontend to:

   * Browse items
   * Place orders

---

## ⚠️ Important Notes

* Do NOT commit `venv/` or `node_modules/`
* Use `.env` for sensitive configs
* Passwords are securely hashed (not stored as plain text)

---

## 📌 Future Improvements

* Payment Gateway Integration (Razorpay/Stripe)
* Admin Dashboard UI
* Order Tracking System
* Deployment (Docker + Cloud)

---

## 👨‍💻 Author

**Dhekshath**

---

## 📜 License

This project is for educational purposes.
