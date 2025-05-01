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
DATABASE_USER=root
DATABASE_PASSWORD=****
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

## 🧪 Sample API Endpoints

| Method | Endpoint                       | Description               |
|--------|--------------------------------|---------------------------|
| POST   | `/reportocr/ocr/`              | Upload PDF for OCR        |
| GET    | `/reportocr/getOcrDocsList/`   | Retrieve extracted data   |
| POST   | `/usermanagement/login/`       | User login                |
| POST   | `/usermanagement/register/`    | User registration         |

## 👨‍💻 **Author**

**Waqar Yaqoob**

- GitHub: [@waqayaqoob21](https://github.com/waqayaqoob21)  
- Email: waqaryaqoob21@gmail.com  
- LinkedIn: [linkedin.com/in/waqaryaqoob21](https://linkedin.com/in/waqaryaqoob21)

---

## 📄 **License**

This project is licensed under the **MIT License**.  
See the [`LICENSE`](LICENSE) file for details.

---

## 🌟 **Show Your Support**

If you like this project:

- ⭐ Star this repository on GitHub  
- 🧑‍💻 Share it with your network  
