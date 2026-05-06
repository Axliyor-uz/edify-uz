# Student App

The `student` app contains everything related to the student experience.

## What It Does

- shows a student dashboard with class and teacher counts
- lists the classes a student has joined
- lets students browse all classes and join new ones
- shows class detail pages for enrolled students
- provides profile and settings pages

## Main Parts

- `models.py` defines the student profile linked to the custom user model.
- `views.py` contains the dashboard, class browsing, join, profile, and settings logic.
- `urls.py` maps the student routes.
- `templates/student/` contains the pages used by students.

## Notes

Student data is connected to class membership through the `Membership` model in the `classes` app. This keeps enrollment history in one place and makes it easier to count joined classes and display related teacher information.

