# 🏦 Banking System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-teal.svg)
![Postgres](https://img.shields.io/badge/Postgres-15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Project-Work%20in%20Progress-orange.svg)

A **Banking System** project built with **Django** (monolith) and **FastAPI microservice** for handling transactions.  
The project is designed to be modular, scalable, and developer-friendly.  

## 📂 Project Structure
```
Banking/
├── django_monolith/        # Django core app (accounts, users, admin)
├── transaction_service/    # FastAPI microservice for handling transactions
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```
---

## ⚙️ Tech Stack  

- **Backend 1**: Django (Monolith - users, accounts, admin)  
- **Backend 2**: FastAPI (Transactions microservice)  
- **Database**: PostgreSQL  
- **Auth**: Django built-in auth system  
- **Containerization**: Docker (future)  

---

## 🚀 Getting Started  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/bankingApp.git

cd bankingApp
```
2️⃣ Create virtual environment & install dependencies

```
python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
```
3️⃣ Run Django monolith

```
cd django_monolith
python manage.py migrate
python manage.py runserver
```

4️⃣ Run FastAPI microservice
```
cd transaction_service
uvicorn main:app --reload --port 8001
```
## 📌 Notes  

- Django app runs on: **http://127.0.0.1:8000/**  
- FastAPI service runs on: **http://127.0.0.1:8001/**  
- Both services can communicate via API calls.  
- Use **PostgreSQL** as the default database.  
- Make sure virtual environment is activated before running servers.



## 📚 API Documentation  

Once the servers are running, you can access the auto-generated API documentation at the following endpoints:

### Django (future)
* **Browsable API:** `http://127.0.0.1:8000/api/`

### FastAPI
* **Swagger UI:** `http://127.0.0.1:8001/docs/`  
* **ReDoc:** `http://127.0.0.1:8001/redoc/`


## 🔮 Future Work  

Planned improvements and upcoming features include:

* Add **unit & integration tests**  
* Implement **Docker support** for both services  
* Enhance **API documentation** and security layers  
* Add **CI/CD pipeline** for automated testing and deployment  
* Improve **logging & monitoring** for microservices  










