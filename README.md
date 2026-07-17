# 🧘‍♀️ Yoga Booking Telegram Bot

A Python-based Telegram bot that automates online session bookings for a yoga studio and syncs user data.

---

## ✨ Features

* **Online Booking:** Step-by-step user scenario to select a time and book a yoga practice.
* **Sheets Integration:** Automated data logging and user management via `sheets.py`.
* **Interactive Menu:** Intuitive custom keyboard layouts for smooth navigation.

---

## 💻 Project Architecture

The codebase follows a modular structure for easy future scaling:
* `main.py` — Entry point to launch the bot.
* `handlers.py` — User message and command processing.
* `keyboards.py` — Custom interface buttons.
* `states.py` — Finite State Machine (FSM) configurations for the booking flow.
* `sheets.py` — Database and table management logic.
* `config.py` — Core bot configuration and environment setup.
