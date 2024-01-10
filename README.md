This is my educational project, the beginning of my acquaintance with web development
ASKII - Question-Answer Website
This repository contains the code for ASKII, a question-answer website developed using Django.

Features
Question and Answer Functionality: Users can post questions, provide answers, and like both questions and answers.
Tagging System: Questions can be tagged for easy categorization.
User Profiles: Each user has a profile containing their details and activity on the platform.
Authentication: User authentication and authorization for secure access.
Settings Management: Users can modify their profiles and account settings.
Structure
Models
Tag: Represents tags used for categorizing questions.
Question: Contains details of posted questions along with their tags and associated answers.
Profile: User profile with additional information and activity tracking.
Answer: Answers provided by users for specific questions.
QuestionLike and AnswerLike: Models for tracking likes on questions and answers.
Views
index: Landing page displaying new questions.
ask: Page for users to post new questions.
settings: User settings page for profile and account modifications.
log_in and logout: Authentication views for login and logout.
signup: View for user registration.
tag: Page to display questions based on specific tags.
question: View to display a single question along with its answers.
hot: Displays hot questions based on likes.
profile: User profile view showing their posted questions.
like: View for handling like functionality.
Forms
LoginForm, RegisterForm: Forms for user authentication and registration.
SettingsForm, ProfileSettingsForm: Forms for modifying user settings and profiles.
AskForm, AnswerForm: Forms for posting questions and answers.
URLs
Contains URL configurations for different views.

Installation and Usage
Clone the repository.
Set up a Python virtual environment.
Install required dependencies using pip install -r requirements.txt.
Run the Django server using python manage.py runserver.
