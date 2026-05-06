# Accounts App

The `accounts` app manages authentication and the shared user profile flow for the whole project.

## What It Does

- registers new users
- logs users in and out
- sends users to the right dashboard after login
- shows a simple profile page after registration

## Main Parts

- `models.py` defines the custom user model with a `role` field.
- `forms.py` contains the registration form.
- `views.py` handles register, login, logout, and profile pages.
- `urls.py` exposes the authentication routes.
- `templates/accounts/` contains the HTML pages for the forms and profile view.

## Why It Matters

This app is the entry point for the entire system. Every other app depends on the user role created here, because the role decides whether the user sees student or teacher features.
