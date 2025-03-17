from datetime import datetime, timezone


def search_patients_ext6(
        connect,
        surname: str,
        name: str,
        patronymic: str,
        birthday: str  # дата рождения в формате dd.mm.yyyy
) -> list:
    """Поиск пациента в ext6.js(поликлиника)"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Person6E',
        'm': 'getPersonGrid',
    }

    data = {
        'start': '0',
        'limit': '100',
        'Double_ids': '[]',
        'Person_Surname': surname,
        'Person_Firname': name,
        'Person_Secname': patronymic,
        'Person_Birthday': birthday,
        'Address_Street': '',
        'Address_House': '',
        'PersonCard_Code': '',
        'Polis_Ser': '',
        'Polis_Num': '',
        'Person_Code': '',
        'AttachLpu_id': 'null',
        'Org_id': '10379',
        'showAll': '1',
        'dontShowUnknowns': '1',
        'page': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response.get('data')


def date_in_milliseconds() -> int:
    dt = datetime.now(timezone.utc)
    milliseconds = int(dt.timestamp() * 1000)
    return milliseconds


def get_evn_pl_number(connect, pl_number: int) -> str:
    """Получает номер амбулаторного случая консультации (дата переводится в миллисекунды)"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnPL',
        'm': 'getEvnPLNumber',
        '_dc': f'{pl_number}',
    }

    response = connect.get('https://ecp38.is-mis.ru/', params=params, headers=headers).json()
    return response.get('EvnPL_NumCard')


