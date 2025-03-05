import streamlit as st
import pandas as pd
import StudentDatabase as sd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from dotenv import load_dotenv

st.title('Placement Eligibility Insights Dashboard')

# Loading variable
load_dotenv()

# Connecting to Database
studentdb=None
try:
    studentdb=sd.StudentDatabaseManager(os.getenv('MySQL_host'),os.getenv('MySQL_username'),os.getenv('MySQL_password'),os.getenv('MySQL_database'))
except Exception as e:
    print(f"Error connecting to the database: {e}")

if studentdb:
# Getting eligibile student list
    st.sidebar.header('Eligibility Criteria')
    problems_solved = st.sidebar.number_input('Minimum Problems Solved', min_value=50,max_value=250, value=50)
    soft_skills_score = st.sidebar.number_input('Minimum Soft Skills Score', min_value=75, max_value=100, value=75)
    query = '''
            SELECT 
            s.StudentID, 
            s.Name, 
            s.Age, 
            s.ContactNumber,
            p.TotalProblemsSolved, 
            ss.AvgSoftSkills
            FROM students s
            JOIN (
                    SELECT 
                    StudentID, 
                    SUM(ProblemsSolved) AS TotalProblemsSolved
                    FROM programming
                    GROUP BY StudentID
                ) p ON s.StudentID = p.StudentID
            JOIN (
                    SELECT 
                    StudentID, 
                    (AVG(Communication) + AVG(Teamwork) + AVG(Presentation) + 
                    AVG(Leadership) + AVG(CriticalThinking) + AVG(InterpersonalSkill)) / 6 AS AvgSoftSkills
                    FROM softskills
                    GROUP BY StudentID
                ) ss ON s.StudentID = ss.StudentID
            WHERE p.TotalProblemsSolved >= %s 
                  AND ss.AvgSoftSkills >= %s; 
            '''
    if st.sidebar.button('Check Eligibility'):
        st.empty()
        st.title('Eligible Students')
        column_names, eligible_students = studentdb.query(query, (problems_solved, soft_skills_score))
        if eligible_students:
            df = pd.DataFrame(eligible_students,columns=column_names)
            st.dataframe(df)
        else:
            st.write('No students meet the eligibility criteria.')
            
# Defining Insights
    insights = ["Select an option","Top 5 Students","Placement Readiness Distribution","Soft Skills Average Scores","Most Popular Programming Languages","Top 5 Coders","Top 5 Interns","Correlation Btw Mock Interview , Internship completed & Readiness","Cities with Most Placed Students","Genderwise Placement Distribution","student placed per graduation year"]
    selected_insight = st.sidebar.selectbox("Select insight", insights)

#Insight1: Top 5 students ready for placement.
    if selected_insight=='Top 5 Students':
        st.subheader('Top 5 Students Ready for Placement')
        top_5_query = '''
                    SELECT  s.StudentID, s.Name, s.ContactNumber
                    FROM Students s
                    JOIN Placements pl ON s.StudentID = pl.StudentID
                    WHERE pl.MockInterviewScore > 8 
                          AND pl.InternshipCompleted >= 1 
                          AND pl.PlacementReadiness = 'Ready'
                    ORDER BY  
                          pl.MockInterviewScore DESC, 
                          pl.InternshipCompleted DESC
                    LIMIT 5;
                  '''
        column_names, top_5_students = studentdb.query(top_5_query)
        
        if top_5_students:
            df_top_5 = pd.DataFrame(top_5_students,columns=column_names)
            #st.table(df_top_5)
            st.dataframe(df_top_5)

#Insight2: Placement Readiness Distribution
    elif selected_insight=='Placement Readiness Distribution':
        st.subheader("Placement Readiness Distribution")
        placement_query="SELECT * FROM placements"
        column_names,placements_details = studentdb.query(placement_query)
        if placements_details:
           placements_df= pd.DataFrame(placements_details,columns=column_names)
           placement_counts = placements_df["PlacementReadiness"].value_counts()
           fig1, ax1 = plt.subplots()
           sns.barplot(x=placement_counts.index, y=placement_counts.values, hue=placement_counts.index, palette="deep",legend=False, ax=ax1)
           ax1.set_xlabel("Placement Readiness")
           ax1.set_ylabel("Number of Students")
           st.pyplot(fig1)
           fig2, ax2 = plt.subplots()
           ax2.pie(placement_counts.values,labels=placement_counts.index,colors=['red','blue','green'],autopct="%1.1f%%")
           st.pyplot(fig2)

#Insight3:  Soft Skills Average Scores
    elif selected_insight == 'Soft Skills Average Scores':
        st.subheader("Soft Skills Average Scores")
        softskill_query = "SELECT * FROM softskills"
        column_names, softskills_data = studentdb.query(softskill_query)
        softskills_df = pd.DataFrame(softskills_data, columns=column_names)
        softskills_avg = softskills_df[["Communication", "Teamwork", "Presentation", "Leadership", "CriticalThinking", "Interpersonalskill"]].mean()
        fig, ax = plt.subplots()
        sns.barplot(x=softskills_avg.index, y=softskills_avg.values,hue=softskills_avg.index, palette="viridis",legend=False, ax=ax)
        ax.set_xlabel("Soft Skills")
        ax.set_ylabel("Average Scores")
        ax.set_xticks(range(len(softskills_avg.index)))
        ax.set_xticklabels(ax.get_xticklabels(), rotation=60)
        st.pyplot(fig)

