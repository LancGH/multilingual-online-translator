import requests
import sys
from bs4 import BeautifulSoup

lang_list = [
    'Arabic',
    'German',
    'English',
    'Spanish',
    'French',
    'Hebrew',
    'Japanese',
    'Dutch',
    'Polish',
    'Portuguese',
    'Romanian',
    'Russian',
    'Turkish'
]
language_1, language_2 = 0, 0
words = []
samples = []


def main():
    global language_1, language_2
    args = sys.argv
    try:
        language_1 = lang_list.index(args[1].capitalize())
    except ValueError:
        print(f"Sorry, the program doesn't support {args[1]}")
        sys.exit()
    word = args[3]
    if args[2] == 'all':
        print_all_words(word)
    else:
        try:
            language_2 = lang_list.index(args[2].capitalize())
        except ValueError:
            print(f"Sorry, the program doesn't support {args[2]}")
            sys.exit()
        print_words(word)


def print_words(word):
    global words, samples
    page_connect(parse_url(word, language_2))
    file_name = word + '.txt'
    with open(file_name, 'w', encoding='utf-8') as new_file:
        print(f'\n{lang_list[language_2]} Translations:')
        new_file.write(f'{lang_list[language_2]} Translations:\n')
        for word in words:
            print(word)
            new_file.write(word + '\n')
        print(f'\n{lang_list[language_2]} Examples:')
        new_file.write(f'\n{lang_list[language_2]} Examples:\n')
        for i in range(0, len(samples), 2):
            print(f'{samples[i]}\n{samples[i + 1]}')
            new_file.write(f'{samples[i]}\n{samples[i + 1]}\n')


def print_all_words(word):
    global words, samples
    page_connect(parse_url(word, language_2))
    words, samples = [], []
    file_name = word + '.txt'
    with open(file_name, 'w', encoding='utf-8') as new_file:
        for lang in range(len(lang_list)):
            if lang == language_1:
                continue
            page_connect(parse_url(word, lang))
            print(f'\n{lang_list[lang]} Translations:')
            print(words[0])
            new_file.write(f'\n{lang_list[lang]} Translations:\n')
            new_file.write(words[0] + '\n')
            print(f'\n{lang_list[lang]} Example:')
            print(f'{samples[0]}\n{samples[1]}\n')
            new_file.write(f'\n{lang_list[lang]} Example:\n')
            new_file.write(f'{samples[0]}\n{samples[1]}\n\n')
            words, samples = [], []


def parse_url(word, language_to):
    return 'https://context.reverso.net/translation/' + lang_list[language_1].lower()\
           + '-' + lang_list[language_to].lower() + '/' + word


def page_connect(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    if page.status_code == 404:
        print(f'Sorry, unable to find {sys.argv[3]}')
        sys.exit()
    elif page.status_code != 200:
        print('Something wrong with your internet connection')
        sys.exit()
    web_scrapping(page)


def web_scrapping(page):
    global words, samples
    soup = BeautifulSoup(page.content, 'html.parser')
    a_tags = soup.find_all('a', {'class': 'dict'})
    words = [clean_string(a.text) for a in a_tags]
    div_tags = soup.find_all('div', {'class': ['src', 'trg']})
    samples = [clean_string(div.text) for div in div_tags]


def clean_string(string):
    return string.replace('\n', '').replace('\r', '').lstrip()


if __name__ == '__main__':
    main()
