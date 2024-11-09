# Importing necessary modules
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import openpyxl
import io
import base64
import time
import math

st.set_page_config(page_title='Performance Tracker V1')
st.header(' Insight Spark 📈')
st.write('Analyse Student Performance in real time')


# File upload
fileupload = st.file_uploader('Please upload your file here', type='XLSX')

# File uploading conditioning
if fileupload is None:
    st.info('Please upload the file to analyze the data')
else:
    try:
        df = pd.read_excel(fileupload, engine='openpyxl')
        st.success('Data uploaded successfully')

        # Input of the roll number
        roll_num = st.number_input("Please enter the student's roll number")

        if roll_num in df['Roll Number'].values:
            with st.spinner(text=' Searching '):
                time.sleep(1)
                st.success(' Roll number data present ')

            # Extracting the roll number data
            selectedroll = df[df['Roll Number'] == roll_num]

            # Subject selection
            selection = st.multiselect('Choose subjects to visualise',
                                      ('English', 'Physics', 'Mathematics', 'Chemistry', 'Optional'))

            validselection = [selection for subject in selection if subject in df.columns]
            if validselection:
                studentname = selectedroll['Name'].values[0]
                splitname = studentname.split()[0]
                st.write(f"{studentname} performance in selected subjects")

                # Create a dataframe for the selected subjects
                student_performance = selectedroll[selection].T
                student_performance.columns = ['Marks']
                student_performance['Marks'] = student_performance['Marks'].astype(float)
                student_performance['Subjects'] = student_performance.index

                # Enhanced Bar Chart
                bar_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
                fig = px.bar(student_performance, x='Subjects', y='Marks', color='Marks',
                             color_continuous_scale=bar_colors, title=f"{studentname}'s Performance in Selected Subjects")

                fig.update_layout(
                    xaxis_title="Subjects",
                    yaxis_title="Marks",
                    yaxis=dict(range=[0, 100]),
                    width=800,
                    height=500,
                    coloraxis_showscale=False
                )
                st.plotly_chart(fig)

                # Radar Chart for Performance Comparison
                fig_radar = go.Figure()

                fig_radar.add_trace(go.Scatterpolar(
                    r=student_performance['Marks'],
                    theta=student_performance['Subjects'],
                    fill='toself',
                    name='Marks',
                    line=dict(color='blue')
                ))

                fig_radar.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    title=f"{studentname}'s Performance Radar Chart"
                )
                st.plotly_chart(fig_radar)

                strongestsubject = student_performance['Marks'].idxmax()
                weakestsubject = student_performance['Marks'].idxmin()
                strongestsubject_marks = student_performance.loc[strongestsubject, 'Marks']
                weakestsubject_marks = student_performance.loc[weakestsubject, 'Marks']

                # Calculate class average
                class_average_strongest = df[strongestsubject].mean()
                class_average_weakest = df[weakestsubject].mean()

                # Data for strongest subject
                strongest_subject_data = {
                    'Type': ['Student', 'Class Average'],
                    'Score': [strongestsubject_marks, class_average_strongest]
                }

                # Data for weakest subject
                weakest_subject_data = {
                    'Type': ['Student', 'Class Average'],
                    'Score': [weakestsubject_marks, class_average_weakest]
                }

                # Convert to DataFrame for Plotly
                df_strongest = pd.DataFrame(strongest_subject_data)
                df_weakest = pd.DataFrame(weakest_subject_data)

                # Enhanced Comparison Chart
                fig_comparison = make_subplots(rows=1, cols=2, subplot_titles=(f"Strongest Subject: {strongestsubject}", f"Weakest Subject: {weakestsubject}"))

                fig_comparison.add_trace(go.Bar(
                    x=df_strongest['Type'],
                    y=df_strongest['Score'],
                    name=strongestsubject,
                    marker_color='blue'
                ), row=1, col=1)

                fig_comparison.add_trace(go.Bar(
                    x=df_weakest['Type'],
                    y=df_weakest['Score'],
                    name=weakestsubject,
                    marker_color='red'
                ), row=1, col=2)

                fig_comparison.update_layout(height=600, width=800, title_text="Performance Comparison")
                st.plotly_chart(fig_comparison)

                # Adding a pie chart for better analysis
                pie = px.pie(values=student_performance['Marks'],
                             names=student_performance['Subjects'],
                             title=f"{splitname} performance share")
                st.plotly_chart(pie)

                # Performance analysis report card
                st.header(f"{splitname}'s Academics Analysis 🏫")
                if strongestsubject_marks > 89:
                    st.write(f"🎉 Congratulations {splitname} for scoring great in {strongestsubject}! Keep it up!")
                elif strongestsubject_marks >= 79:
                    st.write(f"🎉 Great job {splitname} for scoring well in {strongestsubject}!")
                st.write(f"{splitname}, keep working on {weakestsubject}. Next time target for {weakestsubject_marks + 8}.")

                st.header("Strengths 💪")
                st.write(f"{splitname} scored highest in {strongestsubject}")
                st.header("Areas for Improvement 📉")
                st.write(f"{splitname} needs to work more on {weakestsubject}")

                # Calculate percentage
                total_marks = student_performance['Marks'].sum()
                percentage = (total_marks / 500) * 100
                st.subheader(f"📔 {splitname}'s Academic Score is {percentage:.2f}%")

                if percentage >= 90:
                    st.write(f"Excellent job, {splitname}! Keep it up!")
                elif 85 > percentage > 79:
                    st.write(f"Good work, {splitname}. Next time, target for {percentage + 3:.2f}%!")
                else:
                    st.write(f"Keep working hard, {splitname}. Next time, aim for {percentage + 3:.2f}%!")

                # Loading attendance data
                st.header(f" 📑 {splitname}'s attendance insights ")
                selected_attendance = selectedroll['attendance'].values
                converted_attendance = int(selected_attendance)
                st.write(f"{splitname}'s attendance percentage is {converted_attendance} %")

                # Attendance conditioning
                if converted_attendance >= 90:
                    st.write(f' Congratulations {splitname} for being so attentive! Keep it up! ')
                elif 70 <= converted_attendance < 86:
                    st.write(f"Great job {splitname} for being attentive! Keep it up!")
                else:
                    st.write(f"{splitname}, try to be a little more attentive.")

            else:
                st.warning("Please select subjects to visualize.")

        else:
            st.warning("Please enter a valid roll number.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
