# Classes App

The `classes` app is the core of the project. It contains the main classroom workflow and most of the academic logic.

## What It Does

- creates classes for teachers
- connects students to classes through memberships
- creates assignments and attaches them to one or more classes
- supports file uploads for assignment attachments and student submissions
- shows assignment detail pages for both teachers and students
- allows teachers to grade submissions

## Main Parts

- `models.py` defines the main database models: `Class`, `Membership`, `Assignment`, `AssignmentFile`, and `Submission`.
- `views.py` contains the class, assignment, submission, and grading logic.
- `urls.py` routes the teacher and student class pages.
- `templates/classes/` contains the detail pages and forms for classes and assignments.

## Design Idea

This app was built as the shared center of the system. The teacher and student apps handle role-specific dashboards, but the actual academic data lives here so the whole platform stays organized and reusable.

