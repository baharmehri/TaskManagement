# Task Management

This project provides a simple user authentication system with registration, login via password or OTP, and basic task
management functionality. Users can create, read, update, and delete tasks through a straightforward CRUD interface.
Ideal for learning the fundamentals of user authentication and task management.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Deployment](#deployment)

## Features

- **Password and OTP Login:** Supports secure user authentication through both password and One-Time Password (OTP)
  methods.
- **Asynchronous OTP Handling:** Uses Celery for the asynchronous generation and sending of OTPs, ensuring efficient and
  reliable delivery.
- **OTP Queue Management:** Utilizes RabbitMQ for queuing and distributing OTPs, enabling scalable and resilient OTP
  processing.
- **OTP Caching:** Employs Redis to cache OTPs, optimizing verification speed and reducing redundant OTP generation.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.10+** installed on your machine.
- **Virtualenv** or another method for managing virtual environments.
- **Docker** and **Docker Compose**.

## Installation

### 1. Clone the Repository

```bash
git clonehttps://github.com/baharmehri/TaskManagement.git
cd TaskManagement
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements/requirements.txt
```

## Environment Variables

Create a .env file in the project root directory and add the required environment.
You can copy the .env.example file:

```bash
cp .env.example .env
```

## Database Migrations

Apply the migrations to set up your database schema:

```bash
python manage.py migrate
```

## Deployment

To deploy the Notification Service using Docker Compose, run this:

```bash
docker compose up --build -d
```