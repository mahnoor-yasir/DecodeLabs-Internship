# Enterprise Personal Finance Management System

## Overview

The Enterprise Personal Finance Management System is a professional desktop-based expense management application developed in Python using the Tkinter GUI framework. It is designed to help users efficiently record, organise, analyse, and manage their daily financial transactions through a clean and interactive graphical interface.

Unlike a basic expense calculator, this application provides a complete personal finance management environment where users can maintain expense records, organise custom categories, monitor monthly budgets, analyse spending behaviour, export financial data, and securely store information using JSON-based persistence.

The project demonstrates practical implementation of desktop application development, object-oriented programming, CRUD operations, data management, file handling, budget analysis, statistical reporting, and responsive GUI design. Every module has been designed to simulate the functionality of a lightweight personal finance management system suitable for students, professionals, and individual users.

The application focuses on improving financial awareness by providing organised expense tracking, real-time budget monitoring, searchable transaction history, editable financial records, and detailed statistical summaries.

---

# Project Objectives

The primary objectives of this project are:

- Develop a professional desktop application using Python.
- Simplify personal expense recording and management.
- Maintain organised financial records.
- Monitor monthly budgets and spending habits.
- Provide detailed expense analysis.
- Allow users to customise expense categories.
- Demonstrate practical implementation of Python GUI programming.
- Implement secure local data storage using JSON.
- Perform CRUD (Create, Read, Update and Delete) operations efficiently.
- Export financial records for future use.
- Build a project suitable for academic submission and professional portfolio presentation.

---

# Key Features

## Welcome Dialog

The application begins with a personalised welcome dialog where the user enters their name before accessing the main dashboard. This creates a customised user experience and displays a personalised greeting throughout the application.

### Functions

- User name input
- Personalised welcome message
- Simple application initialisation

---

## Dashboard & Ledger

The Dashboard acts as the central workspace of the application.

It displays all recorded financial transactions inside a structured table while allowing users to perform complete expense management operations from a single interface.

The dashboard also displays important financial information including:

- Today's Total Spending
- Current Month Spending
- Remaining Monthly Budget

Every expense record contains detailed information including:

- Expense ID
- Amount
- Category
- Sub Category
- Payment Method
- Date
- Time
- Location
- Tags
- Description

The ledger automatically updates whenever records are added, edited or removed.

---

## Expense Management

Users can record complete expense information using the input panel available on the left side of the dashboard.

Each expense includes:

- Amount
- Category
- Sub Category
- Payment Method
- Description
- Location
- Tags

The application validates user input before saving the record and automatically generates a unique Expense ID.

---

## Edit Expense

Existing expense records can be modified without deleting them.

The edit module allows users to:

- Update expense amount
- Modify expense description
- Save updated information instantly

This ensures financial records remain accurate while preserving existing entries.

---

## Delete Expense

The application includes a secure delete confirmation system.

Before permanently deleting any expense, a confirmation dialog appears asking the user to verify the action.

This prevents accidental deletion of financial records.

---

## Search Records

The built-in search functionality enables users to quickly locate transactions.

Users can search records using keywords related to:

- Category
- Description
- Location
- Payment Method
- Tags

Search results are filtered instantly without affecting the stored data.

---

## Category Management

The application allows users to manage their own expense categories instead of relying only on predefined options.

Users can:

- Create new categories
- Expand expense organisation
- Improve financial classification

This feature makes the application flexible for different users and spending habits.

---

## Budget Manager

The Budget Manager helps users monitor their monthly spending.

Users can define a monthly spending limit, after which the application automatically calculates:

- Total Budget
- Total Spent
- Remaining Budget
- Budget Usage Percentage

A visual progress indicator provides a quick understanding of current spending behaviour.

---

## Statistics & Reports

The Statistics module performs automatic financial analysis using all stored expense records.

The generated report includes:

- Total Cumulative Spending
- Average Expense
- Highest Expense
- Lowest Expense
- Top Spending Category
- Total Number of Entries
- Category-wise Expense Breakdown
- Spending Percentage
- Expense Distribution