#Insight4: Most Popular Programming Languages
    elif selected_insight == 'Most Popular Programming Languages':
        st.subheader("Most Popular Programming Languages")
        programming_query="SELECT * FROM programming"    
        column_names, programming_data = studentdb.query(programming_query)
        programming_df = pd.DataFrame(programming_data, columns=column_names)
        top_languages = programming_df["Language"].value_counts()
        fig, ax = plt.subplots()
        sns.barplot(x=top_languages.index, y=top_languages.values,hue=top_languages.index,palette="Blues", ax=ax,legend=False )
        ax.set_xlabel("Programming Language")
        ax.set_ylabel("Number of Students")
        plt.xticks(rotation=45)
        st.pyplot(fig)

#Insight5: Top 5 Students by Problems Solved
    elif selected_insight == 'Top 5 Coders':
        st.subheader("Top 5 Coders")
        coder_query='''SELECT 
                       s.StudentID, 
                       s.Name, 
                       s.ContactNumber,
                       p.TotalProblemsSolved
                       FROM students s
                       JOIN (
                            SELECT 
                                StudentID, 
                                SUM(ProblemsSolved) AS TotalProblemsSolved
                            FROM programming
                            GROUP BY StudentID
                        ) p ON s.StudentID = p.StudentID
                        ORDER BY p.TotalProblemsSolved DESC
                        LIMIT 5;'''
        column_names, coder_data = studentdb.query(coder_query)
        coder_df = pd.DataFrame(coder_data, columns=column_names)      
        st.table(coder_df[["Name", "TotalProblemsSolved"]])

# Insight6: Students with Highest Internship Experience
    elif selected_insight == 'Top 5 Interns':
        st.subheader("Top 5 Interns")
        intern_query='''SELECT s.Name, p.InternshipCompleted 
                        FROM students s
                        JOIN placements p ON s.StudentID = p.StudentID
                        ORDER BY p.InternshipCompleted DESC
                        LIMIT 5;'''
        column_names, intern_data = studentdb.query(intern_query)
        intern_df = pd.DataFrame(intern_data, columns=column_names)  
        st.table(intern_df[["Name", "InternshipCompleted"]])

# Insight7: Correlation Between Mock Interview Score ,Internship completed and Placement Readiness
    elif selected_insight == 'Correlation Btw Mock Interview , Internship completed & Readiness':
        st.subheader("Correlation Btw Mock Interview , Internship completed & Readiness")
        corr_query='''SELECT PlacementReadiness, MockInterviewScore,InternshipCompleted
                        FROM placements;'''
        column_names, corr_data = studentdb.query(corr_query)
        corr_df = pd.DataFrame(corr_data, columns=column_names)
        print(corr_df) 
        fig1, ax1 = plt.subplots()
        sns.lineplot(data=corr_df,x="MockInterviewScore",y="InternshipCompleted",hue="PlacementReadiness",ax=ax1)
        st.pyplot(fig1)

# Insight8: Cities with Most Placed Students
    elif selected_insight == 'Cities with Most Placed Students':
        st.subheader("Cities with Most Placed Students")
        city_query='''SELECT count(*) as Student_count,s.City
                        FROM students s
                        JOIN placements p ON s.StudentID = p.StudentID
                        Where p.PlacementReadiness="Placed"
                        Group By s.City
                        ORDER BY  Student_count desc
                        Limit 10; '''
        
        column_names, city_data = studentdb.query(city_query)
        city_df = pd.DataFrame(city_data, columns=column_names)        
        fig, ax = plt.subplots()
        sns.barplot(x=city_df['City'], y=city_df['Student_count'], ax=ax, palette="magma")
        plt.xticks(rotation=60)
        st.pyplot(fig)

#Insight9: Genderwise Placement Distribution
    elif selected_insight=='Genderwise Placement Distribution':
        st.subheader("Genderwise Placement Distribution")
        gender_query='''SELECT s.gender 
					  FROM students s, placements p 
					  WHERE s.studentid=p.studentid
					  and p.PlacementReadiness="Placed"
                      '''
        column_names,gender_details = studentdb.query(gender_query)
        if gender_details:
           gender_df= pd.DataFrame(gender_details,columns=column_names)
           gender_counts = gender_df["gender"].value_counts()
           fig1, ax1 = plt.subplots()
           ax1.pie(gender_counts.values,labels=gender_counts.index,colors=['pink','green'],autopct="%1.1f%%")
           st.pyplot(fig1)

#Insight10: student placed per graduation year
    elif selected_insight == 'student placed per graduation year':
        st.subheader("student placed per graduation year")
        grad_query='''SELECT count(*) as student_count, s.GraduationYear
                     FROM students s
                     JOIN placements p on  s.StudentID=p.StudentID
                     WHERE p.PlacementReadiness="Placed" and
                           s.GraduationYear >= 2016 
                     GROUP BY s.GraduationYear
                     ORDER BY s.GraduationYear asc'''
        column_names, grad_data = studentdb.query(grad_query)
        grad_df = pd.DataFrame(grad_data, columns=column_names)
        fig1, ax1 = plt.subplots()
        sns.scatterplot(grad_df,x="GraduationYear",y = "student_count",ax=ax1)
        st.pyplot(fig1)
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=grad_df,x="GraduationYear",y="student_count",ax=ax2)
        st.pyplot(fig2)
# Close the db connection
studentdb.close()