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
- Combining bootstrap css with back-end code to produce visual results;
- Automatic RSS feed updating and retrieval, with functionality to add more feeds to be automatically parsed in the
admin panel.
- Custom model form validation to catch unique constraints.
-----------------------------------------

This was my graduation project for my python programming course. It was written in roughly 2 weeks. I used the Django framework to create a website that provides the following information and functionality to the user:
- Weather forecasts in cities and regions of their choosing using the Nominatim API for geocoding and OpenWeatherMap API for the weather forecast;
- Current currency rates fetched from the European Central Bank via the Frankfurter API. The app can draw a basic graph using matplotlib of currency changes over a specified time period, as well as convert currency for the user;
- RSS feed of news sites of choice (New Scientist used as an example) and steam games the user may be interested in (Final Fantasy XIV used as an example);
- Birthday, to-do list reminders;
- Memo/note-taking functionality;

I have experimented and learned a lot while undertaking this project. It was a good introduction to principles of basic front-end programming and how it ties with the back-end. It allowed me to practice working with APIs, task-scheduling scripts, SQL database manipulation using ORM and more. Working on it required me to become comfortable with trouble-shooting either via researching problems online through Stack Overflow or through perusing module documentation directly. I attempted principles such as test-driven development while working on some modules and weighed it against writing tests after the fact in others.

The app still requires some work and improvement. Particular areas of focus to improve it would be:
- Expanding testing for each module within the app.
  Some unit tests have been written, but more need to be introduced to successfully capture standard errors and data outliers in API calls.
- Expanding error message implementation.
  Django messages have been implemented, but not all errors are captured as Django messages and displayed to the user yet. Some refactoring is necessary to improve this.
- HTML refactoring for better display.
  Some visual bugs are still present and need some patching up. Introduction of more modals and less redirects may be necessary to make the app more user-friendly and less annoying to use on slower networks/hardware.
- Optimisation and code standartisation.
  While working on this I had experimented a lot. Some modules may use slightly different logic in the code, be less optimal in implementing their functionality, for example some views as a function may be better served being transformed into class-based views and vice-   versa. It would improve readability and make the app easier to maintain if everything was standartised and some operations were optimised.
