# OCR System Backend

A Django REST-based OCR backend using Tesseract for text extraction from PDFs, with user/session management and PostgreSQL storage.

## 🛠 Tech Stack

- **Framework:** Django REST Framework (DRF)
- **OCR Engine:** Tesseract
- **Database:** PostgreSQL
- **Language:** Python
- **PDF Handling:** PyPDF2, Pillow, or similar

## ✨ Features

- Upload PDFs and extract text using OCR
- Store extracted data into PostgreSQL
- User authentication and session management
- RESTful APIs for file upload, OCR processing, and data retrieval
- Clean and modular backend code structure

## 🧑‍💻 Role

> This repository includes **backend development only** — built and maintained by me.  
> I was responsible for:
- Session Management
- User Authentication
- OCR APIs and business logic
- PostgreSQL data storage

## 📁 Project Structure

```
ocr-backend/
├── ocr_app/              # Core OCR logic
├── users/                # Authentication & user management
├── api/                  # API routing & views
├── media/                # Uploaded PDF files
├── manage.py
└── requirements.txt
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ocr-backend.git
cd ocr-backend
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # on Windows use: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations and run server

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_NAME=ocrdb
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## 🧪 Sample API Endpoints

| Method | Endpoint            | Description               |
|--------|---------------------|---------------------------|
| POST   | `/api/upload/`      | Upload PDF for OCR        |
| GET    | `/api/results/`     | Retrieve extracted data   |
| POST   | `/api/login/`       | User login                |
| POST   | `/api/register/`    | User registration         |

## 📄 License

MIT License
