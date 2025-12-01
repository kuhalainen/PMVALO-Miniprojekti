class UserInputError(Exception):
    pass

def validate_book(title, author, year, isbn, publisher):
    
    if int(year) < 0:
          raise UserInputError("Error: ei voi olla negatiivinen.")

    if len(title) < 1 or len(title) > 20:  
        raise UserInputError("Error: Title must be between 5 and 200 characters long.")

    if len(year) != 4 or not year.isdigit():
        raise UserInputError("Error: Year must be a four-digit number.")
    
    