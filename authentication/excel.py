import pandas as pd
from faker import Faker

# Create an instance of the Faker class
fake = Faker()

# Function to generate random student data
def generate_student_data(num_students):
    # Lists to store data
    names = []
    emails = []
    phones = []

    # Generate data
    for _ in range(num_students):
        names.append(fake.name())
        emails.append(fake.email())
        phones.append(fake.phone_number())

    # Create a DataFrame
    data = {
        'Name': names,
        'Email': emails,
        'Phone': phones
    }
    return pd.DataFrame(data)

# Generate data for 2 students
df_students = generate_student_data(2)

# Save to Excel
df_students.to_excel('students.xlsx', index=False)

print("Excel file 'students.xlsx' has been created with 2 students' data.")
