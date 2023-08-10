from natasha import (
    MorphVocab,
    NamesExtractor, AddrExtractor
)
from yargy import (
    Parser,
    rule, and_, or_
)
from yargy.interpretation import fact
from yargy.predicates import (
    eq, in_,
    type, normalized,
    dictionary,
    gte, lte, gram
)
from yargy.pipelines import morph_pipeline, pipeline

from pydantic import BaseModel
from typing import List
from datetime import datetime


class Person(BaseModel):
    fio: str = None
    age: int = None
    date_of_birth: str = None
    gender: str = None
    city: str = None
    salary: str = None
    profession: str = None
    experience: str = None
    employment: str = None
    schedule: List[str] = None
    education: str = None
    languages: List[str] = None
    phone: str = None
    email: str = None


def parser_resume(data: str):
    global gender, age, date, employment, schedule, education, salary, experience, fio, profession, phone

    INT = type('INT')
    COMMA = eq(',')
    COLON = eq(':')
    DASH = in_('-—')
    DOT = eq('.')

    """**********************ФИО**********************"""

    morph_vocab = MorphVocab()
    names_extractor = NamesExtractor(morph_vocab)

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
    for match in parser.findall(data):
        start, stop = match.span
        phone = data[start:stop]

    """**********************Почта**********************"""

    email = ''.join([x.strip(',.') for x in data.split() if '@' in x])

    """**********************Пол**********************"""

    GENDERS = {
        'Женщина': 'женщина',
        'Жен.': 'женщина',
        'Жен': 'женщина',
        'Мужчина': 'мужчина',
        'Муж.': 'мужчина',
        'Муж': 'мужчина'
    }
    GENDER = rule(in_(GENDERS))

    parser = Parser(GENDER)
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
    for match in parser.findall(data):
        start, stop = match.span
        date = data[start:stop]

    try:
        date = date.split()[1:]
        date[1] = MONTHS.get(date[1])
    except Exception as _ex:
        print(_ex)

    """**********************Возраст**********************"""

    day, month, year = map(int, date)
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

    # def load_lines(path):
    #     with open(path, encoding='utf-8') as file:
    #         for line in file:
    #             yield line.rstrip('\n')
    #
    # SPECIALIZATIONS = set(load_lines(os.path.join(STORAGE_DIR, 'specialization.txt')))
    # SUBSPECIALIZATIONS = set(load_lines(os.path.join(STORAGE_DIR, 'subspecialization.txt')))
    #
    # TITLE = morph_pipeline([
    #     'Желаемая должность и зарплата',
    #     'Желаемая должность: ',
    #     'Должность',
    #     'Работать',
    #     'сфера'
    # ])
    #
    # DOT = eq('•')
    #
    # SUBTITLE = not_(DOT).repeatable()
    #
    # SPECIALIZATION = pipeline(SPECIALIZATIONS)
    #
    # SUBSPECIALIZATION = pipeline(SUBSPECIALIZATIONS)
    #
    # ITEM = rule(
    #     rule(DOT).optional(),
    #     or_(
    #         SPECIALIZATION,
    #         SUBSPECIALIZATION
    #     )
    # )
    #
    # POSITION = rule(
    #     TITLE,
    #     rule(SUBTITLE).optional(),
    #     ITEM.repeatable()
    # )
    #
    # TOKENIZER = MorphTokenizer().remove_types(EOL)
    #
    # parser = Parser(POSITION, tokenizer=TOKENIZER)
    # for match in parser.findall(data):
    #     start, stop = match.span
    #     profession = data[start:stop]

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
    YEAR = rule(INT, normalized('год').optional())
    MONTH = rule(INT, normalized('месяц'))
    EXPERIENCE = rule(TITLE, YEAR, MONTH.optional())

    parser = Parser(EXPERIENCE)
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

    person = Person()
    try:
        person.fio = fio
    except Exception as _ex:
        print(_ex)
    try:
        person.gender = GENDERS.get(gender)
    except Exception as _ex:
        print(_ex)
    try:
        person.date_of_birth = '.'.join(date)
    except Exception as _ex:
        print(_ex)
    try:
        person.age = age
    except Exception as _ex:
        print(_ex)
    try:
        person.employment = ' '.join(employment.split()[1:])
    except Exception as _ex:
        print(_ex)
    try:
        person.schedule = ' '.join(schedule.split()[2:]).split(', ')
    except Exception as _ex:
        print(_ex)
    try:
        person.education = ' '.join(education.split()[1:])
    except Exception as _ex:
        print(_ex)
    try:
        person.languages = languages
    except Exception as _ex:
        print(_ex)
    try:
        person.salary = salary.replace(' ', '')
    except Exception as _ex:
        print(_ex)
    try:
        experience = experience.lower().replace('опыт работы', '')
        person.experience = ' '.join(experience.split()[1:])
    except Exception as _ex:
        print(_ex)
    try:
        profession = profession.lower().replace('желаемая должность и зарплата', '').replace(' •', ',').replace(' ,',
                                                                                                                ',')
        person.profession = ' '.join(profession.split()).strip()
    except Exception as _ex:
        print(_ex)
    try:
        phone = phone.lower().replace(': ', '').replace('телефон', '')
        person.phone = phone
    except Exception as _ex:
        print(_ex)
    try:
        person.email = email
    except Exception as _ex:
        print(_ex)
    try:
        person.city = city
    except Exception as _ex:
        print(_ex)

    return person


