# LITRevu
 A Django site for reviewing books and articles.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Rules](#rules)
- [Contributing](#contributing)
- [License](#license)

## Prerequisites
This project use Sass and Bootstrap.
The Bootstrap files are located in .\LITRevu\LITReview\static\sass\node_modules\bootstrap and are importing into main.scss.

If you haven't Sass installed on your computer and wish to contribute, you'll need to have npm installed. Here are the steps:

1. Download NodeJS from the following link: https://nodejs.org/en and install it.
(For Linux users):
Open your terminal and run: 
```bash 
sudo apt install nodejs npm 
```
2. Verify your Node.js and npm versions: 
```bash
 node -v
 ```
 ,
  ```bash
   npm -v 
   ```
3. (Optional, if you use Visual Studio Code) Install "Live Sass Compiler" from https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass
4. Open a terminal
5. Install sass with: 
```bash
 npm -g install sass 
 ```
6. Finally, execute the following command to compile your Sass: 
```bash
 npm run sass 
 ``` 

Once you've completed these steps, you can write your CSS style properties in the .\LITRevu\LITReview\static\sass\main.scss file, 
and it will be compiled into .\LITRevu\LITReview\static\style.css.

## Installation

1. Clone the repository:  
```bash
git clone https://github.com/DarkExplorer31/LITRevu
```
2. Create a virtual environment and activate it:
```bash
python -m venv venv
```
if you use Windows:
```bash
env\Scripts\activate
```
on Mac or Linux:
```bash
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Apply database migrations:
```bash
python manage.py migrate
```
5. Run the development server:
```bash
python manage.py runserver
```

## Rules
This Django project consists of two applications: Authentication and Review.
The Authentication application handles user-related functionalities, while the Review application manages tickets and reviews.

It's important to note that there are specific rules that should be adhered to:

1. All tickets that have associated reviews should be displayed within the review's section, 
except for tickets created by the same user who wrote the review. 
In this case, those tickets should be displayed separately.

2. The home feed or activity feed should display content in reverse chronological order, with users being able to view tickets from people they follow, users they are followed by, their own tickets and reviews. Users should also have the ability to view all reviews associated with these tickets.

3. Users should be able to create both tickets and reviews using the same form.

## Contributing
If you'd like to contribute to this project, please follow these guidelines:

1. Fork the project on GitHub.
2. Create a new branch with a descriptive name.
3. Commit your changes and push your branch to your fork.
4. Open a pull request to the main repository.

[Back to table of content](#table-of-contents)

## License
Distributed under the MIT License. See LICENSE.txt for more information.
[Back to table of content](#table-of-contents)