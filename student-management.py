"""
Student Management System
A program to manage student information using CSV files.
Allows displaying, adding, and modifying student records.
"""

import csv
import os

def display_menu():
    """
    Display the main menu of the application and get user choice.
    
    Returns:
        str: The user's menu choice
    """
    print("\n=== Student Management System ===")
    print("1. Display all students")
    print("2. Display students by course")
    print("3. Add new student")
    print("4. Modify student email")
    print("5. Exit")
    return input("\nSelect an option: ")

def display_students(file_path):
    """
    Display all students from the CSV file with their information.
    
    Args:
        file_path (str): Path to the CSV file
        
    Displays:
        Each student's name, email, course, and grade (with 2 decimal places)
    """
    try:
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            print("\nName - Email - Course - Average Grade")
            print("-" * 50)
            next(reader)  # Skip header
            for row in reader:
                # Format grade with 2 decimals if not '0'
                grade = row[3]
                if grade != '0':
                    grade = f"{float(grade):.2f}"
                print(f"{row[0]} - {row[1]} - {row[2]} - {grade}")
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

def group_students(file_path):
    """
    Display students from a specific course.
    
    Args:
        file_path (str): Path to the CSV file
        
    Prompts:
        User for course number (1-10)
        
    Displays:
        All students in the specified course with their information
        Error message if course doesn't exist
    """
    try:
        course_num = input("Enter course number (1-10): ")
        target_course = f"Course{course_num}"
        
        found_course = False
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            
            # First check if the course exists
            students_in_course = []
            for row in reader:
                name, email, course, grade = row
                if course == target_course:
                    found_course = True
                    grade = f"{float(grade):.2f}" if grade != '0' else 'No grade'
                    students_in_course.append((name, email, grade))
            
            if found_course:
                print(f"\n{target_course}:")
                for student in students_in_course:
                    print(f"{student[0]} - {student[1]} - {student[2]}")
            else:
                print(f"\nError: Course{course_num} does not exist.")
                
    except FileNotFoundError:
        print("Error: File not found.")
    except Exception as e:
        print(f"Error: {str(e)}")

def add_student(file_path):
    """
    Add a new student to the CSV file.
    
    Args:
        file_path (str): Path to the CSV file
        
    Prompts:
        User for student name, email, course number, and grade
        
    Notes:
        - Grade can be 0 if not available
        - Grade must be between 0 and 100
        - Grade is stored with 2 decimal places
    """
    try:
        name = input("Student name: ")
        email = input("Student email: ")
        course_num = input("Course number (1-10): ")
        course = f"Course{course_num}"
        grade = input("Average grade (0 if none): ")
        
        if grade == '0':
            grade = '0'
        else:
            try:
                grade = float(grade)
                if not (0 <= grade <= 100):
                    print("Error: Grade must be between 0 and 100")
                    return
                grade = f"{grade:.2f}"  # Format with 2 decimals
            except ValueError:
                print("Error: Please enter a valid number")
                return

        new_student = [name, email, course, grade]
        
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_student)
        print(f"\nStudent {name} successfully added.")
    except Exception as e:
        print(f"Error adding student: {str(e)}")

def modify_email(file_path):
    """
    Modify the email address of an existing student.
    
    Args:
        file_path (str): Path to the CSV file
        
    Prompts:
        User for student name and new email
        
    Notes:
        - Search is case-insensitive
        - User can type 'exit' to return to main menu
        - Preserves CSV header during modification
    """
    student_name = input("Student name (or 'exit' to return): ")
    if student_name.lower() == 'exit':
        return
    
    try:
        # Read entire file
        students = []
        found = False
        with open(file_path, 'r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            students.append(header)
            
            for row in reader:
                if row[0].lower() == student_name.lower():
                    found = True
                    print(f"Current email: {row[1]}")
                    new_email = input("New email: ")
                    row[1] = new_email
                students.append(row)
        
        if found:
            # Write changes
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(students)
            print(f"\nEmail for {student_name} successfully updated.")
        else:
            print(f"\nStudent {student_name} not found")
    except Exception as e:
        print(f"Error modifying email: {str(e)}")

def main():
    """
    Main function to run the Student Management System.
    Provides a menu-driven interface for all operations.
    """
    file_path = 'synthetic_students.csv'
    
    while True:
        option = display_menu()
        
        if option == '1':
            display_students(file_path)
        elif option == '2':
            group_students(file_path)
        elif option == '3':
            add_student(file_path)
        elif option == '4':
            modify_email(file_path)
        elif option == '5':
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()