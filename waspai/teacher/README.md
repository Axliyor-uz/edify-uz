# Teacher App

The `teacher` app contains the teacher-facing part of the platform.

## What It Does

- shows the teacher dashboard with class and student statistics
- displays students grouped by the classes they joined
- lets teachers create and manage classes
- provides teacher profile and settings pages

## Main Parts

- `models.py` defines the teacher profile linked to the custom user model.
- `views.py` contains the dashboard, class creation, student list, and settings logic.
- `urls.py` maps the teacher routes.
- `templates/teacher/` contains the teacher-side pages.

## Notes

This app works closely with the `classes` app because teachers do not just manage their profile; they also create classes and later use those classes to organize assignments and student activity.

