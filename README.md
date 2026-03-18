# Beauty Salon Management System for Odoo 19

## Overview
The **Beauty Salon Management** module is a comprehensive, fully-functional Odoo 19 application designed to automate the daily operations of beauty salons, barbershops, and SPAs. It provides a seamless experience for managing appointments, clients, masters, and financial reporting.

## Key Features

### 📅 Smart Scheduling & Appointments
* **Visual Calendar:** An intuitive calendar view for booking and managing appointments.
* **Double-Booking Prevention:** Built-in Python constraints physically prevent booking two clients with the same master at overlapping times.
* **Auto-Duration Calculation:** The system automatically calculates the end time of an appointment based on the selected services.

### 👥 User & Catalog Management
* **Client Database:** Tracks visit history, contact details, and calculates the "Last Visit" date automatically.
* **Master Profiles:** Manages specialists, their specific services, contacts, and personal bonus percentages (commission).
* **Service Pricelist:** Easy-to-manage catalog of services with fixed prices and durations.

### 💰 Financials & Reporting
* **Payroll Automation:** Calculates the master's bonus for each completed appointment.
* **Wizard & PDF Reports:** Includes a custom Wizard to select a date range and generates a professional PDF report for payroll processing.
* **Analytics:** Interactive Pivot tables and Graphs for analyzing total revenue and master performance over time.

### ⚙️ Automation & Security
* **Automated Reminders (CRON):** A scheduled action runs daily to find clients who haven't visited in over 30 days and automatically creates a "To-Do" activity for the administrator to call them.
* **Role-Based Access Control (RBAC):** * **Manager:** Full access to all records, financial reports, and system settings.
  * **Master:** Restricted access. Can only view and edit their *own* appointments and read basic catalogs (services, clients).

## Installation
1. Clone or download this repository into your Odoo `addons` directory.
2. Ensure you have the `mail` and `calendar` core modules installed in your database.
3. Restart the Odoo server.
4. Enable "Developer Mode" and click "Update Apps List".
5. Search for "Beauty Salon" and click **Activate**.

## Configuration
* **Access Rights:** Go to `Settings -> Users & Companies -> Users`. Select a user and assign the appropriate role (Master or Manager) under the "Beauty Salon" category.
* **Scheduled Actions:** The CRON job for client reminders is installed automatically. You can manually trigger it via `Settings -> Technical -> Scheduled Actions` by searching for "Beauty Salon Reminder".

## Author
* Developed by **Vitaliy** as a comprehensive project demonstrating advanced Odoo 19 framework capabilities.