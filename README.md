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
</p>

---

## 🌆 Overview

**Grihaloy** is a web-based platform that connects landlords and renters in Bangladesh.  
It provides a **streamlined rental process** — from registration to verification — through a secure and modern Django application.

> 🧱 Built with Django and Bootstrap for a clean, responsive experience.

---

## 🖼️ Project Preview

> 📸 Preview of Grihaloy in action:

<p align="center">
  <img src="grihaloy/static/images/screenshot.png" alt="Grihaloy Homepage" width="700"/>
</p>

---

## ✨ Key Features

✅ **User Authentication** — Login, registration, and role-based access (Admin, Landlord, Renter)  
✅ **Document Verification** — Landlords and renters can securely upload verification files  
✅ **Admin Control** — Manage users, roles, and verifications effortlessly  
✅ **Responsive Design** — Powered by Bootstrap 5 for a clean look on any device  
✅ **Future-Ready** — Planned modules for property management, payments, and notifications  

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Backend Framework** | Django 5+ |
| **Language** | Python 3.10+ |
| **Frontend** | HTML5, CSS3, Bootstrap 5 |
| **Database** | SQLite (default) / PostgreSQL (optional) |
| **Authentication** | Django Auth System |

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

