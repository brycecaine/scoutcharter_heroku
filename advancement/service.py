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

def get_li_text(item):
    # Add text of a tag
    for e in item.findAll('a'):
        e.parent.insert(0, e.text)

    # Get remaining text, but not children tags (also excludes a tag above)
    text = ' '.join(' '.join(item.findAll(text=True, recursive=False)).split())

    return text

def ol_to_list(html_list):
    return_list = []
    # ---------- First loop ----------
    for idx1, item1 in enumerate(html_list.findAll('li', recursive=False), start=1):
        text1 = get_li_text(item1)

        list1 = item1.find(['ol', 'ul'])

        if list1:
            if text1:
                return_list.append((idx1, text1))

            # ---------- Second loop ----------
            for idx2, item1 in enumerate(list1.findAll('li', recursive=False), start=1):
                text2 = get_li_text(item1)

                list2 = item1.find(['ol', 'ul'])

                if list2:
                    if text2:
                        return_list.append(('%s.%s' % (idx1, idx2), text2))

                    # ---------- Third loop ----------
                    for idx3, item2 in enumerate(list2.findAll('li', recursive=False), start=1):
                        text3 = get_li_text(item2)
                        return_list.append(('%s.%s.%s' % (idx1, idx2, idx3), text3))

                else:
                    return_list.append(('%s.%s' % (idx1, idx2), text2))

        else:
            return_list.append((idx1, text1))

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
