import datetime


class UserInputError(Exception):
    pass

def validate_book(title, author, year, isbn, publisher):

    if int(year) < 0:
        raise UserInputError("Error: ei voi olla negatiivinen.")
    
    if not title or not author or not publisher:
        raise UserInputError("Error: Title, author, and publisher cannot be empty.")

    if len(title) < 1 or len(title) > 100:  
        raise UserInputError("Error: Title must be between 1 and 100 characters long.")

    if len(str(year)) != 4 or not str(year).isdigit():
        raise UserInputError("Error: Year must be a four-digit number.")

    #if not (str(isbn).isdigit() and (len(str(isbn)) == 10 or len(str(isbn)) == 13)):
    #    raise UserInputError("Error: ISBN must be a 10 or 13 digit number.")

    if int(year) > datetime.datetime.now().year:
        raise UserInputError("Error: Year cannot be set to the future.")


def validate_article(title, author, year, doi=None, journal=None, volume=None, pages=None):
    if not title or not author:
        raise UserInputError("Error: Title and author cannot be empty.")

    if len(title) < 5 or len(title) > 100:
        raise UserInputError("Error: Title must be between 5 and 100 characters long.")

    if int(year) < 0:
        raise UserInputError("Error: Year cannot be negative.")
    
    if len(str(year)) != 4 or not str(year).isdigit():
        raise UserInputError("Error: Year must be a four-digit number.")
    
    if int(year) > datetime.datetime.now().year:
        raise UserInputError("Error: Year cannot be set to the future.")
    

def validate_inproceedings(title, author, booktitle, year):
    
    if not title or not author or not booktitle or not year:
        raise UserInputError("Error: Title, author, booktitle, and year cannot be empty.")

    if len(title) < 5 or len(title) > 100:
        raise UserInputError("Error: Title must be between 5 and 100 characters long.")

    if int(year) < 0:
        raise UserInputError("Error: Year cannot be negative.")
    
    if len(str(year)) != 4 or not str(year).isdigit():
        raise UserInputError("Error: Year must be a four-digit number.")
    
    if int(year) > datetime.datetime.now().year:
        raise UserInputError("Error: Year cannot be set to the future.")