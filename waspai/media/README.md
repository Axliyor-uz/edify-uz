# Home App

The `home` app contains the landing page of the project.

## What It Does

- shows the public home page for visitors who are not logged in
- redirects authenticated users to the correct dashboard based on their role

## Main Parts

- `views.py` contains the home view and redirect logic.
- `urls.py` connects the root route to the home page.
- `templates/home/` contains the landing page template.

## Why It Matters

This app keeps the project entry flow simple. Instead of sending every user to the same page, it checks the login state and role first, then forwards the user to the right place.

