from datetime import datetime
from pprint import pprint

from fake_useragent import FakeUserAgent
from requests import Session


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
        headers = {
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

        response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
        return response.get('data')


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

    def get_all_patients_stac(self, date: str):
        """Получает пациентов находящихся в стационаре"""

        params = {
            'c': 'EvnSection',
            'm': 'getSectionTreeData',
        }

        data = {
            'object': 'LpuSection',
            'object_id': 'LpuSection_id',
            'object_value': '380101000015688',
            'level': '0',
            'LpuSection_id': '380101000015688',
            'ARMType': 'stac',
            'date': date,  # дата строкой в формате dd.mm.YYYY
            'filter_Person_F': '',
            'filter_Person_I': '',
            'filter_Person_O': '',
            'filter_PSNumCard': '',
            'filter_Person_BirthDay': '',
            'filter_MedStaffFact_id': '',
            'MedService_id': '0',
            'node': 'root',
        }

        response = self._connect.post('https://ecp38.is-mis.ru/',
                                      params=params,
                                      headers=self._headers_ecp,
                                      data=data).json()
        return response


class HistoryEcp(PatientECP):
    """Класс случай госпитализации ЕЦП"""

    def __init__(self, connect: Session, name: str, surname: str, patronymic: str, birthday: str):
        super().__init__(connect, name, surname, patronymic, birthday)
        self._evn_number = self.__get_evn_number()

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
