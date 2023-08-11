from natasha import (
    MorphVocab,
    NamesExtractor, AddrExtractor
)
from yargy import (
    Parser,
    rule, and_, or_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, in_,
    type, normalized,
    dictionary,
    gte, lte, gram
)
from yargy.pipelines import morph_pipeline, pipeline

from datetime import datetime

from yargy.tokenizer import MorphTokenizer, EOL

from src.resume.schemas import ResumeSchemaAdd
from src.config import STORAGE_PATH
import os


def parse_resume(data: str) -> ResumeSchemaAdd:
    INT = type('INT')
    COMMA = eq(',')
    COLON = eq(':')
    DASH = in_('-—')
    DOT = eq('.')

    """**********************ФИО**********************"""

    morph_vocab = MorphVocab()
    names_extractor = NamesExtractor(morph_vocab)
    fio = None
    for match in names_extractor(data):
        facts = match.fact
        if all((facts.first, facts.last, facts.middle)):
            fio = ' '.join([facts.last, facts.first, facts.middle])

    """**********************Телефон**********************"""

    Call = morph_pipeline([
        'телефон',
        'тел.'
    ])

    plus = eq('+')
    scob = in_('()')
    tr = eq('-')
    ddot = or_(eq(':'), eq(':'))

    Tel = rule(
        rule(plus).optional(),
        rule(INT),
        rule(scob).optional(),
        rule(INT).optional(),
        rule(scob).optional(),
        rule(INT).optional(),
        rule(tr).optional(),
        rule(INT).optional(),
        rule(tr).optional(),
        rule(INT).optional()
    )

    TELEPHONE = rule(
        Call,
        rule(ddot).optional(),
        Tel
    )
    parser = Parser(TELEPHONE)
    phone = None
    for match in parser.findall(data):
        start, stop = match.span
        phone = data[start:stop]

    """**********************Почта**********************"""

    email = ''.join([x.strip(',.') for x in data.split() if '@' in x])

    """**********************Пол**********************"""

    GENDERS = {
        'Женщина': 2,
        'Жен.': 2,
        'Жен': 2,
        'Мужчина': 1,
        'Муж.': 1,
        'Муж': 1
    }
    GENDER = rule(in_(GENDERS))

    parser = Parser(GENDER)
    gender = None
    for match in parser.findall(data):
        start, stop = match.span
        gender = data[start:stop]

    """**********************Дата рождения**********************"""

    MONTHS = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }
    MONTH_NAME = dictionary(
        MONTHS
    )
    DAY = and_(
        gte(1),
        lte(31)
    )
    YEAR = and_(
        gte(1900),
        lte(2100)
    )
    DATE = rule(
        DAY,
        MONTH_NAME,
        YEAR
    )
    BIRTH = rule(
        morph_pipeline(['родиться', 'дата рождения', 'дата рождения:']),
        DATE
    )

    parser = Parser(BIRTH)
    date_of_birth = None
    for match in parser.findall(data):
        start, stop = match.span
        date_of_birth = data[start:stop]

    try:
        date_of_birth = date_of_birth.split()[1:]
        date_of_birth[1] = MONTHS.get(date_of_birth[1])
    except Exception as _ex:
        print(_ex)

    """**********************Возраст**********************"""

    day, month, year = map(int, date_of_birth)
    today = datetime.today()
    age = today.year - year - ((today.month, today.day) < (month, day))

    """**********************Занятость**********************"""

    TITLE = morph_pipeline(['Занятость:', 'Занятость'])
    TYPES = {
        'полная': 'full',
        'полная занятость': 'full',
        'частичная': 'part',
        'частичная занятость': 'part',
        'волонтерство': 'volunteer',
        'стажировка': 'intern',
        'проектная работа': 'project'
    }
    TYPE = morph_pipeline(TYPES)

    TYPES = rule(
        TYPE,
        rule(
            COMMA,
            TYPE
        ).optional().repeatable()
    )
    EMPLOYMENT = rule(
        TITLE,
        TYPES
    )
    REVERSE_EMPLOYMENT = rule(
        TYPES, TITLE
    )

    parser = Parser(or_(EMPLOYMENT, REVERSE_EMPLOYMENT))
    for match in parser.findall(data):
        start, stop = match.span
        employment = data[start:stop]

    """**********************График работы**********************"""

    TITLE = morph_pipeline(['График работы:', 'График работы'])
    TYPES = {
        'полный день': 'full',
        'сменный график': 'part',
        'вахтовый метод': 'vahta',
        'гибкий график': 'flex',
        'удаленная работа': 'remote',
        'стажировка': 'intern'
    }
    TYPE = morph_pipeline(TYPES)
    TYPES = rule(
        TYPE,
        rule(
            COMMA,
            TYPE
        ).optional().repeatable()
    )
    SCHEDULE = rule(
        TITLE,
        TYPES
    )

    parser = Parser(SCHEDULE)
    for match in parser.findall(data):
        start, stop = match.span
        schedule = data[start:stop]

    """**********************Образование**********************"""

    TITLE = morph_pipeline(['Образование:', 'Образование'])
    TYPES = {
        'основное общее': 'basic general',
        'среднее общее': 'average general',
        'среднее': 'average',
        'среднее профессиональное': 'secondary vocational',
        'среднее специальное': 'secondary special',
        'бакалавриат': 'bachelor',
        'бакалавр': 'bachelor',
        'специалитет': 'specialty',
        'магистратура': 'magistracy',
        'высшее': 'higher'
    }
    TYPE = morph_pipeline(TYPES)
    TYPES = rule(
        TYPE,
        rule(
            COMMA,
            TYPE
        ).optional().repeatable()
    )
    EDUCATION = rule(
        TITLE, TYPES
    )
    REVERSE_EDUCATION = rule(
        TYPES, TITLE
    )

    parser = Parser(or_(EDUCATION, REVERSE_EDUCATION))
    education = None
    for match in parser.findall(data):
        start, stop = match.span
        education = data[start:stop].lower()

    """**********************Знание языков**********************"""

    TITLE = morph_pipeline(['Знание языков:', 'Знание языков'])
    TYPES_LANGUAGES = {
        'русский': 'russian',
        'китайский': 'chinese',
        'английский': 'english',
        'французский': 'french',
        'немецкий': 'german'
    }
    TYPE = morph_pipeline(TYPES_LANGUAGES)
    LEVELS = {
        'родной': 'native',
        'базовые знания': 'base',
        'могу проходить интервью': 'interview'
    }
    LEVEL = morph_pipeline(LEVELS)
    ONE_LANGUAGE = rule(TYPE, DASH.optional(), LEVEL.optional())
    TYPES = rule(
        ONE_LANGUAGE,
        rule(
            COMMA.optional(),
            ONE_LANGUAGE
        ).optional().repeatable()
    )
    LANGUAGES = rule(
        TITLE, TYPES
    )

    parser = Parser(LANGUAGES)
    languages = []
    for match in parser.findall(data):
        for token in match.tokens:
            if token.value.lower() in TYPES_LANGUAGES.keys():
                languages.append(token.value)

    """**********************Должность**********************"""

    def load_lines(path):
        with open(path, encoding='utf-8') as file:
            for line in file:
                yield line.rstrip('\n')

    SPECIALIZATIONS = set(load_lines(os.path.join(STORAGE_PATH, 'specialization.txt')))
    SUBSPECIALIZATIONS = set(load_lines(os.path.join(STORAGE_PATH, 'subspecialization.txt')))

    TITLE = morph_pipeline([
        'Желаемая должность и зарплата',
        'Желаемая должность: ',
        'Должность',
        'Работать',
        'сфера'
    ])

    DOT = eq('•')

    SUBTITLE = not_(DOT).repeatable()

    SPECIALIZATION = pipeline(SPECIALIZATIONS)

    SUBSPECIALIZATION = pipeline(SUBSPECIALIZATIONS)

    ITEM = rule(
        rule(DOT).optional(),
        or_(
            SPECIALIZATION,
            SUBSPECIALIZATION
        )
    )

    TOKENIZER = MorphTokenizer().remove_types(EOL)
    POSITION = rule(
        TITLE,
        rule(SUBTITLE).optional(),
        ITEM.repeatable()
    )

    parser = Parser(POSITION, tokenizer=TOKENIZER)
    profession = None
    for match in parser.findall(data):
        start, stop = match.span
        profession = data[start:stop]

    """**********************Желаемая зарплата**********************"""

    Money = fact(
        'Money',
        ['amount', 'currency'],
    )

    CURRENCIES = {
        'руб.': 'RUB',
        'грн.': 'GRN',
        'бел. руб.': 'BEL',
        'RUB': 'RUB',
        'EUR': 'EUR',
        'KZT': 'KZT',
        'USD': 'USD',
        'KGS': 'KGS',
        'рублей': 'RUB'
    }

    CURRENCIE = {
        'тыс.': 'тысяча',
        'млн.': 'миллион'
    }

    CURRENCY = pipeline(CURRENCIES).interpretation(
        Money.currency.normalized().custom(CURRENCIES.get)
    )

    R_1 = rule(gram('ADJF'),
               dictionary({'оплата', 'зарплата', 'оклад', 'доход'}))

    CURRENCy = pipeline(CURRENCIE).interpretation(
        Money.currency.normalized().custom(CURRENCIE.get)
    )

    def normalize_amount(value):
        return int(value.replace(' ', ''))

    AMOUNT = or_(
        rule(INT),
        rule(INT, INT),
        rule(INT, INT, INT),
    ).interpretation(
        Money.amount.custom(normalize_amount)
    )

    MONEY = rule(
        AMOUNT,
        CURRENCy.optional(),
        CURRENCY,
    )

    parser = Parser(or_(MONEY, R_1))
    for match in parser.findall(data):
        start, stop = match.span
        salary = data[start:stop]

    """**********************Опыт работы**********************"""

    TITLE = rule(morph_pipeline(['Опыт работы']), DASH)
    YEAR = rule(INT, normalized('год').optional()).optional()
    MONTH = rule(INT, normalized('месяц').optional())
    EXPERIENCE = rule(TITLE, YEAR, MONTH.optional())

    parser = Parser(EXPERIENCE)
    experience = None
    for match in parser.findall(data):
        start, stop = match.span
        experience = data[start:stop]

    """**********************Адрес проживания**********************"""

    addr_extractor = AddrExtractor(morph_vocab)

    matches = addr_extractor(data)
    facts = [i.fact.as_json for i in matches]
    for i in range(len(facts)):
        tmp = list(facts[i].values())
        break
    if len(tmp) == 2:
        match = (tmp[1], ':', tmp[0])
    else:
        match = (tmp[0],)
    city = " ".join(match)

    """**********************Общий вывод**********************"""
    fio = fio if fio else ""
    date_of_birth = datetime.strptime('.'.join(date_of_birth),
                                      '%d.%m.%Y').date() if date_of_birth else datetime.now().date()
    gender = GENDERS.get(gender) if gender else 3
    phone = phone.lower().replace(': ', '').replace('телефон', '') if phone else ""
    email = email if email else ""
    # resume = ResumeSchemaAdd(
    #     id_resume_file=-1,
    #     fio=fio,
    #     date_of_birth=date_of_birth,
    #     gender=gender,
    #     phone=phone,
    #     email=email,
    #     experience=experience,
    #     education=education
    # )

    return [fio, date_of_birth, gender, phone, email, experience.lower().replace('опыт работы', '').replace(" — ", ""), education, profession.lower().replace('желаемая должность и зарплата', '').replace(' •', ',').replace(' ,', ',')]
