import requests
import json
from settings import proxies, login_l2, password_l2, IMPLANT_FIELDS, GOOGLE_KEY

import gspread


session = requests.Session()
session.proxies.update(proxies)


def get_patients_from_table(interval: str) -> list:
    """Получение списка номеров выписанных историй из сводной гугл-таблицы"""
    gs = gspread.service_account(filename='utils/jsonS/access.json')
    sh = gs.open_by_key(GOOGLE_KEY)

    worksheet = sh.get_worksheet_by_id(0)
    result = []
    for item in worksheet.get(interval):
        if len(item) > 0:
            result.append(item[0])
    return result


def authorization_l2(connect, login, password):
    """Авторизация в L2"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/login',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'username': f'{login}',
        'password': f'{password}',
        'totp': '',
    }

    response = connect.post('http://192.168.10.161/api/users/auth', headers=headers, json=json_data, verify=False)
    return response.status_code, response.json(), response.cookies


def get_all_favorites(connect):
    """Получение историй из Избранное"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/all-directions-in-favorites',
        headers=headers,
        json={},
        verify=False,
    )
    return response.json()


def get_all_pk_history(connect, number):
    """Получение всех номеров направлений в истории"""

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }

    json_data = {
        'direction': number,
        'r_type': 'all',
        'every': False,
    }

    response = connect.post(
        'http://192.168.10.161/api/stationar/directions-by-key',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def get_initial_examination(connect, pk_researches: int):
    """Получение данных из первичного осмотра"""
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'direction': pk_researches,  # номер истории
        'r_type': 'primary receptions',
        'every': False,
    }

    response = connect.post(
        'http://192.168.10.161/api/stationar/directions-by-key',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def get_history_content(connect, number):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'X-KL-kav-Ajax-Request': 'Ajax_Request',
    }

    json_data = {
        'pk': number,  # номер направления, не истории
        'force': True,
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/paraclinic_form',
        headers=headers,
        json=json_data,
        verify=False,
    )

    return response.json()


def obtain_research_data(connect, pk_desc: int):

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Content-Type': 'application/json',
        'DNT': '1',
        'Origin': 'http://192.168.10.161',
        'Proxy-Connection': 'keep-alive',
        'Referer': 'http://192.168.10.161/ui/stationar',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    }

    json_data = {
        'pk': pk_desc,
        'force': True,
    }

    response = connect.post(
        'http://192.168.10.161/api/directions/results',
        headers=headers,
        json=json_data,
        verify=False,
    )
    return response.json()


def get_result_obtains(index_number: int) -> str:
    """Возвращает результаты исследования по номеру направления"""
    obtain = obtain_research_data(session, index_number)
    result = f"\n{obtain.get('direction').get('date')} "
    for item in obtain.get('results').values():
        result += item.get('title')
        for i in item.get('fractions').values():
            index = f'\n{i.get("title")} {i.get("result")}{i.get("units")}'
            result += index
    return result


