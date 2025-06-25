from datetime import datetime
from pprint import pprint

from fake_useragent import FakeUserAgent
from requests import Session

from settings import LPU_SECTION_ID_TRAUMA, XML_TEMPLATE_ID_OPERATION


class CurrentPatientECP:
    def __init__(self,
                 connect,
                 person_evn_id: str,
                 person_id: str,
                 medpersonal_id: str,
                 evn_section_id: str,
                 evn_ps_id: str,
                 server_id: str,
                 ksg: str):
        self._connect = connect
        self._headers = {
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://ecp38.is-mis.ru',
            'priority': 'u=1, i',
            'referer': 'https://ecp38.is-mis.ru/?c=promed',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
        }
        self.person_evn_id = person_evn_id
        self.person_id = person_id
        self.medpersonal_id = medpersonal_id
        self.evn_section_id = evn_section_id
        self.evn_ps_id = evn_ps_id
        self.server_id = server_id
        self.ksg = ksg
        self.person_fio = self._get_patient_info_by_person_id(connect).get('Person_Fio').lower()
        self.person_birthday = self._get_patient_info_by_person_id(connect).get('Person_BirthDay')

    def _get_patient_info_by_person_id(self, connect):

        params = {
            'c': 'Evn',
            'm': 'getEvnJournal',
        }

        data = {
            'Person_id': self.person_id,
            'PersonNotice_IsSend': '2',
            'start': '0',
            'limit': '10',
            'isMseDepers': '0',
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data).json()
        return response.get('data')

    def get_operation_code(self, code: str, oper_date: str):
        """Получение информации по коду операции
        UslugaComplex_id, UslugaComplex_pid, UslugaComplex_AttributeList
        """

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
            'Person_id': self.person_id,  # забирать из запроса на поиск пациента
            'uslugaCategoryList': '["gost2011"]',
            'EvnUsluga_pid': self.evn_section_id,  # EvnSection_id при создании случая госпитализации
            'LpuSection_pid': LPU_SECTION_ID_TRAUMA,  # const - id отделения
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def save_oper_info(self,
                       medPersonal_id: str,
                       start_date: str,
                       start_time: str,
                       end_date: str,
                       end_time: str,
                       medStaffFact_id: str,
                       oper_code: str,
                       evn_id: str = '0',
                       evnUslugaOper_id: str = '0',
                       ):
        """Сохраняет все данные протокола операции"""

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
            'EvnUslugaOper_rid': self.evn_ps_id,
            'Person_id': self.person_id,
            'PersonEvn_id': self.person_evn_id,
            'Server_id': self.server_id,
            'Morbus_id': '0',
            'IsCardioCheck': '0',
            'EvnUslugaOper_pid': self.evn_section_id,
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

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def add_operation_member(self, medPersonal_id: str, start_date: str, evn_usluga_oper_id: str, medStaffFact_id: str,
                             surgType_id: str):
        """Добавление участника операционной бригады"""

        params = {
            'c': 'EvnUslugaOperBrig',
            'm': 'saveEvnUslugaOperBrig',
        }

        data = {
            'MedPersonal_id': medPersonal_id,
            'EvnUslugaOper_setDate': start_date,
            'EvnUslugaOperBrig_id': '0',
            'EvnUslugaOperBrig_pid': evn_usluga_oper_id,
            'SurgType_id': surgType_id,  # забирать из get_operation_role_team
            'MedStaffFact_id': medStaffFact_id,
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def save_oper_anesthesia(self, evn_usluga_oper_anest_id: str, anesthesiaClass_id: str):
        """Сохраняет вид анестезии"""

        params = {
            'c': 'EvnUslugaOperAnest',
            'm': 'saveEvnUslugaOperAnest',
        }

        data = {
            'EvnUslugaOperAnest_id': '0',
            'EvnUslugaOperAnest_pid': evn_usluga_oper_anest_id,  # id операции
            'AnesthesiaClass_id': anesthesiaClass_id,  # из get_anesthesia_type
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def create_empty_oper(self, evn_id: str, medStaffFact_id: str):
        """Создаёт шаблон протокола операции"""

        params = {
            'c': 'EvnXml',
            'm': 'createEmpty',
        }

        data = {
            'Evn_id': evn_id,
            'XmlType_id': '17',
            'EvnClass_id': '43',
            'EvnClass_SysNick': 'EvnUslugaOper',
            'Server_id': self.server_id,
            'MedStaffFact_id': medStaffFact_id,
            'XmlTemplate_id': XML_TEMPLATE_ID_OPERATION,
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def update_oper(self, evn_xml_id: str, text: str):
        """Обновляет протокол операции (ход операции)"""
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
        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def save_implant_type_link(self, evn_usluga_oper_id: str, implant_id: str, implant_name: str):
        """Добавляет имплантированное изделие (тестировать)"""

        params = {
            'c': 'EvnUsluga',
            'm': 'saveEvnUslugaImplantTypeLink',
        }

        data = {
            'EvnUslugaImplantTypeLink_id': '',
            'EvnUsluga_id': evn_usluga_oper_id,  # EvnUslugaOper_id
            'ImplantType_id': implant_id,  # из implant_info.json
            'EvnUslugaImplantTypeLink_SerNum': '0000',  # серийный номер
            'ImplantType_Name': implant_name,  # из implant_info.json, можно не указывать
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()


class PatientECP:
    def __init__(self, connect: Session, name: str, surname: str, patronymic: str, birthday: str):
        self._connect = connect
        self._headers_ecp = {
            'authority': 'ecp38.is-mis.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://ecp38.is-mis.ru',
            'referer': 'https://ecp38.is-mis.ru/?c=promed',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-kl-kav-ajax-request': 'Ajax_Request',
            'x-requested-with': 'XMLHttpRequest',
        }
        self.name = name
        self.surname = surname
        self.patronymic = patronymic
        self.birthday = birthday

        if self.__search():
            self.person_id = self.__search()[0].get('Person_id')
            self.person_evn_id = self.__search()[0].get('PersonEvn_id')
            self.server_id = self.__search()[0].get('Server_id')
        else:
            self.person_id = None
            self.person_evn_id = None
            self.server_id = None

    def __search(self):
        """Поиск пациента по ФИО и дате рождения"""

        headers_search = {
            'authority': 'ecp38.is-mis.ru',
            'accept': '*/*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'dnt': '1',
            'origin': 'https://ecp38.is-mis.ru',
            'referer': 'https://ecp38.is-mis.ru/?c=promed',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': FakeUserAgent().random,
            'x-requested-with': 'XMLHttpRequest',
        }
        params_search = {
            'c': 'Person',
            'm': 'getPersonSearchGrid',
        }

        data_search = {
            'PersonSurName_SurName': self.surname,
            'ParentARM': '',
            'PersonFirName_FirName': self.name,
            'PersonSecName_SecName': self.patronymic,
            'PersonBirthDay_BirthDay': self.birthday,
            'PersonAge_AgeFrom': '',
            'PersonAge_AgeTo': '',
            'PersonBirthYearFrom': '',
            'PersonBirthYearTo': '',
            'Person_id': '',
            'Person_Snils_Hidden': '',
            'Person_Snils': '',
            'AttachLpu_id': '',
            'Person_Inn': '',
            'Polis_Ser': '',
            'Polis_Num': '',
            'Polis_EdNum': '',
            'PersonCard_id': '',
            'PersonCard_Code': '',
            'EvnPS_NumCard': '',
            'searchMode': 'all',
            'start': '0',
            'limit': '100',
            'armMode': '',
            'isTfoms': '0',
        }

        response_search = self._connect.post('https://ecp38.is-mis.ru/',
                                             params=params_search,
                                             headers=headers_search,
                                             data=data_search)
        return response_search.json().get('data')


class HistoryEcp(PatientECP):
    """Класс случай госпитализации ЕЦП"""

    def __init__(self, connect: Session, name: str, surname: str, patronymic: str, birthday: str):
        super().__init__(connect, name, surname, patronymic, birthday)
        self._evn_number = self.__get_evn_number()
        self.operation_code = []

    def __get_evn_number(self):
        """Получает номер случая госпитализации"""
        params = {
            'c': 'EvnPS',
            'm': 'getEvnPSNumber',
        }

        current_datetime = datetime.now()
        current_year = current_datetime.year
        current_year_str = str(current_year)

        data = {
            'year': current_year_str,
        }

        response = self._connect.post('https://ecp38.is-mis.ru/',
                                      params=params,
                                      headers=self._headers_ecp,
                                      data=data).json()
        if response.get('EvnPS_NumCard'):
            return response.get('EvnPS_NumCard')
        else:
            return False

    def get_info_code_operation(self, code: str, oper_date: str, evnsection_id: str):
        """Получение информации по коду операции
        UslugaComplex_id, UslugaComplex_pid, UslugaComplex_AttributeList
        """
        params = {
            'c': 'Usluga',
            'm': 'loadNewUslugaComplexList',
        }

        data = {
            'to': 'EvnUslugaOper',
            'nonDispOnly': '1',
            'allowedUslugaComplexAttributeList': '["oper"]',
            'UslugaComplex_Date': oper_date,  # дата операции
            'PersonAge': '',  # забирать из запроса на поиск пациента
            'query': f'A{code}',  # код операции???
            'Person_id': self.person_id,  # забирать из запроса на поиск пациента
            'uslugaCategoryList': '["gost2011"]',
            'EvnUsluga_pid': evnsection_id,  # EvnSection_id при создании случая госпитализации
            'LpuSection_pid': '380101000015688',  # const - id отделения
        }

        response = self._connect.post('https://ecp38.is-mis.ru/',
                                      params=params,
                                      headers=self._headers_ecp,
                                      data=data).json()
        return response.json()

    def create_evn(self,
                   date_start: str,
                   time_start: str,
                   type_hospitalization: str,
                   date_of_referral: str,
                   number_of_referral: str,
                   other_hosp: str,
                   org_id: str,
                   med_personal_id: str,
                   med_staff_fact_id: str
                   ):
        """Создаёт случай госпитализации"""

        params = {
            'c': 'EvnPS',
            'm': 'saveEvnPS',
        }

        data = [
            ('MesRegion_id', ''),
            ('LpuSectionBedProfile_id', '380101000000332'),
            ('childPS', 'false'),
            ('EvnPS_IsPLAmbulance', '1'),
            ('Diag_eid', ''),
            ('addEvnSection', '1'),
            ('LpuSection_id', '380101000015688'),  # ID травматолого-ортопедического отделения
            ('MedPersonal_id', med_personal_id),
            ('MedStaffFact_id', med_staff_fact_id),
            ('isAutoCreate', '1'),
            ('vizit_direction_control_check', '0'),
            ('ignoreParentEvnDateCheck', '0'),
            ('ignoreEvnPSDoublesCheck', '1'),  # 0 - проверка пересечения случаев в ЕЦП, 1 - игнорирование этой проверки
            ('ignoreEvnPSTimeDeseaseCheck', '0'),
            ('ignoreCheckKSGisEmpty', '0'),
            ('ignoreEvnPSHemoDouble', '0'),
            ('ignoreEvnPSHemoLong', '0'),
            ('ignoreMorbusOnkoDrugCheck', '0'),
            ('ignoreCheckMorbusOnko', '0'),
            ('ignoreDocumentsCheck', '1'),
            ('ignorePersonAgeByMedSpecCheck', '0'),
            ('checkMoreThanOneEvnPSToEvnDirection', '1'),
            ('accessType', ''),
            ('EvnSection_IsPaid', ''),
            ('EvnPS_IndexRep', ''),
            ('EvnPS_IndexRepInReg', ''),
            ('Lpu_id', '10379'),  # !
            ('EvnPS_id', '0'),
            ('EvnSectionPriem_id', '0'),
            ('EvnPS_IsTransit', '0'),
            ('ChildLpuSection_id', '380101000015688'),  # !
            ('EvnPS_IsPrehospAcceptRefuse', ''),
            ('EvnPS_PrehospAcceptRefuseDT', ''),
            ('EvnPS_PrehospWaifRefuseDT', ''),
            ('EvnDirection_id', '0'),
            ('EvnDirectionHTM_id', ''),
            ('DirType_id', ''),
            ('EvnDirectionExt_id', '0'),
            ('EvnQueue_id', '0'),
            ('PrehospStatus_id', '0'),
            ('Person_id', self.person_id),
            ('PersonEvn_id', self.person_evn_id),
            ('Server_id', self.server_id),
            ('EvnPS_IsZNO', '1'),
            ('EvnPS_IsZNORemove', ''),
            ('EvnInfectNotifyPediculos_id', ''),
            ('PrimaryInspectionONMKPatient_id', ''),
            ('EvnInfectNotifyScabies_id', ''),
            ('EvnPS_IsCont', '1'),
            ('EvnPS_NumCard', self._evn_number),
            ('PayType_id', '380101000000021'),
            ('PayContract_id', ''),
            ('PolisDMS_id', ''),
            ('EvnPS_setDate', date_start),
            ('EvnPS_setTime', time_start),
            ('EvnPS_IsWithoutDirection', '1'),
            ('PrehospDirect_id', other_hosp),  # при плановой госпитализации значение "2" означает другая МО
            ('Org_did', org_id),  # "Org_id"
            ('MedStaffFact_did', ''),
            ('MedStaffFact_TFOMSCode', ''),
            ('EvnDirection_Num', number_of_referral),  # номер направления при плановой госпитализации
            ('EvnDirection_setDate', date_of_referral),  # дата выдачи направления
            ('PrehospArrive_id', '1'),
            ('CmpCallCard_id', ''),
            ('Diag_did', ''),
            ('DiagValidityType_id', ''),
            ('DiagSetPhase_did', ''),
            ('EvnPS_PhaseDescr_did', ''),
            ('PrehospTraumaScale_Value', ''),
            ('ResultECG', ''),
            ('ScaleLams_id', ''),
            ('ScaleLams_Value', ''),
            ('EvnPS_IsImperHosp', '1'),
            ('EvnPS_IsShortVolume', '1'),
            ('EvnPS_IsWrongCure', '1'),
            ('EvnPS_IsDiagMismatch', '1'),
            ('LpuSectionTransType_id', ''),
            ('PrehospType_id', type_hospitalization),  # значение 2 при плановой
            ('EvnPS_HospCount', ''),
            ('Okei_id', '100'),
            ('EvnPS_TimeDesease', ''),
            ('EvnPS_IsNeglectedCase', ''),
            ('PersonHeight_Height', ''),
            ('PersonWeight_Weight', ''),
            ('PersonVitalParam_SistolPress', ''),
            ('PersonVitalParam_DiastolPress', ''),
            ('PersonVitalParam_Temperature', ''),
            ('PersonVitalParam_BreathFrequency', ''),
            ('PersonVitalParam_Pulse', ''),
            ('PersonVitalParam_HeartFrequency', ''),
            ('RepositoryObserv_SpO2', ''),
            ('CovidType_id', ''),
            ('RepositoryObserv_FluorographyDate', ''),
            ('DiagConfirmType_id', ''),
            ('LungInjuryDegreeType_id', ''),
            ('TraumaCircumEvnPS_Name', ''),
            ('TraumaCircumEvnPS_setDTDate', ''),
            ('TraumaCircumEvnPS_setDTTime', ''),
            ('EvnPS_IsUnport', ''),
            ('EntranceModeType_id', ''),
            ('LpuSection_pid', ''),
            ('MedStaffFact_pid', ''),
            ('DiagValidityType_id', ''),
            ('DiagSetPhase_pid', ''),
            ('EvnPS_PhaseDescr_pid', ''),
            ('EvnPSEditWindow_OpenMorbusButton', 'Открытые заболевания'),
            ('EvnPS_CmpTltDate', ''),
            ('EvnPS_CmpTltTime', ''),
            ('ThrombolysisBSMP_58', ''),
            ('EvnPS_IsActive', '1'),
            ('DeseaseType_id', ''),
            ('TumorStage_id', ''),
            ('Diag_spid', ''),
            ('EvnPS_BiopsyDate', ''),
            ('FamilyContact_msgDate', ''),
            ('FamilyContact_msgTime', ''),
            ('FamilyContact_IsInfoAgree', ''),
            ('FamilyContact_FIO', ''),
            ('FamilyContact_Phone_Hidden', ''),
            ('FamilyContact_Phone', ''),
            ('FamilyContactPerson_id', ''),
            ('VologdaFamilyContact_FIO', ''),
            ('VologdaFamilyContact_Phone', ''),
            ('Pediculos_id', ''),
            ('EvnDiagPSPediculos_id', ''),
            ('isExamPediculosisScabies', '1'),
            ('isPediculos', '1'),
            ('PediculosDiag_id', ''),
            ('Pediculos_Sanitation_setDate', ''),
            ('Pediculos_Sanitation_setTime', ''),
            ('Scabies_id', ''),
            ('EvnDiagPSScabies_id', ''),
            ('isScabies', '1'),
            ('ScabiesDiag_id', ''),
            ('Scabies_Sanitation_setDate', ''),
            ('Scabies_Sanitation_setTime', ''),
            ('Pediculos_isPrint', ''),
            ('buttonPrint058', ''),
            ('EvnPS_OutcomeDate', ''),
            ('EvnPS_OutcomeTime', ''),
            ('LeaveType_prmid', ''),
            ('LpuSection_eid', '380101000015688'),  # !
            ('LpuSectionWard_id', ''),
            ('LpuSectionBedProfileLink_id', '380101000000438'),  # !
            ('PrehospWaifRefuseCause_id', ''),
            ('MesRegion_id', ''),
            ('MedicalCareFormType_id', ''),
            ('ResearchObservEmergencyReason_id', ''),
            ('LpuSectionProfile_id', '380101000000301'),
            ('MedStaffFact_tid', ''),
            ('MedStaffFact_sid', med_staff_fact_id),
            ('UslugaComplex_id', ''),
            ('ResultClass_id', ''),
            ('ResultDeseaseType_id', ''),
            ('LeaveType_fedid', ''),
            ('ResultDeseaseType_fedid', ''),
            ('EvnPS_PatientRefuse', '1'),
            ('DiagSetPhase_aid', ''),
            ('EvnPS_IsWaif', '1'),
            ('EvnCostPrint_setDT', ''),
            ('EvnCostPrint_Number', ''),
            ('EvnCostPrint_IsNoPrint', ''),
        ]

        response = self._connect.post('https://ecp38.is-mis.ru/',
                                      params=params,
                                      headers=self._headers_ecp,
                                      data=data)
        return response.json()


def entry(connect: Session, login: str, password: str):
    """Запрос авторизации с логином и паролем"""

    headers_enter = {
        'user-agent': FakeUserAgent().random
    }

    params = {
        'c': 'main',
        'm': 'index',
        'method': 'Logon',
        'login': f'{login}',
    }

    data = {
        'login': f'{login}',
        'psw': f'{password}',
        'swUserRegion': '',
        'swUserDBType': '',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers_enter, data=data)

    return response.json()