if __name__ == '__main__':
    data = 'Углов Иван Иванович. Мужчина, 30 лет, родился 11 октября 1985 Телефон: +79509708570 Почта: fad.ghex_1432@gmail.com Проживает: Москва, м. Дмитровская Гражданство: Россия, есть разрешение на работу: Россия Не готов к переезду, готов к редким командировкам Желаемая должность и зарплата Личный охранник (Телохранитель) Безопасность • Личная безопасность • Охранник Занятость: полная занятость График работы: полный день Желательное время в пути до работы: не имеет значения 100 000 руб. Опыт работы — 8 лет 11 месяцев Август 2015 — настоящее время 1 год 2 месяца Витязь, Концерн безопасности Москва, www.kb-vityaz.com/ Личный охранник Личная охрана, работа 1-2 номером осуществления безопасности главы г.Химки ,   иногда выполнение функции водителя.  *Работа в группе охраны и в одиночку *Выполнение личных поручений *Сопровождение VIP лица и членов  семьи *Выполнение личных поручений *Работа со служебным оружием *Работа в команде *Работа 1-2 номером *Наличие УЧО 6 разряд Июль 2009 — Май 2015 5 лет 11 месяцев ЧОП “Вымпел НОРД” г Москва. Москва Личный охранник Работал  личным охранником 1-2 номером , охранником-водителем в Обязанности *Личная охрана, сопровождение VIP лица и семьи *Выполнение личных поручений, работа с документами ПК и орг.техникой *Работа со служебным оружием *Работа в команде *Работа 1-2 номером *Наличие УЧО 6 разряд *Наличие прав АВС ,8 лет стаж вождения. *Владею всеми видами оружия *Есть опыт  обучение охранников ( новичков ) *Решение орг.вопросов, управление персоналом 7-10 человек . Май 2008 — Май 2009 1 год 1 месяц ВВ МВД  604 Отряд Специального Назначения " Витязь" Москва Заместитель командира взвода Резюме обновлено 20 августа 2016 в 11:07 [image: image0.png][image: image1.png] *Управление личным составом до 25 человек * Проведения учебных занятий * Написание учебных планов * Проведение практических занятий -спортивно – массовых мероприятий - работа с огнестрельным оружием -физической подготовки и боевым единоборствам -морально - психологической  подготовки * В 2008 году прошел  обучения "Школа экстремального вождения ВС" *В 2008 г. 12 декабря Сдал квалификационные экзамены специальной подготовки  "Жетон Витязь" норматив как на "карповый берет" *В 2009 году участвовал в контртеррористической операции в СКО р. Дагестан участник боевых действий. * Есть награды за отличие в службе * 22 мая 2009 г был уволен в запас Август 2007 — Май 2008 10 месяцев Таврическая Автошкола Омской области Омская область Заместитель директора по воспитательной работе * Организация учебного процесса * Организация  и проведения спортивно -массовых  мероприятий * Написание учебных планов и расписаний * Проведение обучающих процессов * Есть опыт создания с нуля материальной-технической базы * Организаций  посещения культурных мероприятий Образование Среднее специальное 2016 Учебный ЦСН Альфа Личная охрана 2015 Учебный центр Витязь Телохранитель, Телохранитель 2012 Омский государственный педагогический университет, Омск Факультет психологии и педагогики, Педагогика и психология 2007 ГОУ СПО СППК Мастер производственного обучения, Прикладная механика Повышение квалификации, курсы 2015 Учебный центр Витязь Учебный центр Витязь, Телохранитель Ключевые навыки Знание языков Русский — родной Английский — базовые знания Навыки  Управление командой      Деловая коммуникация      Адаптация   Экстремальное вождение      Работа в команде      Обучение и развитие     •  Резюме обновлено 20 августа 2016 в 11:07  Управление персоналом      Руководство коллективом      Кадровое делопроизводство   Обучение персонала      Охрана объекта      Организаторские навыки   Подбор персонала      Планирование      Мотивация персонала      Пользователь ПК   Контроль исполнения  решений      MS Outlook  Дополнительная информация Обо мне Интересует работа в дружной команде профессионалов. Высокий уровень физической и психологической подготовки; РУКОПАШНЫЙ БОЙ, Самбо. Результаты на сегодня 3км -13м. турник 20 р. купер 5кругов за 5м. Люблю музыку, велосипедный спорт, бегать в парке 2-3 раза в неделю, путешествовать, общаться с интересными людьми.  Чистое прошлое в перспективное будущее. Я не святой, да и не встречал))) Ценю ответственность, честность, порядочность и целеустремленность в людях.    •  Резюме обновлено 20 августа 2016 в 11:07 '
    print(parser_resume(data))
