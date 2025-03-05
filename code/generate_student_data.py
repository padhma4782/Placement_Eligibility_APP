import pandas as pd
from faker import Faker
from faker.providers import DynamicProvider
import random
import StudentDatabase as sd
import os
from dotenv import load_dotenv

load_dotenv()
studentdb=None

# Create fake data for india location.
fake = Faker("en_IN")
Faker.seed(0)
random.seed(0)
# Number of records to generate
num_records = 500

Course_provider = DynamicProvider(
     provider_name="student_course",
     elements=["CS", "MS", "AIML", "DS", "SC"],
)

Company_provider = DynamicProvider(
     provider_name="placed_company",
     elements=["TCS", "HCL", "Google", "CTS", "Microsft","Amazon","Capgemini","Accenture"],
)

fake.add_provider(Course_provider)
fake.add_provider(Company_provider)

# Create students data and writes to students_details.csv file.
students_list = []
for _ in range(num_records):
    enrollment_year = int(fake.year())
    students_list.append({
        'StudentID': "ST" + str(fake.unique.random_int(min=111111, max=999999)),
        'Name': fake.name(),
        'Age': random.randint(18, 25),
        'Gender':random.choice(['male', 'female']),
        'ContactNumber': fake.phone_number(),
        'Email': fake.email(),
        'City': fake.city(),
        'EnrollmentYear': enrollment_year,
        'Course_Batch':fake.student_course()+"FT"+str(fake.random_int(min=1, max=10)),
        'GraduationYear':enrollment_year + 1
        
    })
students_df = pd.DataFrame(students_list)

# Create students python programming performance data.
programming_list = []
for student in students_list:
    programming_list.append({
        'ProgrammingID':"PROG" + str(fake.unique.random_int(min=111111, max=999999)),
        'StudentID': student['StudentID'],
        'Language': random.choice(['Python', 'Java','SQL']),
        'ProblemsSolved': random.randint(0, 250),
        'AssessmentsCompleted': random.randint(0, 30),
        'MiniProjects': random.randint(0, 10),
        'Certifications': random.randint(0, 5),
        'Projectscore': random.randint(0, 100)
        
    })
programming_df = pd.DataFrame(programming_list)

# Creates Students soft skills data.
soft_skills_data = []
for student in students_list:
        soft_skills_data.append({
        'SoftSkillID':"SS" + str(fake.unique.random_int(min=111111, max=999999)),
        'StudentID': student['StudentID'],
        'Communication': random.randint(0, 100),
        'Teamwork': random.randint(0, 100),
        'Presentation': random.randint(0, 100),
        'Leadership': random.randint(0, 100),
        'CriticalThinking': random.randint(0, 100),
        'Interpersonalskill': random.randint(0, 100)
        })
soft_skills_df = pd.DataFrame(soft_skills_data)

# Creates students placements readiness data.
placements_data = []
for student in students_list:
    placements_data.append({
        'PlacementID':"PL" + str(fake.unique.random_int(min=111111, max=999999)),
        'StudentID': student['StudentID'],
        'MockInterviewScore': random.randint(1, 10),
        'InternshipCompleted': random.randint(1, 10),
        'PlacementReadiness': random.choice(['Ready', 'Not Ready','Placed']),
        'CompanyName': fake.placed_company()
    })
placements_df = pd.DataFrame(placements_data)

try:
    studentdb=sd.StudentDatabaseManager(os.getenv('MySQL_host'),os.getenv('MySQL_username'),os.getenv('MySQL_password'),os.getenv('MySQL_database'))
except Exception as e:
    print(f"Error connecting to the database: {e}")

studentdb.DBLoader(students_df,programming_df,soft_skills_df,placements_df)