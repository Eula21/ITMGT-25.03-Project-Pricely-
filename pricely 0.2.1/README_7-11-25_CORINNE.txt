Changes:
    - added these new views in (views.py) and added paths for them in (urls.py):
        - (login_view)
        - (signup_view)
        - (logout_view)
    - deleted the search_history view in (views.py) because i forgot to delete it last time HASHDH
    - added new html files to direct users to a new page for logging in and signing up:
        - (login_view.html)
        - (signup_view.html)
    - added a profile dropdown in (index.html)
    - renamed the index and search_results html files so that the simple versions will be referenced instead of gpt’s

Changes I made to Lyss’ updates (to fix errors)
    - Deleted the first line: {% extends "base.html" %} from (my_lists.html)

Remember (to prevent errors)
    - Ensure to make migrations for every time a new model has been created
        - python manage.py makemigrations
        - python manage.py migrate

Admin details (to access the admin panel)
    Username: pricelyadmin
    Email: corinne.andie.tan@student.ateneo.edu
    Password: pricelyy

