# KnowledgeHub
## Enterprise General Knowledge Quiz

An enterprise-grade desktop quiz application developed using **Python**, **Tkinter**, and **SQLite**. The application provides a modern graphical interface for conducting category-based quizzes with multiple difficulty levels, countdown timers, analytics, leaderboard management, question management, and report exporting.

Developed as part of the **Decode Labs Python Programming Internship**, this project demonstrates practical implementation of Python GUI development, object-oriented programming, database integration, data management, and desktop application development.

---

# Overview

KnowledgeHub is a desktop-based General Knowledge Quiz System designed to provide an engaging and professional quiz experience. Users can participate in quizzes from different categories, select difficulty levels, monitor their performance, and review analytical statistics through an enterprise-style interface.

The application includes:

- Category-based quizzes
- Multiple difficulty levels
- Countdown timer
- Automatic score calculation
- Performance grading
- Statistics dashboard
- Leaderboard management
- SQLite database integration
- Question and category management
- Theme switching
- CSV and TXT report export

The project follows a modular architecture and stores all quiz data locally using SQLite.

---

# Project Information

| Property | Value |
|----------|-------|
| **Project Name** | KnowledgeHub |
| **Application** | Enterprise General Knowledge Quiz |
| **Programming Language** | Python 3 |
| **GUI Framework** | Tkinter |
| **Database** | SQLite3 |
| **Chart Library** | Matplotlib |
| **Architecture** | Modular |
| **Version** | v4.0.0 |
| **Platform** | Windows Desktop |
| **Internship** | Decode Labs Python Programming Internship |

---

# Features

## Quiz System

- Interactive Multiple Choice Questions (MCQs)
- Dynamic Question Loading
- Random Question Selection
- Category-Based Quiz Sessions
- Difficulty-Based Quiz Sessions
- Countdown Timer
- Automatic Score Calculation
- Performance Summary
- Grade Calculation
- Accuracy Percentage
- Time Tracking

---

## Quiz Categories

The application currently supports:

- General Knowledge
- Science
- Technology
- History
- Geography
- Sports
- Python
- Mixed

Additional categories can be added through the Admin Portal.

---

## Difficulty Levels

Users can choose their preferred difficulty before starting the quiz.

Available difficulty levels:

- Easy
- Medium
- Hard
- Expert

Each level provides a different challenge and timer configuration.

---

## Statistics Dashboard

The analytics module provides:

- Total Sessions Played
- Highest Score
- Average Accuracy
- Category-wise Attempts
- Performance Charts
- Analytical Metrics

---

## Leaderboard

The Leaderboard module includes:

- Player Name
- Quiz Category
- Final Score
- Accuracy Percentage
- Grade
- Individual Record Deletion
- Result Management

---

## Admin Portal

The administrator module allows users to:

- Create New Categories
- Add New Questions
- Select Correct Answers
- Assign Difficulty Levels
- Add Question Explanations
- Save Questions into the SQLite Database

---

## Report Export

Quiz reports can be exported in:

- CSV Format
- TXT Format

Each report includes:

- Player Name
- Category
- Score
- Accuracy
- Grade
- Time Taken

---

## User Interface

The application features:

- Professional Dashboard
- Responsive Desktop Interface
- Dark Theme
- Light Theme
- Sidebar Navigation
- Modern Layout
- Clean Typography
- Enterprise Design

---

# Technologies Used

| Technology | Purpose |
|------------|----------|
| Python 3 | Programming Language |
| Tkinter | GUI Development |
| SQLite3 | Local Database |
| Matplotlib | Statistics Charts |
| CSV | Report Export |
| OS | File Management |
| Pathlib | Directory Management |
| Logging | Application Logging |
| Time | Quiz Timer |
| Random | Random Question Selection |

---

# Requirements

Before running the application, ensure the following are installed:

- Python 3.10 or later

Required libraries:

- tkinter
- sqlite3
- matplotlib
- csv
- pathlib
- random
- logging
- os
- time

Most of these libraries are included with the standard Python installation.

---

# Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/mahnoor-yasir/DecodeLabs-Internship.git
```

### Step 2: Navigate to the Project Folder

```bash
cd "Project 4 General Knowledge Quiz"
```

### Step 3: Install Required Library

```bash
pip install matplotlib
```

### Step 4: Run the Application

```bash
python main.py
```

The KnowledgeHub desktop application will launch automatically.
---
# Application Workflow

The application follows a structured workflow to provide a smooth quiz experience.

### Step 1: Launch Application

Run the application using:

```bash
python main.py
```

The Dashboard window is displayed.

---

### Step 2: Enter Player Information

The user enters:

- Player Name
- Quiz Category
- Difficulty Level

---

### Step 3: Start Quiz

After clicking **Initialize 10-MCQ Quiz Session**, the system:

- Loads questions from the SQLite database
- Filters questions based on the selected category
- Randomly selects ten questions
- Starts the countdown timer

---

### Step 4: Answer Questions

During the quiz, users can:

- Read each question
- Select one option
- View remaining time
- Submit their answer
- Move to the next question

---

### Step 5: Performance Evaluation

After completing all questions, the application calculates:

- Total Score
- Accuracy Percentage
- Grade
- Time Taken

A detailed Performance Summary is displayed.

---

### Step 6: Store Results

Quiz results are automatically stored inside the SQLite database for future analysis.

---

### Step 7: View Leaderboard

The Leaderboard displays:

- Player Name
- Quiz Category
- Score
- Accuracy
- Grade

Users can also delete individual records if required.

---

### Step 8: View Statistics

The Statistics Dashboard provides analytical information including:

- Sessions Played
- Highest Score
- Average Accuracy
- Category-wise Attempts

---

### Step 9: Export Reports

Users can export quiz reports in:

- CSV Format
- TXT Format

---

### Step 10: Manage Questions

Using the Admin Portal, administrators can:

- Create Categories
- Add Questions
- Add Options
- Select Correct Answers
- Assign Difficulty
- Save Questions to the Database

---

# Database Design

The application uses **SQLite3** for local data storage.

The database stores:

## Quiz Questions

- Question ID
- Category
- Question Statement
- Option A
- Option B
- Option C
- Option D
- Correct Answer
- Difficulty
- Explanation

---

## Quiz Results

- Result ID
- Player Name
- Category
- Score
- Accuracy
- Grade
- Time Taken
- Date and Time

---

## Categories

- Category ID
- Category Name

---

# Project Modules

The application consists of several independent modules.

## Dashboard

Responsible for:

- Player Registration
- Category Selection
- Difficulty Selection
- Quiz Initialization

---

## Quiz Engine

Handles:

- Question Loading
- Random Question Selection
- Countdown Timer
- Answer Validation
- Score Calculation

---

## Performance Summary

Displays:

- Final Grade
- Final Score
- Accuracy Percentage
- Time Taken

---

## Leaderboard

Responsible for:

- Viewing Previous Results
- Managing Stored Records
- Deleting Individual Entries

---

## Statistics Dashboard

Provides:

- Performance Analytics
- Highest Score
- Average Accuracy
- Category-wise Statistics

---

## Admin Portal

Allows administrators to:

- Create Categories
- Add Questions
- Assign Difficulty Levels
- Save Questions into the Database

---

## Settings

Provides:

- Dark Theme
- Light Theme

---

# Report Export

The application automatically generates professional reports after quiz completion.

Supported formats include:

- CSV
- TXT

Each exported report contains:

- Player Name
- Category
- Final Score
- Accuracy
- Grade
- Time Taken

Reports are saved inside the **exports** directory for future reference.

---
# Application Screenshots

## 01. Home Dashboard

The main dashboard where users enter their name, select a quiz category and difficulty level, and initialize a new quiz session.

![Home Dashboard](assets/images/01.%20Home%20Dashboard.png)

---

## 02. Category Selection

Users can select a preferred quiz category from multiple available domains including General Knowledge, Science, Technology, History, Sports, Geography, Python, and Mixed.

![Category Selection](assets/images/02.%20Category%20Selection.png)

---

## 03. Difficulty Selection

The application provides four difficulty levels: Easy, Medium, Hard, and Expert. Each difficulty configures the quiz timer accordingly.

![Difficulty Selection](assets/images/03.%20Difficulty%20Selection.png)

---

## 04. Quiz Interface

Interactive multiple-choice quiz interface displaying the current question, available options, countdown timer, and quiz progress.

![Quiz Interface](assets/images/04.%20Quiz%20Interface.png)

---

## 05. Quiz in Progress

Users continue answering randomly selected questions while the application automatically evaluates responses and tracks progress.

![Quiz in Progress](assets/images/05.%20Quiz%20In%20Progress.png)

---

## 06. Performance Summary

After completing the quiz, the application displays a detailed performance summary including final score, grade, accuracy percentage, and total time taken.

![Performance Summary](assets/images/06.%20Performance%20Summary.png)

---

## 07. Global Leaderboard

Displays all previous quiz attempts with player information, score, category, percentage, and grade.

![Global Leaderboard](assets/images/07.%20Global%20Leaderboard.png)

---

## 08. Delete Result Confirmation

Confirmation dialog displayed before permanently removing a selected quiz result from the leaderboard.

![Delete Result Confirmation](assets/images/08.%20Delete%20Result%20Confirmation.png)

---

## 09. Result Deleted Successfully

Success notification displayed after deleting the selected leaderboard record from the database.

![Result Deleted Successfully](assets/images/09.%20Result%20Deleted%20Successfully.png)

---

## 10. Updated Leaderboard

The leaderboard automatically refreshes after deletion to display the latest available quiz records.

![Updated Leaderboard](assets/images/10.%20Updated%20Leaderboard.png)

---

## 11. Statistics Dashboard

Displays analytical metrics including total quiz sessions, average accuracy, highest score, and category-wise performance using graphical visualization.

![Statistics Dashboard](assets/images/11.%20Statistics%20Dashboard.png)

---

## 12. System Preferences

Allows users to switch between Dark Mode and Light Mode, providing a customizable user interface.

![System Preferences](assets/images/12.%20System%20Preferences.png)

---

## 13. Question & Category Creator Portal

Administrative interface used to create new quiz categories and add multiple-choice questions directly into the SQLite database.

![Question & Category Creator Portal](assets/images/13.%20Question%20%26%20Category%20Creator%20Portal.png)

---

## 14. New Question Added Successfully

Confirmation message displayed after successfully saving a newly created question into the selected quiz category.

![New Question Added Successfully](assets/images/14.%20New%20Question%20Added%20Successfully.png)

---

# Learning Outcomes

This project demonstrates practical understanding of:

- Python Programming
- Desktop GUI Development using Tkinter
- Object-Oriented Programming
- SQLite Database Integration
- CRUD Operations
- Event-Driven Programming
- File Handling
- Exception Handling
- Report Generation
- Data Analytics
- Modular Programming
- Software Architecture
- User Interface Design
- Desktop Application Development

---

# Project Highlights

- Enterprise-style Desktop Application
- Modern Tkinter User Interface
- SQLite Database Integration
- Multiple Quiz Categories
- Multiple Difficulty Levels
- Dynamic Question Loading
- Random Question Selection
- Countdown Timer
- Automatic Score Calculation
- Performance Grading System
- Statistics Dashboard
- Leaderboard Management
- Individual Result Deletion
- Admin Portal
- Question & Category Management
- CSV Report Export
- TXT Report Export
- Dark & Light Theme Support
- Modular Project Architecture
- Pure Python Implementation

---

# Author

**Mahnoor Yasir**

**BS Computer Science**

**Decode Labs Python Programming Internship**

GitHub: https://github.com/mahnoor-yasir

LinkedIn: https://www.linkedin.com/in/mahnoor-yasir

---

# License

This project has been developed for educational and internship purposes as part of the Decode Labs Python Programming Internship.

It may be used for learning, academic reference, and portfolio demonstration.

---

# Acknowledgements

Special thanks to:

- Decode Labs
- Python Software Foundation
- Tkinter Development Team
- SQLite Development Team
- Open Source Community

for providing the tools and technologies that made this project possible.

---

## If you found this project useful, consider giving it a star on GitHub.
