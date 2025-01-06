# MealCount Web Application
## Overview

The MealCount Web Application helps manage daily meal counts for a student hostel. It enables users (students) to register for meals, track their consumption, and provides admins with tools for meal management and cost calculations.

This application is built using FlutterFlow, with Firebase Authentication for user login, Firestore to persist user and meal count data, and a periodic backup system to Google Sheets for easy access to data.

## Features
### User Features:
- Meal Registration:

  Users can separately enroll for Lunch and Dinner.
  Meal registration is restricted to specific time windows for each meal.
- Cumulative Meal Tracking:
  
  Users can view their total meals consumed for the month to track their payment calculations.

### Admin Features:

- Meal Count Review:
  
  Admins can review the daily meal count to ensure accurate food preparation and prevent wastage.

- Meal Count Deletion:

  Admins can delete registered counts for a particular meal if it's canceled due to unforeseen circumstances.

- Google Sheets Backup:

  A script runs periodic backups of the Firestore database to a Google Sheet, simplifying month-end cost calculations for the hostel.

- Automated Email Notifications:

  Daily email alerts are sent to users for meal registration reminders.

## Try It!

App Link: https://mealcount-eu4ec2.flutterflow.app/

  - Admin Login:

      Email: admin@gmail.com
    
      Password: appadmin

  - User Login:

      Email: user@gmail.com
    
      Password: appuser

