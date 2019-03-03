Introduction
------------

Welcome to `The Interactive NHL Experience`! This project was made for 15-112,
an introductory programming class at Carnegie Mellon University. It uses Python
and MongoDB to maintain a local database of NHL player and team information. A 
user is allowed to view and update the data. In addition top news headlines are 
shown via an integrated News API. Finally, a game prediction feature is provided
that allows a user to pit two teams (home and away) against each other. A predicted
winner and score will be shown.

This file explains all the required modules and technologies that are required
to run `The Interactive NHL Experience` program.

Required Modules
----------------

There are a multitude of required modules for this project to run completely,
but most of them are already imported inside the file. However, there is one
module that is not built in, and must be downloaded. This module is pymongo.
To install it, go to your terminal and type 'pip install pymongo'. That command
should install the module.

Required Technologies
---------------------

There is only one required outside technology that is used in the project, and
that is the MongoDB Community Edition software. To install this software, go to
the link https://docs.mongodb.com/manual/installation/ and follow the
instructions for your specific operating system.

Running the Project
-------------------

Once you have pymongo and the MongoDB Community Edition installed, you are ready
to run the project. To start, you have to create a new instance of MongoDB on
your laptop. To do so, go to your terminal and type 'mongod'. You will see a
series of text show up. Once the terminal stops and shows the line 'waiting for
connections on port 27017', you can run the main.py file in your editor of
choice and use the application. To close the instance of mongoDB, simply press
Control + C while in the terminal.

I hope you enjoy my project!

Author: Dillan Gajarawala, Carnegie Mellon University

Powered by News API
