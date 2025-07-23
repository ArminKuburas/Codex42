# Codex42
This is going to be a hub of tools or maybe a website of tools I plan to create to help me in my journey at Hive Helsinki.

## Table of Contents
- [XP Calculator](#XP-Calculator)

## XP-Calculator
The XP Calculator is a web application that helps you track your progress in Hive Helsinki's curriculum. It provides the following features:

- Calculate your new level after completing a project
- Create and manage user accounts (locally stored)
- Save project XP values for future reference
- Track your progress over time

### XP Table
The calculator includes the official XP values for levels 0-21, and extrapolated values for levels 22-25.

### Installation and Usage

1. Make sure you have Python and Flask installed:
```bash
pip install flask flask-sqlalchemy
```

2. Run the web application:
```bash
python blackhole_days.py
```

3. Open your browser and navigate to `http://127.0.0.1:5000/`

### Features

#### Calculator Tab
- Input your current level and project XP gain to see your new level
- Select from saved projects to quickly calculate gains

#### Account Tab
- Create a new user account (stored locally)
- Load existing accounts

#### Projects Tab
- Save project names and XP values for future reference
- View all your saved projects
