from settings import XML_TEMPLATE_ID_OPERATION


def save_changes(connect):
    """Сохраните внесенные данные (опционально)"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnMediaFiles',
        'm': 'saveChanges',
    }

    data = {
        'Evn_id': '380101342738885',  # ???
        'changedData': '',
        'saveOnce': 'true',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_info_for_operation(connect):
    """Информация для протокола операции. Ключи:
    OperDiff - категория сложности. Параметры OperDiff_id, OperDiff_code
    OperType - плановая/экстренная/срочная. Параметры OperType_id, OperType_code
    TreatmentConditionsType - вид операции, TreatmentConditionsType_id и TreatmentConditionsType_code нужно значение 2
    UslugaCategory - UslugaCategory_Code=4, UslugaCategory_Name="ГОСТ", UslugaCategory_SysNick="gost2011", UslugaCategory_id=4
    UslugaPlace - UslugaPlace_Code=1, UslugaPlace_Name="Отделение ЛПУ", UslugaPlace_id=1
    """
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'MongoDBWork',
        'm': 'getDataAll',
    }

    data = "data=%7B%22UslugaExecutionReason%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DUslugaExecutionReason%22%2C%22baseparams%22%3A%7B%22UslugaExecutionReason_id%22%3A%22%22%2C%22UslugaExecutionReason_Code%22%3A%22%22%2C%22UslugaExecutionReason_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22UslugaExecutionReason%22%7D%2C%22params%22%3Anull%7D%2C%22UslugaPlace%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DUslugaPlace%22%2C%22baseparams%22%3A%7B%22UslugaPlace_id%22%3A%22%22%2C%22UslugaPlace_Code%22%3A%22%22%2C%22UslugaPlace_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22UslugaPlace%22%7D%2C%22params%22%3A%7B%22where%22%3A%22where%20UslugaPlace_Code%20%3C%3E%204%22%7D%7D%2C%22Okei%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DOkei%22%2C%22baseparams%22%3A%7B%22Okei_id%22%3A%22%22%2C%22OkeiType_id%22%3A%22%22%2C%22Okei_Code%22%3A%22%22%2C%22Okei_Name%22%3A%22%22%2C%22Okei_NationSymbol%22%3A%22%22%2C%22Okei_InterNationSymbol%22%3A%22%22%2C%22Okei_NationCode%22%3A%22%22%2C%22Okei_InterNationCode%22%3A%22%22%2C%22Okei_cid%22%3A%22%22%2C%22Okei_UnitConversion%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22Okei%22%7D%2C%22params%22%3Anull%7D%2C%22CaesarianPhaseType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DCaesarianPhaseType%22%2C%22baseparams%22%3A%7B%22CaesarianPhaseType_id%22%3A%22%22%2C%22CaesarianPhaseType_Code%22%3A%22%22%2C%22CaesarianPhaseType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22CaesarianPhaseType%22%7D%2C%22params%22%3Anull%7D%2C%22nsi_CaesarianIncisionType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3Dnsi_CaesarianIncisionType%22%2C%22baseparams%22%3A%7B%22CaesarianIncisionType_id%22%3A%22%22%2C%22CaesarianIncisionType_Code%22%3A%22%22%2C%22CaesarianIncisionType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22nsi_CaesarianIncisionType%22%7D%2C%22params%22%3Anull%7D%2C%22RumenLocalType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DRumenLocalType%22%2C%22baseparams%22%3A%7B%22RumenLocalType_id%22%3A%22%22%2C%22RumenLocalType_Code%22%3A%22%22%2C%22RumenLocalType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22RumenLocalType%22%7D%2C%22params%22%3Anull%7D%2C%22UslugaCategory%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DUslugaCategory%22%2C%22baseparams%22%3A%7B%22UslugaCategory_id%22%3A%22%22%2C%22UslugaCategory_Code%22%3A%22%22%2C%22UslugaCategory_Name%22%3A%22%22%2C%22UslugaCategory_SysNick%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22UslugaCategory%22%7D%2C%22params%22%3A%7B%22where%22%3A%22where%20UslugaCategory_SysNick%20in%20('tfoms'%2C%20'promed'%2C%20'gost2011'%2C%20'lpu'%2C%20'syslabprofile'%2C%20'lpulabprofile'%2C%20'budget')%22%7D%7D%2C%22UslugaMedType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DUslugaMedType%22%2C%22baseparams%22%3A%7B%22UslugaMedType_id%22%3A%22%22%2C%22UslugaMedType_Code%22%3A%22%22%2C%22UslugaMedType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22UslugaMedType%22%7D%2C%22params%22%3Anull%7D%2C%22DiagSetClass%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DDiagSetClass%22%2C%22baseparams%22%3A%7B%22DiagSetClass_id%22%3A%22%22%2C%22DiagSetClass_Code%22%3A%22%22%2C%22DiagSetClass_Name%22%3A%22%22%2C%22DiagSetClass_SysNick%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22DiagSetClass%22%7D%2C%22params%22%3Anull%7D%2C%22OperType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DOperType%22%2C%22baseparams%22%3A%7B%22OperType_id%22%3A%22%22%2C%22OperType_Code%22%3A%22%22%2C%22OperType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22OperType%22%7D%2C%22params%22%3Anull%7D%2C%22OperDiff%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DOperDiff%22%2C%22baseparams%22%3A%7B%22OperDiff_id%22%3A%22%22%2C%22OperDiff_Code%22%3A%22%22%2C%22OperDiff_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22OperDiff%22%7D%2C%22params%22%3Anull%7D%2C%22TreatmentConditionsType%22%3A%7B%22url%22%3A%22%2F%3Fc%3DMongoDBWork%26m%3DgetData%26object%3DTreatmentConditionsType%22%2C%22baseparams%22%3A%7B%22TreatmentConditionsType_id%22%3A%22%22%2C%22TreatmentConditionsType_Code%22%3A%22%22%2C%22TreatmentConditionsType_Name%22%3A%22%22%2C%22remove%22%3A%22%22%2C%22intersection%22%3A%22%22%2C%22object%22%3A%22TreatmentConditionsType%22%7D%2C%22params%22%3Anull%7D%7D"

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_blood_group(connect):
    """Для ввода группы крови"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'MongoDBWork',
        'm': 'getDataAll',
    }

    data = {
        'data': '{"BloodGroupType":{"url":"/?c=MongoDBWork&m=getData&object=BloodGroupType","baseparams":{"BloodGroupType_id":"","BloodGroupType_Code":"","BloodGroupType_Name":"","remove":"","intersection":"","object":"BloodGroupType"},"params":null},"RhFactorType":{"url":"/?c=MongoDBWork&m=getData&object=RhFactorType","baseparams":{"RhFactorType_id":"","RhFactorType_Code":"","RhFactorType_Name":"","remove":"","intersection":"","object":"RhFactorType"},"params":null}}',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_blood_group(connect, person_id: str, server_id: str, date: str, group_type: str, rh: str):

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'PersonBloodGroup',
        'm': 'savePersonBloodGroup',
    }

    data = {
        'accessType': '',
        'PersonBloodGroup_id': '0',
        'Person_id': person_id,
        'Server_id': server_id,
        'BloodGroupType_id': group_type,  # номер группы 1-первая, 2-вторая и тд
        'RhFactorType_id': rh,  # 1 - положительная, 2 - отрицательная
        'PersonBloodGroup_setDate': date,  # dd.mm.yyyy
        'PersonBloodPhenotype_id': '0',
        'PersonBloodPhenotype_ThereAre_H': 'off',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_info_code_operation(connect, code: str, oper_date: str, person_id: str, evnsection_id: str):
    """Получение информации по коду операции
    UslugaComplex_id, UslugaComplex_pid, UslugaComplex_AttributeList
    """

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Usluga',
        'm': 'loadNewUslugaComplexList',
    }

    data = {
        'to': 'EvnUslugaOper',
        'nonDispOnly': '1',
        'allowedUslugaComplexAttributeList': '["oper"]',
        'UslugaComplex_Date': oper_date,  # дата операции
        'PersonAge': '10',  # забирать из запроса на поиск пациента
        'query': f'A{code}',  # код операции???
        'Person_id': person_id,  # забирать из запроса на поиск пациента
        'uslugaCategoryList': '["gost2011"]',
        'EvnUsluga_pid': evnsection_id,  # EvnSection_id при создании случая госпитализации
        'LpuSection_pid': '380101000015688',  # const - id отделения
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_operation_role_team(connect):
    """Возвращает роли в операционной бригаде"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'MongoDBWork',
        'm': 'getData',
        'object': 'SurgType',
    }

    data = {
        'SurgType_id': '',
        'SurgType_Code': '',
        'SurgType_Name': '',
        'remove': '',
        'intersection': '',
        'object': 'SurgType',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def add_operation_member(connect, medPersonal_id: str, evn_usluga_oper_id: str, medStaffFact_id: str, surgType_id: str):
    """Добавление участника операционной бригады"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnUslugaOperBrig',
        'm': 'saveEvnUslugaOperBrig',
    }

    data = {
        'MedPersonal_id': medPersonal_id,
        'EvnUslugaOper_setDate': '03.04.2024',
        'EvnUslugaOperBrig_id': '0',
        'EvnUslugaOperBrig_pid': evn_usluga_oper_id,
        'SurgType_id': surgType_id,  # забирать из get_operation_role_team
        'MedStaffFact_id': medStaffFact_id,
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_anesthesia_type(connect):
    """Получает вид анестезии
    AnesthesiaClass_id, AnesthesiaClass_Code
    """
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'MongoDBWork',
        'm': 'getDataAll',
    }

    data = {
        'data': '{"AnesthesiaClass":{"url":"/?c=MongoDBWork&m=getData&object=AnesthesiaClass","baseparams":{"AnesthesiaClass_id":"","AnesthesiaClass_Code":"","AnesthesiaClass_Name":"","remove":"","intersection":"","object":"AnesthesiaClass"},"params":null}}',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_oper_anesthesia(connect, evn_usluga_oper_anest_id: str, anesthesiaClass_id: str):
    """Сохраняет вид анестезии"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnUslugaOperAnest',
        'm': 'saveEvnUslugaOperAnest',
    }

    data = {
        'EvnUslugaOperAnest_id': '0',
        'EvnUslugaOperAnest_pid': evn_usluga_oper_anest_id,  # id операции
        'AnesthesiaClass_id': anesthesiaClass_id,  # из get_anesthesia_type
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_complication(connect):
    """Получает осложнения и этап операции
    AggType - само осложнение
    AggWhen - этап на котором произошло
    """

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'MongoDBWork',
        'm': 'getDataAll',
    }

    data = {
        'data': '{"AggType":{"url":"/?c=MongoDBWork&m=getData&object=AggType","baseparams":{"AggType_Code":"","AggType_id":"","AggType_Name":"","AggType_begDT":"","AggType_endDT":"","remove":"","intersection":"","object":"AggType"},"params":null},"AggWhen":{"url":"/?c=MongoDBWork&m=getData&object=AggWhen","baseparams":{"AggWhen_id":"","AggWhen_Code":"","AggWhen_Name":"","remove":"","intersection":"","object":"AggWhen"},"params":null}}',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_complication(connect,
                      person_id: str,
                      personEvn_id: str,
                      server_id: str,
                      date: str,
                      time_set: str,
                      complication_id: str,
                      when_id: str):
    """Сохраняет осложнения"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnAgg',
        'm': 'saveEvnAgg',
    }

    data = {
        'accessType': '',
        'EvnAgg_id': '0',
        'EvnAgg_pid': '380101342738885',  # ???
        'EvnUslugaOnkoSurg_id': '',
        'Person_id': person_id,  # из поиска пациента
        'PersonEvn_id': personEvn_id,  # из поиска пациента
        'Server_id': server_id,  # из поиска пациента
        'EvnAgg_setDate': date,  # dd.mm.YYY
        'EvnAgg_setTime': time_set,  # hh:mm
        'AggType_id': complication_id,  # из get_complication
        'AggWhen_id': when_id,  # из get_complication
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_oper_template(connect, medStaffFact_id: str, medPersonal_id: str, ):
    """Загружает шаблон протокола операции"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'XmlTemplate',
        'm': 'loadGrid',
    }

    data = {
        'MedStaffFact_id': medStaffFact_id,
        'MedPersonal_id': medPersonal_id,
        'LpuSection_id': '380101000006029',
        'MedService_id': '',
        'XmlTemplateCat_id': '380101000010968',
        'UslugaComplex_id': '202879',  # из кода операции
        'XmlTypeKind_id': '',
        'templName': '',
        'templType': '1',
        'limit': '50',
        'start': '0',
        'EvnClass_id': '43',
        'XmlType_id': '17',
        'XmlTemplate_id': XML_TEMPLATE_ID_OPERATION,  # const
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def create_empty_oper(connect, evn_id: str, medStaffFact_id: str):
    """Создаёт шаблон протокола операции"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'createEmpty',
    }

    data = {
        'Evn_id': evn_id,
        'XmlType_id': '17',
        'EvnClass_id': '43',
        'EvnClass_SysNick': 'EvnUslugaOper',
        'Server_id': '38',
        'MedStaffFact_id': medStaffFact_id,
        'XmlTemplate_id': XML_TEMPLATE_ID_OPERATION,
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def update_oper(connect, evn_xml_id: str, text: str):

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'updateContent',
    }

    data = {
        'EvnXml_id': evn_xml_id,
        'objectIsSigned': 'Evn',
        'name': 'descriptionoperation',
        'value': text,
        'isHTML': '1',
    }
    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_all_oper_info(connect,
                       medPersonal_id: str,
                       person_id: str,
                       personEvn_id: str,
                       server_id: str,
                       start_date: str,
                       start_time: str,
                       end_date: str,
                       end_time: str,
                       medStaffFact_id: str,
                       evn_id: str,  # пока '0'
                       evnUslugaOper_id: str,  # '0' при первом сохранении, затем меняется от полученного значения
                       evnPS_id: str,
                       evnSection_id: str,
                       oper_code: str
                       ):
    """Сохраняет все данные протокола операции"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnUsluga',
        'm': 'saveEvnUslugaOper',
    }

    data = {
        'MedPersonal_id': medPersonal_id,
        'Lpu_uid': '',
        'ignoreParentEvnDateCheck': '0',
        'ignoreBallonBegCheck': '0',
        'ignoreCKVEndCheck': '0',
        'accessType': '',
        'XmlTemplate_id': '380101000224703',  # id шаблона протокола операции по 530н приказу
        'Evn_id': evn_id,  # тестировать со значением "0"
        'EvnUslugaOper_id': evnUslugaOper_id,  # ??? найти метод (при сохранении) или указать 0
        'EvnUslugaOper_rid': evnPS_id,  # EvnPS_id (id всей госпитализации)
        'Person_id': person_id,  # из поиска пациента
        'PersonEvn_id': personEvn_id,  # из поиска пациента
        'Server_id': server_id,  # из поиска пациента
        'Morbus_id': '0',
        'IsCardioCheck': '0',
        'EvnUslugaOper_pid': evnSection_id,  # EvnSection_id (id внутри госпитализации)
        'EvnDirection_id': '',
        'EvnUslugaOper_setDate': start_date,  # dd.mm.YYYY
        'EvnUslugaOper_setTime': start_time,  # hh:mm
        'EvnUslugaOper_disDate': end_date,
        'EvnUslugaOper_disTime': end_time,
        'notDefinedBloodField': '',
        'ext-comp-2507': '',
        'bloodParams': '',
        'UslugaExecutionReason_id': '',
        'UslugaPlace_id': '1',
        'LpuSection_uid': '380101000015688',  # id отделения (травматология)
        'LpuSectionProfile_id': '380101000000301',
        'MedSpecOms_id': '',
        'MedStaffFact_id': medStaffFact_id,
        'MedStaffFact_sid': '',
        'PayType_id': '380101000000021',
        'PayContract_id': '',
        'PolisDMS_id': '',
        'EvnPrescr_id': '',
        'UslugaCategory_id': '4',
        'UslugaComplex_id': oper_code,  # из кода операции
        'UslugaMedType_id': '',
        'UslugaComplexTariff_id': '',
        'DiagSetClass_id': '',
        'Diag_id': '',
        'EvnUslugaOper_Kolvo': '1',
        'OperType_id': '2',
        'OperDiff_id': '2',
        'TreatmentConditionsType_id': '2',
        'EvnUslugaOper_IsVMT': '',
        'EvnUslugaOper_IsMicrSurg': '',
        'EvnUslugaOper_IsOpenHeart': '',
        'EvnUslugaOper_IsEndoskop': '1',
        'EvnUslugaOper_IsLazer': '1',
        'EvnUslugaOper_IsKriogen': '1',
        'EvnUslugaOper_IsRadGraf': '1',
        'CaesarianPhaseType_id': '',
        'EvnUslugaOper_WaterlessPeriod': '',
        'Okei_wid': '',
        'CaesarianIncisionType_id': '',
        'RumenLocalType_id': '',
        'EvnUslugaOper_BloodLoss': '',
        'Okei_bid': '',
        'EvnUslugaOper_BallonBegDate': '',
        'EvnUslugaOper_BallonBegTime': '',
        'EvnUslugaOper_CKVEndDate': '',
        'EvnUslugaOper_CKVEndTime': '',
        'EvnUslugaOnkoSurg_id': '',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()
