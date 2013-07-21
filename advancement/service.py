from datetime import date

def get_birth_info(born_date, return_type):
    today = date.today()
    try: 
        birthday = born_date.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born_date.replace(year=today.year, day=born_date.day-1)

    if birthday > today:
    	if return_type == 'age':
        	return_val = today.year - born_date.year - 1
        elif return_type == 'next_birthday':
        	return_val = birthday

    else:
        if return_type == 'age':
        	return_val = today.year - born_date.year
        else:
        	return_val = born_date.replace(year=today.year+1)

    return return_val