''' Student performance Visual for meetings and analysis
Built by : D. Rana 
Version 2.1.1'''

# importing modules
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
st.header(' Student Performance tracker©️  V1.1.1 🧑‍🏫')
st.subheader('Analyse Student Performance in real time')
st.write(' Built by D.Rana  ')
st.write(' Code restricted and not be used without permission ')


# File upload
fileupload = st.file_uploader('Please upload your file here', type='XLSX')


#file uploading conditioning
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
                bar = st.progress(2)
                time.sleep(2)
                bar.progress(2)

                with st.status("Loading data ...") as s:
                    time.sleep(2)
                    st.write("loading")




                studentname = selectedroll['Name'].values[0]
                splitname = studentname.split()[0]
                st.write(f"{studentname} performance in selected subjects")

                # Create a dataframe for the selected subjects
                student_performance = selectedroll[selection].T
                student_performance.columns = ['Marks']
                student_performance['Marks'] = student_performance['Marks'].astype(float)
                student_performance['Subjects'] = student_performance.index

                # Bar chart colors
                bar_colors = ['#ADD8E6', '#FA8072', '#FFD700', '#2E8B57', '#EE82EE']
                markercolors = ['#FFFFFF', '#8B0000', '#FF8C00', '#008080', '#800080']

                # Create subplots for combined bar and line chart
                fig = make_subplots(specs=[[{"secondary_y": True}]])

                # Add bar chart
                fig.add_trace(
                    go.Bar(
                        x=student_performance['Subjects'],
                        y=student_performance['Marks'],
                        name='Marks',
                        marker_color=bar_colors,
                    ),
                    secondary_y=False,
                )

                # Add line chart
                fig.add_trace(
                    go.Scatter(
                        x=student_performance['Subjects'],
                        y=student_performance['Marks'],
                        name='Score marker',
                        mode='lines+markers',
                        line=dict(color='white'),
                        marker=dict(color=markercolors, size=10),
                    ),
                    secondary_y=False,
                )

                fig.update_layout(
                    title_text=f"{studentname}'s performance in Selected Subjects",
                    xaxis_title="Subjects",
                    yaxis_title="Marks",
                    yaxis=dict(range=[0, 100]),
                    width=1500,
                    height=509,
                    showlegend=True,
                )
                st.plotly_chart(fig)

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

                # Plot strongest subject performance
                fig_strongest = go.Figure()
                fig_strongest.add_trace(go.Scatter(
                    x=df_strongest['Type'],
                    y=df_strongest['Score'],
                    mode='lines+markers',
                    name=f"{strongestsubject} Performance",
                    line=dict(color='blue', width=2),
                    marker=dict(size=10)
                ))
                fig_strongest.update_layout(
                    title=f"Comparison of Student's Performance in {strongestsubject}",
                    xaxis_title="Type",
                    yaxis_title="Score",
                    showlegend=True
                )

                # Plot weakest subject performance
                fig_weakest = go.Figure()
                fig_weakest.add_trace(go.Scatter(
                    x=df_weakest['Type'],
                    y=df_weakest['Score'],
                    mode='lines+markers',
                    name=f"{weakestsubject} Performance",
                    line=dict(color='red', width=2),
                    marker=dict(size=10)
                ))
                fig_weakest.update_layout(
                    title=f"Comparison of Student's Performance in {weakestsubject}",
                    xaxis_title="Type",
                    yaxis_title="Score",
                    showlegend=True
                )

                # Adding a pie chart for better analysis
                pie = px.pie(values=student_performance['Marks'],
                             names=student_performance['Subjects'],
                             title=f"{splitname} performance share")
                st.plotly_chart(pie)

                # Performance analysis report card
                st.header(f"{splitname}'s Academics Analysis 🏫")
                if strongestsubject_marks > 89:
                    st.write(f"🎉 Congratulations {splitname} for scoring great in {strongestsubject}! keep it up ")
                elif strongestsubject_marks >= 79:
                    st.write(f"🎉 Great job {splitname} for scoring well in {strongestsubject}!")
                st.write(f"{splitname}, keep working on {weakestsubject}. Next time target for {weakestsubject_marks + 8}.")

                st.plotly_chart(fig_strongest)
                st.plotly_chart(fig_weakest)

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
                st.header(f" 📑 {splitname}'s  attendance insights ")
                selected_attendance = selectedroll['attendance'].values
                converted_attendance = int(selected_attendance)
                st.write(f"{splitname}'s attendance percentage is  {converted_attendance} % ")

                # Attencdance condtioning
                if converted_attendance >= 90:
                    st.write(f' Congratulations {splitname} for being so attentive keep it up ')
                elif converted_attendance >=70<86:
                    st.write(f"Congratulations {splitname} for being so attentive keep it up ")
                else:
                    st.write(f" {splitname} try to be little more attentive ")


            else:
                st.warning("Please select subjects to visualize.")

        else:
            st.warning("Please enter a valid roll number.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