This helps users understand their financial habits through organised statistical summaries.

---

## Settings & Data Management

The Settings module provides user profile and data management options.

Available features include:

- Update User Name
- Change Active Currency
- Export Records to CSV
- Create Backup Files

This section centralises important application settings while improving data portability.

---

## Currency Selection

Users can change the preferred currency used throughout the application.

Supported currencies include:

- PKR
- USD
- EUR
- AED

This improves flexibility for users managing expenses in different currencies.

---

## Data Persistence

All financial records are automatically stored locally using JSON files.

The application preserves:

- Expense Records
- Categories
- Budget Information
- User Settings

Data remains available even after closing and reopening the application.

---

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python 3 | Core Programming Language |
| Tkinter | Graphical User Interface |
| JSON | Local Data Storage |
| CSV | Export Financial Records |
| Datetime | Date & Time Management |
| OS Module | File & Folder Management |

---

# Application Workflow

The application follows the workflow below:

1. Launch the application.
2. Enter user name through the Welcome Dialog.
3. Access the main dashboard.
4. Record daily expenses.
5. Organise expenses using categories and subcategories.
6. Search existing records whenever required.
7. Edit or delete existing transactions.
8. Monitor monthly budget usage.
9. Generate financial statistics.
10. Export records or create backups.
11. Save all information automatically using JSON storage.

---

# Screenshots

## Welcome Dialog

The application begins with a personalised welcome screen where the user enters their name before accessing the main system.

![Welcome Dialog](assets/images/Welcome%20Dialog.png)

---

## Main Dashboard

The main dashboard serves as the central workspace for recording expenses, viewing transactions, monitoring budget information, and managing financial records.

![Main Dashboard](assets/images/Main%20Dashboard.png)

---

## Search Record

The search functionality allows users to quickly locate expense records using keywords such as category, location, payment method, or description.

![Search Record](assets/images/Search%20Record.png)

---

## Edit Expense

Users can modify existing expense records by updating important information such as amount and description without deleting the original record.

![Edit Expense](assets/images/Edit%20Expense.png)

---

## Delete Confirmation

Before deleting an expense record, the application displays a confirmation dialog to prevent accidental data loss.

![Delete Confirmation](assets/images/Delete%20Confirmation.png)

---

## Sub Category Dropdown

The application dynamically updates available subcategories based on the selected expense category, improving organisation and usability.

![Sub Category Dropdown](assets/images/Sub%20Category%20Dropdown.png)

---

## Statistics Report

The statistical reporting module generates detailed financial summaries, spending analysis, category-wise distributions, averages, and overall expense insights.

![Statistics Report](assets/images/Statistics%20Report.png)

---

## Budget Manager

The Budget Manager enables users to set monthly spending limits while continuously tracking total spending, remaining balance, and budget utilisation.

![Budget Manager](assets/images/Budget%20Manager.png)

---

## Category Manager

Users can create and manage custom expense categories to better organise personal financial records according to their own requirements.

![Category Manager](assets/images/Category%20Manager.png)

---

## Settings Panel

The Settings module provides options for updating user information, selecting currencies, exporting financial records, and creating backup files.

![Settings Panel](assets/images/Settings%20Panel.png)

---

## Currency Selection

Users can switch between multiple supported currencies for displaying financial information throughout the application.

![Currency Selection](assets/images/Currency%20Selection.png)

---
# Core Modules

The application is organised into multiple functional modules that work together to provide a complete expense management solution.

---

## User Profile Module

This module personalises the application by allowing users to enter and update their profile name. The entered name is displayed throughout the application, creating a customised user experience.

### Responsibilities

- Store user name
- Display personalised greeting
- Update profile information
- Save user preferences

---

## Expense Recording Module

The Expense Recording Module is responsible for creating new financial records.

Users can enter complete expense information including amount, category, payment method, location, tags, and descriptions.

Every record is automatically assigned a unique Expense ID along with the current date and time.

