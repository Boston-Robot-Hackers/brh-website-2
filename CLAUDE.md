# CLAUDE.md

## Overview

* a static web site generator which converts a series of templates and content and generates a directory of html, js and css that fully represents the web site of the Boston Robot Hackers

## Key Technical Directives

* Use uv for package management not pip. Only use UV
* We use markdown for much of the user supplied content
* Look for and eliminate duplicate code or css
* There should almost never be css or js inside an html file
* Templates represent different types of page on the web site
* The generator regenerates the complete contents of the output/ directory
* Claude should not edit the output/ files directly, instead look at generator to see how they are created
* Github actions are used to produce and github page hosted web site from the output/ directory

## Key Coding Style Requirements

* Code in Python using latest version
* Always look for a well supported package to implement a feature
* Look for and eliminate duplicate code
* Use Python classes where appropriate
* No methods or functions longer than 50 lines
* No source files longer than 300 lines
* No html or css inside of python source files. Very small exceptions are permitted
* Uses only ROS2
* Write idiomatic Python
* Don't go overboard on error checking
* Give methods intention revealing names
* Use classes and put them in a separate file
* Put data classes in the file where they are constructed
* Name files after the class defined in the file
* Use Python latest and ROS2 compliant package management and building with colcon
* Prefer async/await over threading when there is a choice
* Avoid if/else statements that are nested more than 1 deep
* Avoid 1 line methods
* Look for code duplication and make the code DRY if it makes sense
* When undertaking a multi step implementation or refactoring, do it in a way that after each step we retain a running program so that I can test it to make sure we are on the right track
* Don't assign the result of a function to a variable just to use that variable one time only, just use the function call

