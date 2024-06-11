import wikipediaapi
import requests

def wiki_search(search_str: str) -> None:
    wiki_wiki = wikipediaapi.Wikipedia('get_info (wesene9608@hutov.com)', 'en')

    page_py = wiki_wiki.page(search_str)
    if page_py.exists() == True:
        with open("wiki_search.txt", "a") as file:
            file.write("Title: %s \n" % page_py.title)
            file.write("Summary: %s \n" % page_py.summary[0:-1])
            file.write("------------------------------------ \n")
    else:
        print("Wiki page doesn't exist.")


if __name__ == '__main__':
    wiki_search('Python_(programming_language)')