### Responsibilities

- Create expense entries
- Generate unique Expense IDs
- Validate user input
- Save records automatically

---

## Ledger Management Module

The Ledger Module displays all financial transactions inside a structured table.

It allows users to monitor, organise, and review all expense records from a single interface.

### Responsibilities

- Display expense history
- Organise records
- Refresh data automatically
- Maintain transaction consistency

---

## Search Module

The Search Module enables users to instantly locate expense records without manually browsing the ledger.

Filtering occurs dynamically as search keywords are entered.

### Search Criteria

- Category
- Description
- Location
- Tags
- Payment Method

---

## Category Management Module

Instead of limiting users to predefined expense categories, the application allows creation of additional categories according to personal requirements.

This increases flexibility while improving financial organisation.

### Functions

- Add new categories
- Store categories
- Update category list
- Populate category dropdowns

---

## Budget Monitoring Module

The Budget Module continuously monitors spending against the monthly budget defined by the user.

Budget information updates automatically whenever a new expense is recorded.

### Displays

- Monthly Budget
- Current Spending
- Remaining Budget
- Budget Usage Percentage

A graphical progress indicator provides a quick visual representation of spending progress.

---

## Statistics Module

The Statistics Module analyses stored financial records and generates a complete statistical report.

It calculates multiple financial indicators that help users understand their spending behaviour.

### Generated Information

- Total Expenses
- Average Expense
- Highest Expense
- Lowest Expense
- Total Entries
- Category Distribution
- Spending Percentage
- Largest Spending Category

---

## Settings Module

The Settings Module manages user preferences and application configuration.

Users can customise application settings without modifying the program source code.

### Available Settings

- User Profile Name
- Active Currency
- CSV Export
- Backup Creation

---

## Export Module

The Export Module enables users to save financial records outside the application.

Currently supported format:

- CSV

Exported files can be opened using Microsoft Excel, Google Sheets, LibreOffice Calc, and other spreadsheet software.

---

## Backup Module

The Backup Module allows users to create copies of their financial records.

This helps prevent accidental data loss and enables recovery when required.

---

# Data Storage

The application stores information locally using JSON files.

This approach removes the need for an external database while ensuring that all financial records remain available after restarting the application.

Stored information includes:

- Expense Records
- Categories
- Budget Information
- User Profile
- Application Settings

The application automatically loads existing data during startup and saves updates whenever changes are made.

---

# Input Validation

To improve reliability and minimise user errors, the application validates entered information before processing any request.

Validation includes:

- Empty field detection
- Invalid numeric input prevention
- Required field verification
- Record selection validation before editing
- Record selection validation before deletion

These checks help maintain accurate and consistent financial records.

---

# Key Learning Outcomes

This project demonstrates practical implementation of:

- Desktop GUI Development
- Object-Oriented Programming
- Event-Driven Programming
- CRUD Operations
- File Handling
- JSON Data Persistence
- CSV Export
- Financial Record Management
- Budget Tracking
- Statistical Analysis
- User Input Validation
- Multi-Tab Interface Design
- Responsive Desktop Application Development

---

# Project Highlights

This application demonstrates the practical implementation of several software engineering concepts within a single desktop application.

Highlights include:

- Professional multi-tab graphical user interface
- Personalised user experience
- Complete expense recording system
- Real-time budget monitoring
- Dynamic category management
- Advanced search functionality
- Editable transaction records
- Secure deletion confirmation
- Automatic statistical reporting
- JSON-based persistent storage
- CSV export capability
- Modular and maintainable application structure

---

# Author

**Mahnoor Yasir**

BS Computer Science

Python Programming Internship

---

# Acknowledgements

This project was developed as part of a Python Programming Internship to demonstrate practical knowledge of Python desktop application development, graphical user interface design, data management, and software engineering principles.

---

# License

This project is intended for educational purposes, portfolio demonstration, and internship submission. It may be used as a reference for learning desktop application development using Python and Tkinter.
