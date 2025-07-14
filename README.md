# 🏆 SPORTSMAXX

**Elevate Your Game!**\
SPORTSMAXX is a user-friendly online platform offering top-quality jerseys, cycles, sportswear, and sporting equipment—all in one place.

---

## About the Project

SPORTSMAXX is a scalable e-commerce application built with a full-stack Django framework. It features an intuitive frontend with dynamic filtering and AJAX interactions, and a secure, production-ready backend hosted on AWS.

The project includes:

- A seamless shopping experience for users
- Comprehensive admin control over product, users, and order management
- Secure payments and promotional offers
- Scalable infrastructure for future growth

---

## Features

### User Side

- **Account Registration & Login**
- **Wishlist & Cart Management**
- **Coupons and Discounts**
- **Multiple Payment Methods**\
  Supports: COD, Razorpay, Wallet
- **Referral Program**
- **Order Tracking & Retry Payment**
- **Secure Checkout & HTTPS Enabled**

### Admin Side

- **Product Management**\
  (Variants, Sizes, Stock, Categories)
- **Banner & Offer Management**
- **Coupon System Control**
- **Sales Analytics**\
  (Charts, Tables, Download as PDF/Excel)
- **Order Fulfillment Dashboard**
- **User Management Panel**

---

## Tech Stack

| Layer           | Technology                        |
| --------------- | --------------------------------- |
| Backend         | Django (Python)                   |
| Frontend        | HTML, JavaScript, AJAX, Bootstrap |
| Database        | PostgreSQL                        |
| Hosting         | AWS EC2 + Nginx                   |
| Domain & SSL    | Hostinger + HTTPS                 |
| Version Control | Git & GitHub                      |

---

## Getting Started (Dockerized Setup)

### Prerequisites

- Docker
- Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/MrLionByte/Sportsmaxx-Dockerized
cd Sportsmaxx-Dockerized
```

### 2. Add `.env` File

Create a `.env` file in the root directory:

```env
# Django
ALLOWED_HOSTS=127.0.0.1,localhost
SECRET_KEY=your_django_secret_key
DEBUG=True

# Database (choose one)
POSTGRES_DB=sportsmaxx
POSTGRES_USER=postgres
POSTGRES_PASSWORD=yourpassword
POSTGRES_PORT=5432
# OR use external DB:
# DATABASE_URL=postgres://user:password@hostname:port/dbname

# Email
EMAIL_PORT=587
EMAIL_HOST_USER=youremail@example.com
EMAIL_HOST_PASSWORD=your_app_password
EMAIL_TLS=True
EMAIL_SSL=False

# Razorpay
RAZORPAY_KEY=your_key
RAZORPAY_SECRET=your_secret

# Cloudinary
cloudinary_cloud_name=your_cloud_name
cloudinary_api_key=your_key
cloudinary_api_secret=your_secret

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_SECRET=your_google_client_secret
```

### 3. Build and Run Containers

```bash
docker-compose up -d --build
```

### 4. Run Migrations and Create Superuser

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the App

- Frontend: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## Deployment Notes

- **Production Web Server**: Nginx (reverse proxy)
- **Gunicorn**: WSGI HTTP server
- **HTTPS**: SSL Certificate via Hostinger/GoDaddy
- **Static & Media Files**: Served via Nginx or S3-compatible services

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---
