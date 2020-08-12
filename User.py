import re


class PasswordTooShort(Exception):
    "PasswordTooShort is an is an Exception that raises when the provided argument is too short"""

    def __init__(self, length):
        self._length = length

    def __str__(self):
        return "The password's length %s is shorter then 8" % self._length


class PasswordTooLong(Exception):
    """PasswordTooLong  is an is an Exception that raises when the provided argument is too long"""

    def __init__(self, length):
        self._length = length

    def __str__(self):
        return "The password's length %s is longer then 40" % self._length


class PasswordMissingCharacter(Exception):
    """PasswordMissingCharacter  is an is an Exception that raises when
    the provided argument is missing a specific char"""

    def __init__(self, missing_criteria, password):
        self._missing_criteria = missing_criteria
        self._password = password

    def __str__(self):
        return "The password {0} is missing a {1}".format(self._password, self._missing_criteria)


class User:
    def __init__(self, email, password, user_id=None, first_name="", last_name=""):
        if check_user(email, password):
            self._email = email
            self._password = password
            self._user_id = user_id
            self._first_name = first_name
            self._last_name = last_name

    def __str__(self):
        return "User[email= " + self._email + ", password= " + self._password + ", user_id= " \
               + str(self._user_id) + ", first_name= " + self._first_name + \
               ", last_name= " + self._last_name + "]"

    def get_email(self):
        return self._email

    def get_id(self):
        return self._user_id


def check_user(email, password):
    try:
        return check_email(email=email) and check_password(password)
    # TODO Handle exceptions
    except(Exception):
        pass


def check_email(email):
    check = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return re.search(check, email)


def check_password(password):
    if len(password) < 8:
        raise PasswordTooShort(len(password))
    elif len(password) > 40:
        raise PasswordTooLong(len(password))
    elif not any(char.isupper() for char in password):
        raise PasswordMissingCharacter(password=password, missing_criteria="an upper letter")
    elif not any(char.islower() for char in password):
        raise PasswordMissingCharacter(password=password, missing_criteria="a lower letter")
    elif not any(char.islower() for char in password):
        raise PasswordMissingCharacter(password=password, missing_criteria="a digit ")
    else:
        return True


def main():
    pass


if __name__ == '__main__':
    main()
