# Placement_Eligibility_APP
This project is to Design and implement a Streamlit application where users can input eligibility criteria for placement. Based on these criteria, the application should query a dataset of student information to display eligible candidates' details and there are options to generate insights.

Features

Student Data Management: Store and manage student details using MYSQL.

placement_eligibility_checker: Placement team can input eligibility criteria for placement. Based on these criteria, the application queries a dataset of student information to display eligible candidates' details and there are options to generate valuable insights using Seaborn & Matplotlib.
 
Tech Stack
Backend: Python, MySQL
Frontend: Streamlit
Data Visualization: Matplotlib, Seaborn

Folder Structure
📦 Placement-Eligibility-App

├── 📂 code                # Python scripts for analysis and app
├── 📜 .env                # environment variables
└── 📜 README.md           # Project documentation

Setup
Create student_database with students,placements,programming and softskills table.


Run the Application: 
streamlit run code\placement_eligibility_checker.py reload

