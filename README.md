<p align="center">
  <img src="grihaloy/static/images/logo.png" alt="Grihaloy Logo" width="180"/>
</p>

<p align="center">
  <b>A Smart Rental Management Platform for Bangladesh</b><br>
  Simplifying property renting through modern web technology.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Framework-Django-0C4B33?style=flat-square&logo=django&logoColor=white"/>
  <img src="https://img.shields.io/badge/Language-Python%203.10+-blue?style=flat-square&logo=python"/>
  <img src="https://img.shields.io/badge/Frontend-Bootstrap%205-purple?style=flat-square&logo=bootstrap"/>
  <img src="https://img.shields.io/badge/Database-SQLite-lightgrey?style=flat-square&logo=sqlite"/>
  <img src="https://img.shields.io/badge/Status-Active-success?style=flat-square"/>
</p>

---

## 🌆 Overview

**Grihaloy** is an advanced **web-based rental management platform** crafted for the modern Bangladeshi housing ecosystem.  
It acts as a **digital bridge** between **landlords and renters**, automating the process of renting, verification, and property communication — replacing traditional, time-consuming manual methods with an intelligent, data-driven, and secure approach.

Built using **Django (Python)** as the backend framework and **Bootstrap 5** for the frontend, Grihaloy is designed to be **scalable, responsive, and easy to use**.  
The system provides role-based dashboards, allowing **Admins**, **Landlords**, and **Renters** to seamlessly interact within a unified digital environment.

> ⚙️ Grihaloy’s ultimate goal is to modernize the real estate rental industry of Bangladesh through **automation, transparency, and digital transformation**.

---

## 🧭 Core Vision

> To revolutionize the traditional renting system in Bangladesh by introducing a **secure, intelligent, and fully digitalized** solution — empowering property owners and renters with technology that fosters **trust, speed, and efficiency**.

### 🎯 Problem It Solves

Traditional renting in Bangladesh is often:
- Manual and time-consuming  
- Lacking document verification systems  
- Non-transparent in pricing and agreements  
- Hard to manage multiple property listings or tenant communications  

**Grihaloy** eliminates these issues by offering:
- Centralized **user verification and data storage**
- Built-in **heatmap analytics** for rental prices
- **Automated approval workflows** for property requests
- Future modules for **digital rent payment and smart notifications**

---

## 🧠 Broad Description

At its heart, **Grihaloy** is a **multi-role platform** with a layered architecture that ensures data separation, performance, and scalability.  

### 💼 Landlords
Landlords can register properties, upload images, set rental prices, and verify renters through a secure digital channel.  
They get a dedicated dashboard to manage properties, view requests, and communicate directly with potential tenants.

### 👥 Renters
Renters can browse listings, send rental requests, upload identification documents, and track verification progress — all in one place.  
They can also view rental price insights using the **heatmap service**, helping them make better housing decisions.

### 🧑‍💼 Admins
Admins maintain full control of the platform — approving new users, verifying identities, managing reports, and monitoring system activity.

Together, these three roles create a **secure ecosystem** that makes renting faster, smarter, and safer.

---

## 🖼️ Project Preview

> 📸 A glimpse of **Grihaloy** in action:

<p align="center">
  <img src="grihaloy/static/images/screenshot.png" alt="Grihaloy Homepage" width="700"/>
</p>

---

## ✨ Key Features

✅ **Role-Based Authentication** — Admin, Landlord, and Renter login with isolated permissions  
✅ **Document Verification** — Secure upload and verification of identity documents  
✅ **Heatmap Visualization** — Visual representation of rent prices across areas  
✅ **Notification System** — Smart alerts for verification, approval, or property updates  
✅ **Modern UI/UX** — Fully responsive layout powered by Bootstrap 5  
✅ **Admin Dashboard** — Centralized control for user and data management  
✅ **Secure File Handling** — Uploaded files stored under media/ for controlled access  
✅ **Scalable Architecture** — Supports PostgreSQL, WebSockets, and additional apps  

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend Framework** | Django 5+ |
| **Programming Language** | Python 3.10+ |
| **Frontend Framework** | Bootstrap 5, HTML5, CSS3 |
| **Database** | SQLite (default) / PostgreSQL (optional) |
| **Authentication** | Django Auth System |
| **Visualization** | Custom Heatmap Service |
| **Deployment (Optional)** | Render / Railway / Nginx + Gunicorn |

---

## ⚙️ Installation & Setup

### 🪟 On Windows

```bash
# 1️⃣ Clone the repository
git clone https://github.com/AniK-75/project_Grihaloy.git
cd Grihaloy

# 2️⃣ Create and activate virtual environment
python -m venv venv
venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python manage.py migrate

# 5️⃣ Create admin user
python manage.py createsuperuser

# 6️⃣ Run the development server
python manage.py runserver
```
### 🐧 On Linux / macOS

```bash
# 1️⃣ Clone the repository
git clone https://github.com/AniK-75/project_Grihaloy.git
cd Grihaloy

# 2️⃣ Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Apply migrations
python3 manage.py migrate

# 5️⃣ Create admin user
python3 manage.py createsuperuser

# 6️⃣ Run the development server
python3 manage.py runserver
```

---

## 🏗️ Project Structure

project_Grihaloy/
│
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
├── requirements.txt
│
├── grihaloy/ (Container folder)
│   └── grihaloy/ (Actual Django Project folder)
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
│
├── heatmap_service/ (App)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── home/ (App)
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── properties/ (App)
│   ├── migrations/
│   ├── templatetags/
│   │   ├── __init__.py
│   │   └── notif_tags.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── consumers.py
│   ├── forms.py
│   ├── models.py
│   ├── routing.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── users/ (App)
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── media/
│   ├── profile_pics/
│   ├── property_photos/
│   └── default.png
│
├── static/
│   └── images/
│       ├── logo.png
│       └── screenshot.png
│
└── templates/
    ├── base.html
    │
    ├── heatmap_service/
    │   └── heatmap.html
    │
    ├── home/
    │   └── index.html
    │
    ├── properties/
    │   ├── admin_requests_list.html
    │   ├── delete_request_form.html
    │   ├── edit_request_form.html
    │   ├── my_negotiations.html
    │   ├── my_requests.html
    │   ├── negotiation_chat.html
    │   ├── notifications.html
    │   ├── property_confirm_delete.html
    │   ├── property_detail.html
    │   ├── property_form.html
    │   ├── property_list.html
    │   └── property_my_list.html
    │
    └── users/
        ├── login.html
        ├── profile_detail.html
        ├── profile_edit.html
        ├── rating_form.html
        ├── rating_list.html
        ├── register.html
        ├── user_list.html
        ├── verification_form.html
        └── verification_list.html

