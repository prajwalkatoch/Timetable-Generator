from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
import random

# Load data from CSV files
classes_df = pd.read_csv('classes.csv')
courses_df = pd.read_csv('courses.csv')
faculty_df = pd.read_csv('faculty.csv')

# Convert 'courses' column in classes_df and faculty_df to lists of integers
classes_df['courses'] = classes_df['courses'].apply(lambda x: list(map(int, x.split(','))))
faculty_df['courses'] = faculty_df['courses'].apply(lambda x: list(map(int, x.split(','))))

# Constants
DAYS = ["MON", "TUE", "WED", "THU", "FRI", "SAT"]
TIME_SLOTS = ["10:00-11:00", "11:00-12:00", "12:00-1:00", "Lunch Break", "1:30-2:30", "2:30-3:30"]

# Initialize timetable dictionary for each class
timetable = {class_id: {day: {slot: None for slot in TIME_SLOTS} for day in DAYS} for class_id in classes_df['class_id']}

# Function to check faculty availability
def is_faculty_available(faculty_id, day, time_slot):
    for class_id in timetable:
        if timetable[class_id][day][time_slot] and timetable[class_id][day][time_slot]['faculty_id'] == faculty_id:
            return False
    return True

# Generate timetable
for _, class_row in classes_df.iterrows():
    class_id = class_row['class_id']
    class_courses = [course_id for course_id in class_row['courses']]
    
    for course_id in class_courses:
        course_info = courses_df[courses_df['course_id'] == course_id].iloc[0]
        lec_per_week = course_info['lectures_per_week']
        
        # Find faculty members who can teach this course
        available_faculty = faculty_df[faculty_df['courses'].apply(lambda courses: course_id in courses)]
        
        for _ in range(lec_per_week):
            assigned = False
            while not assigned:
                day = random.choice(DAYS)
                time_slot = random.choice(TIME_SLOTS)
                
                # Skip "Lunch Break" slot
                if time_slot == "Lunch Break":
                    continue
                
                # Check if time slot is available for this class
                if timetable[class_id][day][time_slot] is None:
                    for _, faculty_row in available_faculty.iterrows():
                        faculty_id = faculty_row['faculty_id']
                        faculty_name = faculty_row['faculty_name']
                        
                        # Check if faculty is available at this time
                        if is_faculty_available(faculty_id, day, time_slot):
                            timetable[class_id][day][time_slot] = {
                                "course_id": course_id,
                                "course_name": course_info['course_name'],
                                "faculty_id": faculty_id,
                                "faculty_name": faculty_name
                            }
                            assigned = True
                            break  # Exit faculty loop once assigned

# Function to generate PDF with lunch break and wrapped text
def generate_pdf(timetable, filename="timetable.pdf"):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 10)
    width, height = letter
    margin = 30  # Margin around the content
    styles = getSampleStyleSheet()  # Get default styles for Paragraphs
    style = styles['BodyText']  # Use BodyText style for wrapping text

    for class_id, class_timetable in timetable.items():
        data = [["Day/Time"] + TIME_SLOTS]
        
        for day, slots in class_timetable.items():
            row = [day]
            for slot in TIME_SLOTS:
                if slot == "Lunch Break":
                    # Add "Lunch Break" label for the lunch time slot
                    text = "Lunch Break"
                else:
                    session = slots[slot]
                    if session:
                        text = f"{session['course_name']} ({session['faculty_name']})"
                    else:
                        text = "Free"
                row.append(Paragraph(text, style))  # Use Paragraph for text wrapping
            data.append(row)
        
        # Define column widths to prevent None values
        column_widths = [80] + [80] * len(TIME_SLOTS)
        
        # Create a table with specified column widths
        table = Table(data, colWidths=column_widths)
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center text vertically
        ]))
        
        # Draw class title
        c.drawString(margin, height - margin, f"Timetable for Class {class_id}")
        
        # Calculate table position and scale to fit the page if needed
        available_width = width - 2 * margin
        available_height = height - 2 * margin - 40  # Leave space for the title
        
        # Adjust the table width and height based on available space
        table_width, table_height = table.wrap(available_width, available_height)
        
        if table_width > available_width or table_height > available_height:
            scale = min(available_width / table_width, available_height / table_height)
            table_width *= scale
            table_height *= scale
            table._argW = [col_width * scale for col_width in column_widths]  # Adjust column widths to scale
        
        # Draw the table on the canvas
        table.drawOn(c, margin, height - margin - table_height - 40)  # 40 is the space for title

        c.showPage()  # Create a new page for each class

    c.save()

# Generate the timetable PDF
generate_pdf(timetable)

print("Timetable PDF generated successfully.")
