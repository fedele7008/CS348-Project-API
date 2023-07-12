# SQL templates for R10: User Registration & Login

### Add a UNIQUE INDEX on email
CREATE UNIQUE INDEX user_email ON user(email);

### Register user
INSERT INTO user (name, password, email, registration_date) 
VALUES(<name>, <hashed_password>, <email>, CURRENT_TIMESTAMP);

### Log in
# application will verify if password matches inputted password
SELECT email, password FROM User WHERE email=<email>; 

### Example queries
INSERT INTO user (name, password, email, registration_date) VALUES("Betty Crocker", "hashed_pw", "betty@crocker.com", CURRENT_TIMESTAMP);
SELECT email, password FROM user WHERE email="betty@crocker.com"; 