import requests


def check_word(word: str, lang: str) -> bool:
    address = 'https://speller.yandex.net/services/spellservice.json/checkText'
    response = requests.get(f'{address}?text={word}&lang={lang}').json()
    if not response:
        return True
    elif response[0]['code'] == 1:
        return False
    return False


def main():
    print(check_word("hom", 'en'))
    pass


if __name__ == '__main__':
    main()

