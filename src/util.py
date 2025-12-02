import datetime


class UserInputError(Exception):
    pass

def validate_book(title, author, year, isbn, publisher):

    if int(year) < 0:
        raise UserInputError("Error: ei voi olla negatiivinen.")

    if len(title) < 1 or len(title) > 20:  
        raise UserInputError("Error: Title must be between 5 and 200 characters long.")

    if len(str(year)) != 4 or not str(year).isdigit():
        raise UserInputError("Error: Year must be a four-digit number.")

    if not (str(isbn).isdigit() and (len(str(isbn)) == 10 or len(str(isbn)) == 13)):
        raise UserInputError("Error: ISBN must be a 10 or 13 digit number.")

    if int(year) > datetime.datetime.now().year:
        raise UserInputError("Error: Year cannot be set to the future.")