def extract_patient_data_from_L2(history_number: int) -> dict:

    discharge_summary = {
        'Анализы': '',
        'Протоколы операций': []
    }

    authorization_l2(session, login_l2, password_l2)  # авторизация в L2

    history = get_history_content(session, history_number)  # все данные по истории болезни
    directions = history.get('researches')[0].get('children_directions')  # номера направлений всех записей в истории болезни

    fio = history.get('patient').get('fio_age').split(',')[0]
    birthday = history.get('patient').get('fio_age').split(',')[2]

    discharge_summary['Фамилия'] = fio.split(' ')[0]
    discharge_summary['Имя'] = fio.split(' ')[1]
    discharge_summary['Отчество'] = fio.split(' ')[2]
    discharge_summary['Дата рождения'] = birthday.strip().split()[0]

    for direction in directions:
        if direction.get('services') == ['Первичный осмотр']:
            data = get_history_content(session, direction.get('pk'))
            for group in data.get('researches')[0].get('research').get('groups'):
                if group.get('title') == 'Анамнез заболевания':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key == 'Диагноз направившего учреждения' and value != '':
                            discharge_summary[key] = value
                        elif item.get('pk') == 18733 and value != '- Не выбрано':
                            discharge_summary[key] = value
                            with open('jsonS/hospitals.json', 'r') as file:
                                hospitals = json.load(file)
                                hospital = hospitals.get(value)
                                discharge_summary['Org_id'] = hospital.get('Org_id')
                        elif key == 'Виды транспортировки' and value != '':
                            discharge_summary[key] = value

                        elif key == 'Номер направления' and value != '':
                            discharge_summary[key] = value

                        elif (
                                key == 'Дата выдачи направления' and
                                value != '' and
                                discharge_summary.get('Вид госпитализации') == 'плановая'
                        ):
                            value = '.'.join(value.split('-')[::-1])
                            discharge_summary[key] = value
                        elif key == 'Вид госпитализации' and value != '':
                            discharge_summary[key] = value
        elif direction.get('services') == ['Протокол операции (тр)']:
            operation_info_for_append = {}
            data = get_history_content(session, direction.get('pk'))
            operation_info = data.get('researches')[0].get('research').get('groups')
            for index in range(0, len(operation_info)):
                for item in operation_info[index].get('fields'):
                    if item.get('title') == 'Дата проведения':
                        operation_date = '.'.join(item.get('value').split('-')[::-1])
                        operation_info_for_append['Дата проведения'] = operation_date
                    elif item.get('title') == 'Время начала':
                        if len(item.get('value')) == 5 and ':' in item.get('value'):
                            operation_time_start = item.get('value')
                        elif '.' in item.get('value'):
                            operation_time_start = item.get('value').replace('.', ':')
                        elif '-' in item.get('value'):
                            operation_time_start = item.get('value').replace('-', ':')
                        elif len(item.get('value')) < 4:
                            operation_time_start = f'0{item.get("value")}'
                        else:
                            operation_time_start = 'Не верно указано время начала операции'
                        operation_info_for_append['Время начала'] = operation_time_start
                    elif item.get('title') == 'Время окончания':
                        if len(item.get('value')) == 5 and ':' in item.get('value'):
                            operation_time_end = item.get('value')
                        elif '.' in item.get('value'):
                            operation_time_end = item.get('value').replace('.', ':')
                        elif len(item.get('value')) < 4:
                            operation_time_end = f'0{item.get("value")}'
                        else:
                            operation_time_end = 'Не верно указано время окончания операции'
                        operation_info_for_append['Время окончания'] = operation_time_end
                    elif item.get('title') == 'Название операции':
                        operation_info_for_append['Название операции'] = item.get('value')
                    elif item.get('title') == 'Код операции':
                        operation_info_for_append['Код операции'] = item.get('value')
                    elif item.get('title') == 'Категория сложности':
                        operation_info_for_append['Категория сложности'] = item.get('value')
                    elif item.get('title') == 'Оперативное вмешательство' and item.get('pk') == 1994:
                        operation_info_for_append['Категория сложности'] = item.get('value')
                    elif item.get('title') == 'Оперировал':
                        operation_info_for_append['Оперировавший хирург'] = item.get('value')
                    elif item.get('title') == 'Ассистенты':
                        operation_info_for_append['Ассистенты'] = item.get('value')
                    elif item.get('title') == 'Анестезиолог':
                        operation_info_for_append['Анестезиолог'] = item.get('value')
                    elif item.get('title') == 'Анестезист':
                        operation_info_for_append['Анестезист'] = item.get('value')
                    elif item.get('title') == 'Операционная медицинская сестра':
                        if item.get('value') != '':
                            operation_info_for_append['Операционная медицинская сестра'] = item.get('value')
                    elif item.get('pk') == 1873:
                        operation_info_for_append['Ход операции'] = item.get('value')
                    elif item.get('title') == 'Метод обезболивания':
                        operation_info_for_append['Вид анестезии'] = item.get('value')
                    elif item.get('title') == 'Осложнения':
                        operation_info_for_append['Осложнения'] = item.get('value')
                    elif item.get('title') == 'Количество использованных металлоконструкций':
                        operation_info_for_append['Количество имплантов'] = item.get('value')
                        operation_info_for_append['Импланты'] = []
                    elif item.get('pk') in IMPLANT_FIELDS:
                        if item.get('value') != '- Не выбрано':
                            operation_info_for_append['Импланты'].append(item.get('value'))
            discharge_summary['Протоколы операций'].append(operation_info_for_append)

        elif direction.get('services') == ['Выписка -тр']:
            data = get_history_content(session, direction.get('pk'))
            who_confirmed = data.get('patient').get('doc').split(' ')[0]
            discharge_summary['Лечащий врач'] = who_confirmed
            groups = data.get('researches')[0]
            for group in groups.get('research').get('groups'):
                if group.get('title') == 'Дата и время поступления':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            discharge_summary[key] = value
                elif group.get('title') == 'Дата и время выписки':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            if key == 'Время выписки':
                                discharge_summary[key] = value
                            elif key == 'Дата выписки':
                                value = '.'.join(value.split('-')[::-1])
                                discharge_summary[key] = value
                elif group.get('title') == 'Результат лечения':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            discharge_summary[key] = value
                elif group.get('title') == 'Диагноз заключительный клинический':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            if key == 'Основной диагноз по МКБ':
                                discharge_summary[key] = value.split()[0]
                            else:
                                discharge_summary[key] = value
                elif group.get('title') == 'Проведенное обследование':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            discharge_summary[key] = value
                elif group.get('title') == 'Проведенное лечение':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            discharge_summary[key] = value
                elif group.get('title') == 'Рекомендации':
                    for item in group.get('fields'):
                        key = item.get('title')
                        value = item.get('value')
                        if key != '' and value != '':
                            discharge_summary[key] = value
        if direction.get('services')[0] in ['Общий анализ мочи',
                                            'Калий,  натрий',
                                            'Полный гематологический анализ',
                                            'Общий белок', 'Глюкоза(г)',
                                            'Билирубин общий',
                                            'Билирубин связанный (прямой)',
                                            'Билирубин свободный (непрямой)']:
            data = get_result_obtains(direction.get('pk'))
            discharge_summary['Анализы'] += data
    return discharge_summary
