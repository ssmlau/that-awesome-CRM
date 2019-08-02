To get started:
Need the requirements in requirements.txt (not all, just some key ones, flask, pyrebase4, python3)

Run with (in the app directory)
$ export FLASK_APP=app.py
$ flask run
 * Running on http://127.0.0.1:5000/

To debug:
$ export FLASK_ENV=development
$ flask run

To log: (will log into dev console)
app.logger.info("test")

README.md

****Feature Documentation

In order to understand the features available for the CRM, you must first understand the structure of how things are mapped.

Background:

1. Every user has their own login, associated with an ID that uniquely identifies who they are.
2. A client has the ability to add, update, delete and view any projects that they have made or anybody else has made.
3. Every client has associated projects, interactions and issues.
A project: Any ongoing project that a client is looking to undergo. Since a client may have many projects, this keeps track of all history so that it can be referred to. A project can also span any time length from a few weeks to a couple of years.
An interaction: Any form of communication that was made with the client is logged here. For example, if a consultant called or communicated with e-mail. This is for transparency.
An issue: This is any issue that a client is having, and the consultant will update this. This is so that any future consultants working on the project or client can see the way the client works and any ways in which they can better serve the client. It is important that issues are not deleted unless necessary.
4. Under every project, interaction, and issue, a consultant can make a comment. Any consultant can comment on a project in case the individual missed something. Some things that are counted may be a question regarding the current issue or a comment about whether something has been collected. 

Features:

Client Specific:
Add a client: Consultants are able to add a client on the mainpage
Delete a Client: Consultants are able to delete any clients on the mainpage
Update a Client: Consultants are able to update any information regarding size, point of contact and contact name.
View: Consultants are able to view any clients:

Interaction Specific:
These features follow the same as the Client specific features but clients can log, update, delete and view any interactions.
Log an interaction
Update an interaction
Delete an interaction
View	

Issue Specific: 
These features follow the same as the Client specific features, but clients can log, update, delete and view any issues.
Log Issue
Delete Issue
Update Issue
View

Project Specific: 
These features follow the same as the Client specific features, but clients can log, update, delete and view any projects.
Create Project, 
Update Project, 
Delete project, View

Comments: 
These features allow clients to add, delete, update, or view any comment on any project, interaction and issue.
Add Comment,
Delete Comment
Update Comment
View	

Together, these features keep track of projects and clients that the CFC has. Through this, the CFC foundation aims to better serve their clients by keeping a well documented place of all things going on. 

Additional Features:

Google maps External API feature: This feature allows a user to search up any location that they may need when needed for a specific site. Furthermore, it provides the ability for users to find airports, hotel bookings, or any other miscellaneous items needed for visiting a client site. 

# that-awesome-CRM
