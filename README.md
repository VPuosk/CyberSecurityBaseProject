LINK: https://github.com/VPuosk/CyberSecurityBaseProject

The usual Python Django program installation. So I'm here assuming that Python (together with Django) and Git have been installed. To clone to repository go to directory of your choice and use command: 'git clone https://github.com/VPuosk/CyberSecurityBaseProject.git'.

In case you want to start the program you should use command: 'python manage.py runserver' when in the program's directory. Which should then inform you as to from which port of the localhost the program can be found. You can shutdown the application by using Ctrl-Break key combination (using for example Anaconda Prompt in windows).

Following accounts have been created:
    - Admin:
        - Username: admin
        - Password: admin
    - Timo:
        - Username: Timo
        - Password: Testaaja
    - Kille:
        - Username: Kille
        - Password: Kokeilija
        
Some meaningless test data has also already been included to the database. Program consists of two parts, one is for posting shared (among all users) posts and another one which is for posting personal notes.


FLAW 1:

Insufficient Logging & Monitoring:

https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L25

Issue:
Program is not logging anything at the moment event though it has support for that. By adding monitoring of user activity, and especially login and failed login activity greatly increases the awareness of access attempts to the server. Additionally database write access is not being logged at all.

Fix:
Removing comment markers from the lines 25 - 29 in the views.py (i.e. linked document) starts the logging on failed login attempts. Other activities (successful logins) could also be logged but this is just an example. These are now just pushed into the console but in more serious software they ought to be logged into a separate log files. In similar manner logging can be enabled especially on any database access that potentially allows for the SQL injection but also preferably on database write access. Ability to track the vulnerable points of the webpage via logged activities makes it possible for the maintainer to become aware of the problems with the site.


FLAW 2:

Injection

https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L51

Issue:
Function 'showFilteredList(request)' uses unsafe method of accessing the database making SQL injection attack possible in case the database contents are filtered. This makes the SQL database technically vulnerable to the SQL injection. Injection with for example: "re' OR 1=1;--" shows full list of posts to any one accessing the filtered views page. This also forms part of the problem of the flaw #5.

Fix:
The best way to fix the threat on an SQL injection attack in this case would be to replace all instances where database raw or direct access is used with sanitized (by Django) parametrized queries. For example the filtered option could be replaced with "Post.objects.filter(header = filterText).order_by('-time')". This would remove the direct or raw access to the SQL database making it much harder to perform SQL injections.


FLAW 3:

Broken Authentication

No link (overall program setting)

Issue:
Program uses Django's default protection method which is supposed to be fairly strong protection - however on this instance as so very often with locally maintained systems the admin username and admin password are both 'admin'. This is a very bad username/password combination, that can be easily guessed, and which should never ever actually be used in production.

Fix:
Easiest option would be to simply replace the password for the admin account with something much harder to guess or fuzz. The easiest way of doing this would be to issue a command line command: "python manage.py changepassword admin" and replacing the admin password with something much more secure than just 'admin'. Additionally it would be a good idea to create a better and harder to guess name for admin account as well - in other words it would not hurt to create a whole new admin account and remove the 'admin' account altogether since that account name is fairly obvious and therefore clearly a potential vulnerability.


FLAW 4:

Broken Access Control

https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L75
https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L87

Issue:
Functions showNotes and postNewNote both use the path parameter name (from /notes/<name>/) for determining the user while still requiring login. This allows for example user A to access personal notes of user B and even post more of them.

Fix:
Access to sensitive or personal information should be limited. This could be done for example by making sure that variables 'name' and 'request.user' have to match before allowing the function to continue. This would enable only the person who has logged in to be able to access his or her personal information.


FLAW 5:

Sensitive Data Exposure

https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L51
https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L42
https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L103
https://github.com/VPuosk/CyberSecurityBaseProject/blob/42ec8697458273167be14368edb1010a0eeffeb8/sovellus/views.py#L110

Issue:
Program makes it possible for any one accessing the webpage to read any of the sent posts without login. While the actual initial index page requires login the subsequent 'filtered' view or pages for individual posts do not. This makes it possible for any one to access the pages leading to potential data exposure depending on what information is stored in the posts. It is even possible to make new posts into the database without logging in.

Fix :
All view function calls 'showPost' 'showFilteredList' 'addNewPost' 'postNewPost' should be preceded with "@login_required" notation. This should prevent the sensitive data from being accessed.
