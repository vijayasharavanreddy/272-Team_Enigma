# 272-hrm
Get data from <a href="https://github.com/datacharmer/test_db"> here... </a> and injest into ur local db </br>
<br/>
Create a table hr_user with below cmd:
<code>
CREATE TABLE hr_user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    address VARCHAR(200),
    email VARCHAR(120) NOT NULL UNIQUE,
    mobile_number VARCHAR(20) NOT NULL UNIQUE,
    password_hash VARCHAR(128),
    role VARCHAR(255)
);
</code><br/> 
Configure app.config['SQLALCHEMY_DATABASE_URI'] with your local database connection string <br/><br/>
Install all required packages from requirements.txt

<code> python3 install -r requirements.txt </code>

To run the application: <code> Python3 main.py </code>
<hr/>

# Project-Details:






# High Level Design

![High-Level-Design](https://github.com/shiva-vardhineedi/272-hrm/assets/143037444/f3c2f805-78d1-4f8f-94f9-20428f904890)


# Class Diagram

![WhatsApp Image 2023-12-06 at 6 10 04 PM](https://github.com/shiva-vardhineedi/272-hrm/assets/143037444/9be14bbb-6e6c-4696-8baa-e83b19346d42)



# State Diagram

![state-diagram](https://github.com/shiva-vardhineedi/272-hrm/assets/143037444/1951d040-40bc-418d-8ded-e8fe9e53ab45)

# UML Diagram

![UML_diagram](https://github.com/shiva-vardhineedi/272-hrm/assets/143037444/1bda5717-9536-4924-84a7-86f9055cada7)

# Sequence Diagram

![sequence-diagram](https://github.com/shiva-vardhineedi/272-hrm/assets/143037444/e095a31d-35c9-4aef-a95b-808482706645)






