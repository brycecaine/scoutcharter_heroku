from BeautifulSoup import BeautifulSoup
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

def ol_to_list(html_list):
	return_list = []
	for idx1, item in enumerate(html_list.findAll('li', recursive=False), start=1):
	    text = " ".join(item.find(text=True, recursive=False).split())

	    # print idx1, text

	    sublist = item.find(['ol', 'ul'])
	    if sublist:
		    if text:
			    return_list.append((idx1, text))
		    for idx2, subitem in enumerate(sublist.findAll('li', recursive=False), start=1):
			    text = " ".join(subitem.find(text=True, recursive=False).split())



			    sublist2 = subitem.find(['ol', 'ul'])
			    if sublist2:
				    if text:
					    return_list.append(('%s.%s' % (idx1, idx2), text))
				    for idx3, subitem2 in enumerate(sublist2.findAll('li', recursive=False), start=1):
					    text = " ".join(subitem2.find(text=True, recursive=False).split())
					    return_list.append(('%s.%s.%s' % (idx1, idx2, idx3), text))

			    else:
				    return_list.append(('%s.%s' % (idx1, idx2), text))

	    else:
		    return_list.append((idx1, text))

	return return_list











def ol_to_list_old(html_list, start_idx=''):
	return_list = []
	for i, item in enumerate(html_list.findAll('li', recursive=False), start=1):
	    text = " ".join(item.find(text=True, recursive=False).split())
	    idx = '%s.%s' % (start_idx, i)

	    # print idx, text

	    sublist = item.find(['ol', 'ul'])
	    if sublist:
		    subitems = sublist.findAll('li')
		    print subitems
		    if subitems:
			    return_list.append(ol_to_list(item, idx))

	    else:
		    return_list.append((idx, text))

	return return_list