def save_first_data_vizit(
        connect,
        med_staff_fact_id: str,
        med_personal_id: str,
        person_evn_id: str,
        person_id: str,
        server_id: str,
        date_pl: str,
        time_pl: str,
        evn_pl_number: str,
        lpu_section_id: str,
        vizit_type_id: str
):
    """Первые данные обращения"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnPL',
        'm': 'saveEmkEvnPL',
    }

    data = {
        'action': 'addEvnPL',
        'allowCreateEmptyEvnDoc': '2',
        'MedStaffFact_id': med_staff_fact_id,
        'LpuSection_id': lpu_section_id,  # const
        'MedPersonal_id': med_personal_id,
        'TimetableGraf_id': '',
        'EvnDirection_id': '',
        'EvnDirection_vid': '',
        'EvnPrescr_id': '',
        'isMyOwnRecord': '',
        'PersonEvn_id': person_evn_id,  # из поиска
        'Person_id': person_id,  # из поиска
        'Server_id': server_id,
        'EvnPL_id': '0',
        'EvnPL_IsFinish': '1',
        'EvnVizitPL_id': '0',
        'EvnVizitPL_setDate': date_pl,  # dd.mm.YYYY
        'EvnVizitPL_setTime': time_pl,  # hh:mm
        'PayType_id': '380101000000021',  # const
        'ServiceType_id': '0',
        'VizitType_id': vizit_type_id,  # const?
        'EvnPL_NumCard': evn_pl_number,
        'EvnPL_IsWithoutDirection': '1',
        'isAutoCreate': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def save_visit(
        connect,
        date_save_revers: str,
        evn_vizit_pl_id: str,
        person_id: str,
        person_evn_id: str,
        date_save: str,
        time_save: str,
        med_staff_fact_id: str,
        treatment_class_id: str,
        service_type_id: str,
        diag_id: str,
        diagnos_text: str,
        lpu_section_id: str,
        vizit_type_id: str,
        lpu_section_profile_id: str,
        usluga_complex_id: str
):
    """Сохраняет все данные посещения"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnPL',
        'm': 'saveEvnVizitFromEMK',
    }

    data = {
        'ignoreCorrectPalliativeCareCheck': '1',
        'ignoreUslugaPayTypeCheck': '1',
        'ignoreUslugaToMesCheck': '1',
        'EvnVizitPL_IsTMK': '',
        'ignoreLpuSectionAge': '',
        'checkCVI': 'true',
        'ignoreDiagDeseaseTypeLink': '0',
        'diagDeseaseTypeLinkDate': date_save_revers,
        'EvnVizitPL_id': evn_vizit_pl_id,  # из save_first_data_vizit()
        'form_saved': '0',
        'Person_id': person_id,
        'EvnVizitPL_IsZNORemove': '',
        'lastZNO': '',
        'Server_id': '0',
        'PersonEvn_id': person_evn_id,
        'MedSpecClass_id': '79',
        'MedicalFormPersonDispPrescr_id': '',
        'IsDeleteSpecificCVI': '1',
        'EvnVizitPL_setDate': date_save,
        'EvnVizitPL_setTime': time_save,
        'EvnVizitPL_IsPrimaryVizitAnnual': 'null',
        'LpuSection_id': lpu_section_id,  # 380101000015788 - травма, 380101000015715 - ЛОР
        'MedStaffFact_id': med_staff_fact_id,
        'MedStaffFact_id2': 'null',
        'MedStaffFact_id3': 'null',
        'MedStaffFact_sid': 'null',
        'TreatmentClass_id': treatment_class_id,  # Вид обращения 1-заболевание, 2-неотложка(заболевание)
        'VizitActiveType_id': 'null',
        'ServiceType_id': service_type_id,  # для первичного '6', для повторного должно быть '4'
        'VizitClass_id': '1',
        'VizitType_id': vizit_type_id,  # 380101000000063 - травма, 380101000000016 - заболевание
        'MedOffice_id': 'null',
        'RiskLevel_id': 'null',
        'WellnessCenterAgeGroups_id': 'null',
        'Mes_id': 'null',
        'Eye_id': 'null',
        'MedicalCareKind_id': '6',
        'MesRegion_id': 'null',
        'UslugaComplex_uid': usluga_complex_id,
        'DispClass_id': 'null',
        'EvnPLDisp_id': '',
        'PersonDisp_id': '',
        'LpuSectionProfile_id': lpu_section_profile_id,  # 380101000000301 - травматология, 380101000000021 - ЛОР
        'PayType_id': '380101000000021',  # ОМС
        'PayContract_id': 'null',
        'PolisDMS_id': 'null',
        'ProfGoal_id': 'null',
        'PregnancyEvnVizitPL_Period': '',
        'Diag_id': diag_id,  # ???
        'EvnInfectNotify_id': '',
        'Diag11_Code': 'null',
        'HeartFailureStage_54': 'null',
        'HeartFailureClass_55': 'null',
        'StenocardiaFuncClass_id': 'null',
        'PulmonaryHypertensionFuncClass_id': 'null',
        'OnkoLesionSide_id': 'null',
        'DeseaseType_id': '3',
        'DiagSetPhase_id': '1',
        'PainIntensity_id': 'null',
        'TumorStage_id': 'null',
        'ClinicalDiagnosis_140': diagnos_text,
        'EvnVizitPL_IsZNO': '1',
        'RankinScale_id': 'null',
        'Diag_agid': 'null',
        'Diag_spid': 'null',
        'Diag_oid': 'null',
        'EvnVizitPL_BiopsyDate': '',
        'HealthKind_id': 'null',
        'RehabScale_id': 'null',
        'EvnVizitPL_IsRecoveryPotential': '1',
        'RehabType_id': 'null',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def create_template(
        connect,
        date_in_ms: str,
        person_id: str,
        evn_vizit_pl_id: str,  # из first_save
        med_personal_id: str,
        med_staff_fact_id: str,
        lpu_section_id: str
):
    """Получает номер шаблона текстовой части протокола (EvnXml_id)"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'loadEvnXmlPanel',
        '_dc': date_in_ms,
        'XmlType_id': '3',
        'Person_id': person_id,
        'Evn_id': evn_vizit_pl_id,
        'EvnClass_id': '11',
        'LpuSection_id': lpu_section_id,
        'MedPersonal_id': med_personal_id,
        'MedStaffFact_id': med_staff_fact_id,
        'MedService_id': '',
        'EvnXml_id': '',
        'XmlTemplate_id': '',
        'EMDRegistry_ObjectName': '',
        'isEvnOperPDF': '',
        'ARMType': '',
        'userLpuSection_id': '',
        'page': '1',
        'start': '0',
        'limit': '25',
    }

    response = connect.get('https://ecp38.is-mis.ru/', params=params, headers=headers).json()
    return response


def save_text_protocol(
        connect,
        evn_xml_id: str,
        evn_vizit_pl_id: str,
        protocol_text: str,
):
    """Сохраняет шаблон самого протокола текста"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml6E',
        'm': 'saveEvnXml',
    }

    data = f'EvnXml_id={evn_xml_id}&Evn_id={evn_vizit_pl_id}&objectIsSigned=Evn&EvnClass_id=11&XmlType_id=3&XmlTemplate_id=380101000472618&XmlTemplate_HtmlTemplate=%3Cdiv%20class%3D%22sw-editor-page-header%22%20contenteditable%3D%22false%22%3E%40%23%40%D0%A8%D0%B0%D0%BF%D0%BA%D0%B0%D0%9E%D1%81%D0%BC%D0%BE%D1%82%D1%80%D0%B0%3C%2Fdiv%3E%3Cdiv%20class%3D%22sw-editor-page-content%22%3E{protocol_text}%3Cp%3E%3Cbr%20data-mce-bogus%3D%221%22%3E%3C%2Fp%3E%3C%2Fdiv%3E%3Cdiv%20class%3D%22sw-editor-page-footer%22%20contenteditable%3D%22false%22%3E%40%23%40%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA%D0%9B%D0%92%D0%9D%40%23%40%D0%9D%D0%B0%D0%B7%D0%BD%D0%B0%D1%87%D0%B5%D0%BD%D0%B8%D1%8F%3C%2Fdiv%3E&EvnXml_Data=%7B%22complaint%22%3A%22%22%2C%22anamnesmorbi%22%3A%22%22%2C%22diagnos%22%3A%22%22%2C%22resolution%22%3A%22%22%2C%22researchResults%22%3A%22xcv789%22%2C%22specMarker_115%22%3A%22%22%2C%22specMarker_353%22%3A%22%22%2C%22specMarker_354%22%3A%22%3Cdiv%20class%3D%5C%22header-content%5C%22%3E%5Cn%20%20%20%20%3Cdiv%20style%3D%5C%22float%3A%20left%3B%20width%3A%2060%25%3B%5C%22%3E%5Cn%3Cp%3E%5Cu041f%5Cu0430%5Cu0446%5Cu0438%5Cu0435%5Cu043d%5Cu0442%3A%20%5Cu0411%5Cu043e%5Cu0447%5Cu043a%5Cu0430%5Cu0440%5Cu043d%5Cu0438%5Cu043a%5Cu043e%5Cu0432%20%5Cu0411%5Cu043e%5Cu0433%5Cu0434%5Cu0430%5Cu043d%20%5Cu0418%5Cu0432%5Cu0430%5Cu043d%5Cu043e%5Cu0432%5Cu0438%5Cu0447%3C%2Fp%3E%5Cn%3Cp%3E%5Cu0414%5Cu0430%5Cu0442%5Cu0430%20%5Cu0440%5Cu043e%5Cu0436%5Cu0434%5Cu0435%5Cu043d%5Cu0438%5Cu044f%3A%2024.03.2008%20(16%20%5Cu043b%5Cu0435%5Cu0442)%3C%2Fp%3E%5Cn%3Cp%3E%5Cu0410%5Cu0434%5Cu0440%5Cu0435%5Cu0441%20%5Cu043f%5Cu0440%5Cu043e%5Cu0436%5Cu0438%5Cu0432%5Cu0430%5Cu043d%5Cu0438%5Cu044f%3A%20%3C%2Fp%3E%5Cn%3C%2Fdiv%3E%5Cn%20%20%20%20%3Cdiv%20style%3D%5C%22float%3A%20right%3B%20width%3A%2040%25%3B%5C%22%3E%5Cn%3Cp%3E%5Cu0414%5Cu0430%5Cu0442%5Cu0430%20%5Cu0438%20%5Cu0432%5Cu0440%5Cu0435%5Cu043c%5Cu044f%20%5Cu043f%5Cu043e%5Cu0441%5Cu0435%5Cu0449%5Cu0435%5Cu043d%5Cu0438%5Cu044f%3A%2001.07.2024%2013%3A07%3C%2Fp%3E%5Cn%3Cp%3E%5Cu041c%5Cu041e%3A%20%5Cu041e%5Cu0413%5Cu0410%5Cu0423%5Cu0417%20%5C%22%5Cu0413%5Cu0418%5Cu041c%5Cu0414%5Cu041a%5Cu0411%5C%22%20%5Cu0433.%20%5Cu0418%5Cu0420%5Cu041a%5Cu0423%5Cu0422%5Cu0421%5Cu041a%5Cu0410%3C%2Fp%3E%5Cn%3Cp%3E%5Cu041f%5Cu0440%5Cu043e%5Cu0444%5Cu0438%5Cu043b%5Cu044c%3A%20%5Cu0422%5Cu0440%5Cu0430%5Cu0432%5Cu043c%5Cu0430%5Cu0442%5Cu043e%5Cu043b%5Cu043e%5Cu0433%5Cu0438%5Cu044f%20%5Cu0438%20%5Cu043e%5Cu0440%5Cu0442%5Cu043e%5Cu043f%5Cu0435%5Cu0434%5Cu0438%5Cu044f%3C%2Fp%3E%5Cn%3C%2Fdiv%3E%5Cn%20%20%20%20%3Cdiv%20style%3D%5C%22clear%3A%20both%3B%20margin%3A%200pt%3B%20padding%3A%200pt%3B%20%5C%22%3E%3C%2Fdiv%3E%5Cn%3C%2Fdiv%3E%5Cn%22%7D&EvnXml_DataSettings=%7B%22complaint%22%3A%7B%22name%22%3A%22complaint%22%2C%22xtype%22%3A%22ckeditor%22%2C%22fieldLabel%22%3A%22%3Cstrong%3E%5Cu0416%5Cu0430%5Cu043b%5Cu043e%5Cu0431%5Cu044b%3C%2Fstrong%3E%22%2C%22hideLabel%22%3A%22false%22%7D%2C%22anamnesmorbi%22%3A%7B%22name%22%3A%22anamnesmorbi%22%2C%22xtype%22%3A%22ckeditor%22%2C%22fieldLabel%22%3A%22%3Cstrong%3E%5Cu0410%5Cu043d%5Cu0430%5Cu043c%5Cu043d%5Cu0435%5Cu0437%20%5Cu0437%5Cu0430%5Cu0431%5Cu043e%5Cu043b%5Cu0435%5Cu0432%5Cu0430%5Cu043d%5Cu0438%5Cu044f%3C%2Fstrong%3E%22%2C%22hideLabel%22%3A%22false%22%7D%2C%22diagnos%22%3A%7B%22name%22%3A%22diagnos%22%2C%22xtype%22%3A%22ckeditor%22%2C%22fieldLabel%22%3A%22%3Cstrong%3E%5Cu0414%5Cu0438%5Cu0430%5Cu0433%5Cu043d%5Cu043e%5Cu0437%20%5Cu043e%5Cu0441%5Cu043d%5Cu043e%5Cu0432%5Cu043d%5Cu043e%5Cu0439%20(%5Cu0440%5Cu0430%5Cu0441%5Cu0448%5Cu0438%5Cu0444%5Cu0440%5Cu043e%5Cu0432%5Cu043a%5Cu0430)%3C%2Fstrong%3E%22%2C%22hideLabel%22%3A%22false%22%7D%2C%22resolution%22%3A%7B%22name%22%3A%22resolution%22%2C%22xtype%22%3A%22ckeditor%22%2C%22fieldLabel%22%3A%22%3Cstrong%3E%5Cu0417%5Cu0430%5Cu043a%5Cu043b%5Cu044e%5Cu0447%5Cu0435%5Cu043d%5Cu0438%5Cu0435%3C%2Fstrong%3E%22%2C%22hideLabel%22%3A%22false%22%7D%2C%22researchResults%22%3A%7B%22name%22%3A%22researchResults%22%2C%22xtype%22%3A%22ckeditor%22%2C%22fieldLabel%22%3A%22%3Cstrong%3E%5Cu0420%5Cu0435%5Cu0437%5Cu0443%5Cu043b%5Cu044c%5Cu0442%5Cu0430%5Cu0442%5Cu044b%20%5Cu0438%5Cu0441%5Cu0441%5Cu043b%5Cu0435%5Cu0434%5Cu043e%5Cu0432%5Cu0430%5Cu043d%5Cu0438%5Cu044f%3C%2Fstrong%3E%22%2C%22hideLabel%22%3A%22false%22%7D%7D'

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def add_initial_examination_service(
        connect,
        evn_id: str,
        medpersonal_id: str,
        person_id: str,
        personevn_id: str,
        server_id: str,
        medstafffact_id: str,
        exam_date: str,
        start_time: str,
        end_time: str,
        usluga_complex_id: str,
        lpu_section_id: str,
        lpu_section_profile_id: str
):
    """Добавляет услугу первичного приема травматологом"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnUsluga',
        'm': 'saveEvnUslugaCommon',
    }

    data = {
        'EvnUslugaCommon_Price': '0',
        'EvnUslugaCommon_Summa': '0.00',
        'ignoreParentEvnDateCheck': '0',
        'ignorePaidCheck': '',
        'CovidContingentType_id': 'null',
        'PersonDisp_ids': '[]',
        'isPaidUsluga': 'false',
        'EvnUslugaComplexPlanLink_id': '',
        'PayDocEvnPersonalAgreementsLink_paguid': '',
        'accessType': '',
        'EvnClass_SysNick': 'EvnUslugaCommon',
        'EvnUslugaCommon_id': '',
        'EvnUslugaCommon_rid': '0',
        'Evn_id': evn_id,  # first_save.get('EvnVizitPL_id')
        'EvnDirection_id': '',
        'MedPersonal_id': medpersonal_id,  # из doctors.json
        'Morbus_id': '-1',
        'Person_id': person_id,  # из search_patient
        'PersonEvn_id': personevn_id,  # patient_data[0].get('PersonEvn_id')
        'Server_id': server_id,
        'EvnUslugaCommon_pid': evn_id,  # first_save.get('EvnVizitPL_id')
        'EvnUslugaCommon_setDate': exam_date,  # dd.mm.YYYY
        'EvnUslugaCommon_setTime': start_time,  # hh:mm
        'EvnUslugaCommon_disDate': exam_date,  # dd.mm.YYYY
        'EvnUslugaCommon_disTime': end_time,  # hh:mm
        'UslugaExecutionType_id': 'null',
        'UslugaExecutionReason_id': 'null',
        'UslugaPlace_id': '1',
        'LpuSection_uid': lpu_section_id,  # const
        'LpuSectionProfile_id': lpu_section_profile_id,  # const
        'Lpu_uid': 'null',
        'Org_uid': 'null',
        'MedSpecOms_id': 'null',
        'MedStaffFact_id': medstafffact_id,  # из doctors.json
        'MedStaffFact_sid': 'null',
        'PayType_id': '380101000000021',  # const
        'PayContract_id': 'null',
        'PersonalAgreements_id': '',
        'PolisDMS_id': 'null',
        'EvnPrescr_id': 'null',
        'UslugaCategory_id': '4',
        'UslugaComplex_id': usluga_complex_id,  # 206696 - id первичного осмотра травматологом, 206697 - повторный осмотр травматологом
        'smoPersonFio': '',
        'smoComment': 'Укажите количество согласованных услуг и дату окончания согласования',
        'UslugaComplexTariff_id': 'null',
        'DiagSetClass_id': 'null',
        'Diag_id': 'null',
        'PersonDisp_id': '',
        'EvnUslugaCommon_Kolvo': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def finished(
        connect,
        evn_pl_id: str,
        diag_id: str,
        text_diag: str,
        diag_w: str,
        result_class_id: str
):
    """Закрывает случай обращения"""
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnPL',
        'm': 'saveEvnPLFinishForm',
    }

    data = {
        'EvnPL_IsFinish': '2',
        'EvnPL_id': evn_pl_id,
        'IsDeleteSpecificCVI': '1',
        'EvnPL_IsSurveyRefuse': 'null',
        'ResultClass_id': result_class_id,
        'InterruptLeaveType_id': 'null',
        'ResultDeseaseType_id': '380101000000028',
        'EvnPL_UKL': '1',
        'EvnPL_IsFirstDisable': 'null',
        'PrivilegeType_id': 'null',
        'DirectType_id': 'null',
        'DirectClass_id': 'null',
        'LpuSection_oid': 'null',
        'Lpu_oid': 'null',
        'Diag_lid': diag_id,
        'ClinicalDiagnosis_140': text_diag,
        'Diag_concid': diag_w,
        'PrehospTrauma_id': 'null',  # идентификатор вида травмы
        'EvnPL_IsUnlaw': 'null',
        'EvnPL_IsUnport': 'null',
        'LeaveType_fedid': 'null',
        'ResultDeseaseType_fedid': 'null',
        'EvnPL_isMseDirected': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response


def get_operation_id(connect, date_mls: str, date: str, evn_usluga_pid: str, lpu_section_pid: str, operation_code: str):
    """Запрос на получение UslugaComplex_id по коду операции"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'dnt': '1',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'Usluga',
        'm': 'loadNewUslugaComplexList',
        '_dc': date_mls,  # количество миллисекунд
        'query': operation_code,  # только латинская литера
        'UslugaComplex_Date': date,
        'ucp': '',
        'EvnUsluga_pid': evn_usluga_pid,  # EvnVizitPL_id
        'UslugaCategory_id': '4',
        'to': 'EvnUslugaOper',
        'DispClass_id': '',
        'dispOnly': '',
        'nonDispOnly': '1',
        'LpuSection_pid': lpu_section_pid,  # lpu_section_id
        'uslugaCategoryList': '["gost2011"]',
        'Person_id': '0',
        'PersonAge': '0',
        'PayType_id': '0',
        'allowedUslugaComplexAttributeList': '["oper"]',
        'allowedUslugaComplexAttributeMethod': 'or',
        'disallowedUslugaComplexAttributeList': '',
        'allowMorbusVizitCodesGroup88': '0',
        'allowMorbusVizitOnly': '0',
        'allowNonMorbusVizitOnly': '0',
        'ignoreUslugaComplexDate': '0',
        'Mes_id': '',
        'LpuLevel_Code': '',
        'uslugaComplexCodeList': '',
        'UslugaComplex_2011id': '',
        'withoutPackage': '1',
        'page': '1',
        'start': '0',
        'limit': '25',
    }

    response = connect.get('https://ecp38.is-mis.ru/', params=params, headers=headers).json()
    return response  # .get('UslugaComplex_id')


