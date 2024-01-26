Author: Robertas Kulnis
------------------------------------------
Project Name: Loyal Companion
------------------------------------------
Project description:
A Django-based "companion app" that delivers to the user current currency exchange rates, weather forecasts for their
chosen cities, upcoming birthdays and tasks, as well as memos they might have saved.
------------------------------------------
Technical challenges:
- Updating, deleting, creating new database entries automatically, periodically using django-apscheduler;
- Using API calls and saving the response, if it is favourable, to a database;
- Displaying data from one app in another;
- Compartmentalisation of some template components by creating custom template tag libraries;
- Limited use of unit tests with django's inbuilt test system;
- Chaining API calls to get information of interest;
- Extensive use of bootstrap elements and JS script functionality;
- Combining bootstrap css with back-end code to produce visual results;
- Automatic RSS feed updating and retrieval, with functionality to add more feeds to be automatically parsed in the
admin panel.
- Custom model form validation to catch unique constraints.
-----------------------------------------