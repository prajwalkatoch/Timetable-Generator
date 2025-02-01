# Timetable Generator

## Overview
This project generates a **class timetable PDF** based on input data from CSV files containing class, course, and faculty information. The system ensures that:
- Classes are assigned lectures based on the number of weekly sessions required per subject.
- Faculty members are assigned only to courses they are qualified to teach.
- No scheduling conflicts occur for faculty members.
- The generated timetable is visually structured and exported as a **PDF file**.

## Features
- **Automated Scheduling**: Assigns subjects to available time slots.
- **Faculty Conflict Checking**: Ensures faculty are not double-booked.
- **Customizable Time Slots**: Editable daily schedule format.
- **Lunch Break Handling**: Preserves a fixed lunch break time.
- **PDF Generation**: Uses `reportlab` to generate structured PDF reports.
- **Randomized Scheduling**: Allocates courses dynamically to avoid static patterns.

## Technologies Used
- **Python 3**
- **Pandas**: Handles CSV data manipulation.
- **ReportLab**: Generates PDFs with structured tables and formatted text.
- **Random Module**: Distributes courses across different time slots.

## Installation
### Prerequisites
Ensure you have **Python 3** installed along with the required dependencies:
```sh
pip install pandas reportlab
```

## CSV File Structure
### `classes.csv`
This file contains the list of classes and their assigned courses.
```csv
class_id,courses
1,101,102,103
2,104,105
```

### `courses.csv`
This file lists the available courses and their weekly lecture count.
```csv
course_id,course_name,lectures_per_week
101,Mathematics,3
102,Physics,2
```

### `faculty.csv`
This file contains faculty members and the courses they can teach.
```csv
faculty_id,faculty_name,courses
1,John Doe,101,102
```

## Usage
1. **Prepare CSV Files**: Ensure `classes.csv`, `courses.csv`, and `faculty.csv` are correctly formatted.
2. **Run the script**:
   ```sh
   python timetable_generator.py
   ```
3. **View the PDF Output**: A `timetable.pdf` file is generated in the project directory.

## Customization
- Modify the **days of the week** or **time slots** by adjusting the `DAYS` and `TIME_SLOTS` lists in the script.
- Customize the **PDF layout** and styling in the `generate_pdf()` function.

## Future Enhancements
- **User Interface**: A web or GUI-based tool for timetable customization.
- **Database Integration**: Store and manage data dynamically.
- **Optimized Scheduling**: Implement AI-based scheduling for better efficiency.

## License
This project is open-source under the MIT License.

## Author
Developed by Prajwal Katoch. Feel free to contribute and improve!

