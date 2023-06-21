# SQL templates for R10: User Registration & Login

### Register user
INSERT INTO user (name, password, email, registration_date) 
VALUES(<name>, <hashed_password>, <email>, CURRENT_TIMESTAMP);

### Log in
# application will verify if password matches inputted password
SELECT email, password FROM User WHERE email=<email>; 

