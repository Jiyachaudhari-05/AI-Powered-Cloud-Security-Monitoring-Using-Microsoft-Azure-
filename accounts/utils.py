from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import make_password

def register_user(username, email, password):
    """
    Registers a new user if the username or email does not already exist.
    
    :param username: The username of the new user
    :param email: The email of the new user
    :param password: The password of the new user
    :return: A tuple (success, message)
    """
    try:
        # Check if the username or email already exists
        if User.objects.filter(username=username).exists():
            return False, "Username already taken"
        
        if User.objects.filter(email=email).exists():
            return False, "Email already registered"

        # Hash the password for security
        hashed_password = make_password(password)

        # Create the new user
        user = User.objects.create(username=username, email=email, password=hashed_password)
        user.save()
        
        return True, "User registered successfully"
    
    except Exception as e:
        return False, f"Error occurred: {str(e)}"