def add_operation_service(
        connect,
        med_personal_id: str,
        evn_id: str,
        person_id: str,
        person_evn_id: str,
        evn_usluga_oper_pid: str,
        oper_start_date: str,
        oper_end_date: str,
        oper_start_time: str,
        oper_end_time: str,
        lpu_section_uid: str,
        lpu_section_profile_id: str,
        med_staff_fact_id: str,
        usluga_complex_id: str
):
    """Запрос на добавление услуги - операции"""

    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=1, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnUsluga',
        'm': 'saveEvnUslugaOper',
    }

    data = {
        'MedPersonal_id': med_personal_id,
        'MedPersonal_sid': '',
        'ignorePaidCheck': '',
        'ignoreParentEvnDateCheck': '0',
        'ignoreBallonBegCheck': '0',
        'ignoreCKVEndCheck': '0',
        'isPaidUsluga': 'false',
        'EvnUslugaComplexPlanLink_id': '',
        'EvnUslugaOper_Price': '0',
        'EvnUslugaOper_Summa': '0.00',
        'PayDocEvnPersonalAgreementsLink_paguid': '',
        'EvnUslugaOper_Kolvo': '1',
        'accessType': '',
        'XmlTemplate_id': '0',
        'EvnUslugaOper_id': '',
        'EvnUslugaOper_rid': '0',
        'Server_id': '38',
        'Morbus_id': '0',
        'IsCardioCheck': '0',
        'Evn_id': evn_id,  # EvnVizitPL_id
        'AnesthesiaClass': '0',
        'EvnDirection_id': '',
        'Person_id': person_id,
        'PersonEvn_id': person_evn_id,
        'EvnUslugaOper_pid': evn_usluga_oper_pid,  # EvnVizitPL_id
        'EvnUslugaOper_setDate': oper_start_date,
        'EvnUslugaOper_setTime': oper_start_time,
        'EvnUslugaOper_disDate': oper_end_date,
        'EvnUslugaOper_disTime': oper_end_time,
        'UslugaExecutionType_id': 'null',
        'UslugaExecutionReason_id': 'null',
        'UslugaPlace_id': '1',
        'LpuSection_uid': lpu_section_uid,
        'LpuSectionProfile_id': lpu_section_profile_id,
        'Lpu_uid': 'null',
        'Org_uid': 'null',
        'MedSpecOms_id': 'null',
        'MedStaffFact_id': med_staff_fact_id,
        'MedStaffFact_sid': 'null',
        'PayType_id': '380101000000021',
        'PayContract_id': 'null',
        'PersonalAgreements_id': '',
        'PolisDMS_id': 'null',
        'EvnPrescr_id': 'null',
        'UslugaCategory_id': '4',
        'UslugaComplex_id': usluga_complex_id,
        'BeamLoad_RadiationDose': '',
        'BeamLoadUnits_id': 'null',
        'smoPersonFio': '',
        'smoComment': 'Укажите количество согласованных услуг и дату окончания согласования',
        'UslugaComplexTariff_id': 'null',
        'DiagSetClass_id': 'null',
        'Diag_id': 'null',
        'EvnUslugaOper_BallonBegDate': '',
        'EvnUslugaOper_BallonBegTime': '',
        'EvnUslugaOper_CKVEndDate': '',
        'EvnUslugaOper_CKVEndTime': '',
        'OperType_id': '3',
        'OperDiff_id': '1',
        'TreatmentConditionsType_id': 'null',
        'EvnUslugaOper_IsVMT': '1',
        'EvnUslugaOper_IsOpenHeart': '1',
        'EvnUslugaOper_IsMicrSurg': '1',
        'EvnUslugaOper_IsArtCirc': '1',
        'EvnUslugaOper_IsEndoskop': '1',
        'EvnUslugaOper_IsKriogen': '1',
        'EvnUslugaOper_IsLazer': '1',
        'EvnUslugaOper_IsRadGraf': '1',
        'CaesarianPhaseType_id': 'null',
        'EvnUslugaOper_WaterlessPeriod': '',
        'Okei_wid': 'null',
        'CaesarianIncisionType_id': 'null',
        'RumenLocalType_id': 'null',
        'EvnUslugaOper_BloodLoss': '',
        'Okei_bid': 'null',
        'EvnUslugaOper_deadDate': '',
        'EvnUslugaOper_deadTime': '',
        'EvnUslugaOnkoSurg_id': 'null',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response
