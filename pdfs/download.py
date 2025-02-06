import os
import mysql.connector
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

# Function to generate PDF for a user
def generate_user_pdf(user_data, test_report_data, output_directory):
    # Create a PDF document
    pdf_filename = os.path.join(output_directory, f"{user_data['username']}.pdf")
    pdf = SimpleDocTemplate(pdf_filename, pagesize=letter)

    # Get predefined styles
    styles = getSampleStyleSheet()

    # Define table style
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    # Prepare user data for the table
    user_table_data = [[Paragraph("<b>ID</b>", styles['Normal']), Paragraph("<b>Username</b>", styles['Normal']), Paragraph("<b>Email</b>", styles['Normal'])],
                       [user_data["id"], user_data["username"], user_data["email"]]]

    # Prepare test report data for the table
    test_report_table_data = [[Paragraph("<b>Attribute</b>", styles['Normal']), Paragraph("<b>Value</b>", styles['Normal'])]]
    for attribute, value in test_report_data.items():
        test_report_table_data.append([attribute, value])

    # Create tables
    user_table = Table(user_table_data)
    test_report_table = Table(test_report_table_data)

    # Add style to the tables
    user_table.setStyle(style)
    test_report_table.setStyle(style)

    # Build PDF
    elements = [Paragraph("<u>User Details:</u>", styles['Heading1']), user_table, Paragraph("<u>Test Report:</u>", styles['Heading1']), test_report_table]
    pdf.build(elements)

    print(f"PDF generated for {user_data['username']}")

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="user_db"
)
cursor = conn.cursor(dictionary=True)

# Specify the output directory for PDF files
output_directory = r"C:\Users\Dipen Rana\Desktop\Parkinson\pdfs"

# Fetch data from users table
cursor.execute("SELECT id, username, email FROM users")
users_data = cursor.fetchall()

# Fetch data from test_report table for each user
for user_data in users_data:
    cursor.execute(f"SELECT * FROM test_report WHERE id = {user_data['id']}")
    test_report_data = cursor.fetchone()

    # Generate PDF for the user
    generate_user_pdf(user_data=user_data, test_report_data=test_report_data, output_directory=output_directory)

# Close MySQL connection
conn.close()
