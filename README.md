# Field Data Collection & Sync App

## Overview

This is a **Flask-based web application** for collecting, managing, and syncing agricultural research data. Researchers can fill in structured forms (Agronomic, Disease, Growth, Yield, etc.), store them locally in a database, and then sync them to a **Google Sheets spreadsheet** for cloud storage, collaboration, and backup.

The app ensures **duplicate-free syncing**: once a record is exported to Google Sheets, it is marked as synced and won’t be exported again.

---

## Features

- **Dashboard**

  - Displays total counts of records per form.
  - Shows the most recent entries.
  - Provides a **Sync button** when unsynced records exist.

- **Form Collection**

  - Eight structured forms for different data categories:
    - Agronomic & Morphological
    - Disease
    - Field Conditions
    - Greenhouse Conditions
    - Growth (Field)
    - Growth (Greenhouse)
    - Yield (Field)
    - Yield (Greenhouse)
  - Multi-step input forms with validation.

- **Data Storage**

  - Records stored locally in a **SQLite database** (`app.sqlite`).
  - Each record includes a `synced` flag (`True/False`).

- **Google Sheets Sync**
  - Records exported to a shared Google Sheet.
  - Each form syncs to its own worksheet/tab.
  - Headers automatically created if missing.
  - Duplicate checks prevent re-adding the same record.
  - After syncing, records are marked as `synced=True` in the database.

---

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** SQLAlchemy + SQLite (default, extendable to Postgres/MySQL)
- **Frontend:** Jinja2 templates + Bootstrap 5 + custom JS
- **Sync:** Google Sheets API (`gspread` + `oauth2client`)

---

## File Structure

install package

pyinstaller -w -F --onefile ^
--add-data "templates;templates" ^
--add-data "static;static" ^
--add-data "instance/app.sqlite;instance" ^
--add-data "config.py;." ^
--add-data "credentials.json;." ^
app.py
