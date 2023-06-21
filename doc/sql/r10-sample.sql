# SQL Samples for R10: User Registration & Login

# Create user
INSERT INTO user (name, password, email, registration_date) VALUES("Betty Crocker", "hashed_pw", "betty@crocker.com", CURRENT_TIMESTAMP);
# Check email
SELECT email, password FROM user WHERE email="betty@crocker.com"; 
