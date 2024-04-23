import re

def validateFormData(formData):
    # Check if all fields are filled
    for key in formData:
        if not formData[key]:
            return 'Please fill in all fields'

    # Check if Name contains only letters
    nameRegex = '^[A-Za-z]+$'
    if not re.match(nameRegex, formData['firstName']) or not re.match(nameRegex, formData['lastName']):
        return 'Name should only contain letters'

    # Check if username is valid
    usernameRegex = '^(?=.*[a-zA-Z])[a-zA-Z0-9_]+$'
    if not re.match(usernameRegex, formData['username']):
        return 'Username should not contain only numbers or special characters!'

    # Email format validation using regular expression
    emailRegex = '^\S+@\S+\.\S+$'
    if not re.match(emailRegex, formData['email']):
        return 'Invalid email address'

    # Password length check
    if len(formData['password']) < 8:
        return 'Password should be at least 8 characters long'

    # Check if password contains both letters and numbers
    passwordRegex = '^(?=.*[a-zA-Z])(?=.*\d).+$'
    if not re.match(passwordRegex, formData['password']):
        return 'Password should contain both letters and numbers'

    # Check if passwords match
    if formData['password'] != formData['confirmPassword']:
        return 'Password and Confirm Password don\'t match. Try again!'

    # If all validations pass
    return None