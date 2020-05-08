"""
@author: Thomason
@contact: ThomasonZhao810@gmail.com 
@create: 2020/5/2 8:48 AM 
"""


def get_page_list(paginator, page):
    page_list = []

    if paginator.num_pages > 10:
        if page.number <= 5:
            start_page = 1
        elif page.number > paginator.num_pages - 5:
            start_page = paginator.num_pages - 9
        else:
            start_page = page.number - 5

        for i in range(start_page, start_page + 10):
            page_list.append(i)
    else:
        for i in range(1, paginator.num_pages + 1):
            page_list.append(i)

    return page_list
