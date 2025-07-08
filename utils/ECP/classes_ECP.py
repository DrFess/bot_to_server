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

    def set_treating_doctor(
            self,
            med_personal_id: str,
            med_staf_fact_id: str
    ):
        """Назначает лечащего врача"""

        params = {
            'c': 'EvnSection',
            'm': 'setEvnSectionMedPersonal',
        }

        data = {
            'LpuSection_id': LPU_SECTION_ID_TRAUMA,  # id травматологии
            'EvnSection_id': self.evn_section_id,
            'Person_id': self.person_id,
            'PersonEvn_id': self.person_evn_id,
            'Server_id': self.server_id,
            'MedPersonal_id': med_personal_id,  # назначаемого врача
            'MedStaffFact_id': med_staf_fact_id,  # назначаемого врача
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data).json()
        return response

    def get_mkb_code(self, letter: str):
        """Все коды МКБ по литере"""

        params_mkb = {
            'c': 'MongoDBWork',
            'm': 'getData',
            'object': 'Diag',
        }

        data_mkb = f"where=where%20(Diaglevel_id%20%3D%204%20)%20and%20Diag_Code%20like%20'{letter}%25'%20and%20(Diag_begDate%20is%20null%20or%20Diag_begDate%20%3C%3D%20'2023-10-23')%20and%20(Diag_endDate%20is%20null%20or%20Diag_endDate%20%3E%3D%20'2023-10-23')%20&Diag_id=&Diag_pid=&DiagLevel_id=&Diag_Code=&Diag_Name=&Diag_begDate=&Diag_endDate=&PersonAgeGroup_Code=&Sex_Code=&DiagFinance_IsOms=&DiagFinance_IsAlien=&DiagFinance_IsFacult=&DiagFinance_IsHealthCenter=&DiagFinance_IsRankin=&PersonRegisterType_List=&MorbusType_List=&DeathDiag_IsLowChance=&Diag_IsPairedOrgans=&DiagRRS=&VimisDiag_id=&VimisType_id=&VimisDiag_group=&remove=&intersection=&object=Diag"

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params_mkb, headers=self._headers, data=data_mkb)
        return response.json()

    def get_KSG_KOEF(self, date_start: str, date_end: str, diagnosis_id: str):
        """Запрос на получение КСГ и коэффициента"""

        params = {
            'c': 'EvnSection',
            'm': 'loadKSGKPGKOEF',
        }

        data = {
            'EvnSection_setDate': f'{date_start}',
            'EvnSection_disDate': f'{date_end}',
            'Person_id': self.person_id,
            'EvnSection_id': '0',
            'PayType_id': '380101000000021',
            'Diag_id': diagnosis_id,
            'HTMedicalCareClass_id': '',
            'EvnSection_IndexRep': '',
            'EvnSection_IndexRepInReg': '',
            'EvnSection_pid': '',
            'LpuSection_id': '380101000015688',
            'LpuSectionBedProfile_id': '380101000000332',
            'LpuSectionProfile_id': '380101000000301',
            'LpuUnitType_id': '1',
            'DrugTherapyScheme_ids': '',
            'MesDop_ids': '',
            'RehabScale_id': '',
            'CureResult_id': '',
            'EvnSection_SofaScalePoints': '',
            'EvnSection_IsAdultEscort': '1',
            'EvnSection_Absence': '',
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def save_data(
            self,
            date_start: str,
            date_end: str,
            koiko_dni: str,
            ksg_val: str,
            ksg_mes_tid: str,
            ksg_mestarif_id: str,
            ksg_mes_old_usluga_complex_id: str,
            time_start: str,
            time_end: str,
            ksg_coeff: str,
            diag_id,
            med_staff_fact_id: str,
            med_personal_id: str
    ):
        """Сохраняет данные выписки и переводит пациенты в выписанных"""

        params = {
            'c': 'EvnSection',
            'm': 'saveEvnSection',
        }

        data = [
            ('checkIsOMS', '1'),
            ('DrugTherapyScheme_ids', ''),
            ('MesDop_ids', ''),
            ('AdditionalFields', '{"4":1}'),
            ('AdditionalHospitalizationResultFields', ''),
            ('AdditionalHospitalizationResultCardiologyFields', ''),
            ('AdditionalNewbornResultFields', ''),
            ('AdditionalNeurologyFields', ''),
            ('AdditionalCardiologyFields', ''),
            ('NatureOfCurrent', '{}'),
            ('EvnSection_disDate', date_start),
            ('EvnSection_setDate', date_end),
            ('silentSave', '0'),
            ('isAutoCreate', '0'),
            ('editAnatom', '1'),
            ('vizit_direction_control_check', '0'),
            ('ignoreDiagKSGCheck', '0'),
            ('ignoreEDiagProfilesCheck', '0'),
            ('ignoreParentEvnDateCheck', '0'),
            ('ignoreEvnPSDoublesCheck', '1'),
            ('ignoreCheckEvnUslugaChange', '0'),
            ('ignoreCheckEvnUslugaDates', '0'),
            ('ignoreCheckKSGisEmpty', '0'),
            ('ignoreCheckCardioFieldsEmpty', '0'),
            ('ignoreCheckTimePainFieldsEmpty', '0'),
            ('ignoreCheckPointsGraceFieldsEmpty', '0'),
            ('skipPersonRegisterSearch', '0'),
            ('ignoreEvnUslugaHirurgKSGCheck', '0'),
            ('ignoreCheckTNM', '0'),
            ('ignoreCheckMorbusOnko', '0'),
            ('ignoreMorbusOnkoDrugCheck', '0'),
            ('ignoreCheckConciliumOnko', '0'),
            ('ignoreFirstDisableCheck', '0'),
            ('ignoreDocumentsCheck', '1'),
            ('ignorePersonAgeByMedSpecCheck', '0'),
            ('ignoreDiagSmallChild', '0'),
            ('ignoreFillnessKSG', '0'),
            ('ignoreCovidDrugTherapyEmpty', '0'),
            ('ignoreCovidDrugTherapyDiffs', '0'),
            ('ignoreMorbusKasByInternalTransfer', '0'),
            ('ignoreMorbusKasByTransferOut', '0'),
            ('EvnSection_KoikoDni', koiko_dni),
            ('ignoreControlPayTypeUslAndEvnSection', '0'),
            ('ignoreControlDatePrescrAndDirectionToEvnSection', '0'),
            ('ignoreDiagValidityType', '0'),
            ('ignoreControlOMS', '0'),
            ('ignoreCheckEvnUslugaInESOMS', '0'),
            ('KSG_val', f'{ksg_val}'),
            ('LeaveType_SysNick', 'ksleave'),
            ('Mes_tid', f'{ksg_mes_tid}'),
            ('PrehospTrauma_id', ''),
            ('Mes_kid', ''),
            ('MesTariff_id', f'{ksg_mestarif_id}'),
            ('MesTariff_sid', ''),
            ('accessType', 'edit'),
            ('Evn_Name', ''),
            ('EvnDiagPS_id', '0'),
            ('EvnDie_id', '0'),
            ('EvnLeave_id', '0'),
            ('EvnOtherLpu_id', '0'),
            ('EvnOtherSection_id', '0'),
            ('EvnOtherSectionBedProfile_id', '0'),
            ('EvnSection_Index', '-1'),
            ('EvnOtherStac_id', '0'),
            ('EvnSection_id', self.evn_section_id),
            ('EvnSection_pid', self.evn_ps_id),
            ('EvnSection_IsPaid', ''),
            ('EvnSection_IndexRep', ''),
            ('EvnSection_IndexRepInReg', ''),
            ('MedPersonal_aid', '0'),
            ('MedPersonal_did', '0'),
            ('MedPersonal_id', med_personal_id),
            ('Person_id', self.person_id),
            ('PersonEvn_id', self.person_evn_id),
            ('Server_id', self.server_id),
            ('EvnSection_IsCardioCheck', '0'),
            ('MesOldUslugaComplex_id', f'{ksg_mes_old_usluga_complex_id}'),
            ('LpuSectionBedProfile_id', ''),
            ('EvnSection_IsZNO', '1'),
            ('EvnSection_IsZNORemove', ''),
            ('EvnSection_IsMultiKSG', ''),
            ('TalonHTM_id', ''),
            ('EvnDirectionHTM_id', ''),
            ('TalonHTM_IsSigned', ''),
            ('EvnDirectionHTM_begDate', ''),
            ('EvnDiagPS_setDT', ''),
            ('EvnSection_setDate', date_start),
            ('EvnSection_disDate', date_end),
            ('EvnSection_setTime', time_start),
            ('EvnSection_disTime', time_end),
            ('EvnSection_IsAdultEscort', '1'),  # const
            ('EvnSection_IsMedReason', '1'),  # проверить не индекс ли заключительного диагноза, если да -> const
            ('EvnSection_AdultEscortPeriod', ''),
            ('LpuSection_id', LPU_SECTION_ID_TRAUMA),  # Травматологии и ортопедии
            ('LpuSectionTransType_id', ''),
            ('EvnSection_IsMeal', '1'),  # const
            ('LpuSectionProfile_id', '380101000000301'),  # id профиля Травматологии и ортопедии
            ('LpuSectionBedProfileLink_fedid', '380101000000438'),  # id профиля койки
            ('LpuSectionWard_id', ''),
            ('Bed_id', ''),
            ('NewLpuSectionBedProfile_id', ''),
            ('BedFund_setDate', ''),
            ('GetRoom_id', ''),
            ('GetBed_id', ''),
            ('EvnSection_insideNumCard', ''),
            ('PayType_id', '380101000000021'),  # "ОМС" скорее всего const
            ('PayContract_id', ''),
            ('PolisDMS_id', ''),
            ('TariffClass_id', ''),
            ('MedStaffFact_id', med_staff_fact_id),
            ('Diag_id', diag_id),
            ('HeartFailureStage_54', ''),
            ('HeartFailureClass_55', ''),
            ('StenocardiaFuncClass_id', ''),
            ('PulmonaryHypertensionFuncClass_id', ''),
            ('DiagValidityType_id', '3'),  # "Заключительный клинический диагноз" const
            ('DiagSetPhase_id', '2'),  # "Средней тяжести" состояние при поступлении const ("удовлетворительное" - 1)
            ('EvnSection_PhaseDescr', ''),
            ('Diag_cid', ''),
            ('DeseaseBegTimeType_id', ''),
            ('YesNo_148', ''),
            ('DeseaseType_id', ''),
            ('DiseaseCourseType_149', ''),
            ('DiseaseCourseType_150', ''),
            ('DiseaseCourseType_151', ''),
            ('DiseaseCourseType_152', ''),
            ('DiseaseCourseType_153', ''),
            ('DiseaseCourseType_154', ''),
            ('DrugTherapyScheme_id_0', ''),
            ('RehabScale_id', ''),
            ('RehabScale_vid', ''),
            ('EvnSection_SofaScalePoints', ''),
            ('TumorStage_id', ''),
            ('Diag_spid', ''),
            ('EvnSection_BiopsyDate', ''),
            ('PainIntensity_id', ''),
            ('MesDop_id_0', ''),
            ('HTMedicalCare_isAdjacentES', ''),
            ('HTMedicalCareType_id', ''),
            ('HTMedicalCareType_Code', ''),
            ('HTMedicalCareClass_id', ''),
            ('HTMedicalCareClass_Code', ''),
            ('HTMedicalCareType_Name', ''),
            ('HTMedicalCareClass_Name', ''),
            ('RankinScale_id', ''),
            ('RankinScale_oid', ''),
            ('EvnSection_NIHSSAfterTLT', ''),
            ('EvnSection_NIHSSLeave', ''),
            ('RankinScale_sid', ''),
            ('Mes_id', ''),
            ('Mes_sid', ''),
            ('StandartExecutionLink_id', ''),
            ('SurveyStandartExecution_id', ''),
            ('CureStandartExecution_id', ''),
            ('Diag_it_id', ''),
            ('Mes_it_id', ''),
            ('CerebralSymptoms_102', ''),
            ('CorticalActivity_103', ''),
            ('MeningealSyndrome_104', ''),
            ('Speech_105', ''),
            ('CranialNerves_106', ''),
            ('Sensitivity_107', ''),
            ('SpinalLesion_108', ''),
            ('PolyneuriticLesion_109', ''),
            ('MotorSystem_110', ''),
            ('CoordinationSystem_111', ''),
            ('ExtrapyramidalSystem_112', ''),
            ('AutonomicNervousSystem_113', ''),
            ('PelvicFunctions_114', ''),
            ('VertebralSyndrome_115', ''),
            ('IntracerebralHematoma_116', ''),
            ('tltDateTimeSMP', ''),
            ('ext-comp-2080', ''),
            ('ext-comp-2081', ''),
            ('cardiology_YesNo_119', ''),
            ('cardiology_StopFibrillationAtrial_120', ''),
            ('cardiology_StopFibrillationAtrialDT_121Date', ''),
            ('cardiology_StopFibrillationAtrialDT_121Time', ''),
            ('EvnSectionEditWindow_OpenMorbusButton', 'Открытые заболевания'),
            ('UslugaComplex_id', ''),
            ('EvnSection_Absence', ''),
            ('Mes_rid', ''),
            ('MesOldUslugaComplexLink_Number', ''),
            ('EvnSection_KSG', f'{ksg_val}'),
            ('EvnSection_KPG', ''),
            ('EvnSection_KOEF', f'{ksg_coeff}'),
            ('EvnSection_KPGKOEF', ''),
            ('EvnSection_CoeffCTP', '0'),
            ('EvnSection_IsST', ''),
            ('EvnSection_IsCardShock', ''),
            ('EvnSection_StartPainHour', ''),
            ('EvnSection_StartPainMin', ''),
            ('EvnSection_GraceScalePoints', ''),
            ('ACSType_id', ''),
            ('ONMKType_1', ''),
            ('KillipClass_2', ''),
            ('InfarctionECGType_3', ''),
            ('InfarctionAnamnesisType_4', '1'),
            ('TimeSymptomONMK_5', ''),
            ('ONMKDescr_42', ''),
            ('ONMKPeriod_43', ''),
            ('ONMKReason_44', ''),
            ('ONMKTreatment_45', ''),
            ('ClinicalScaleParameter_6', ''),
            ('ClinicalScaleInterpret_86', ''),
            ('ClinicalScaleInterpret_7', ''),
            ('ClinicalScaleInterpret_8', ''),
            ('ClinicalScaleASPECTS_57', ''),
            ('LAMS_79', ''),
            ('HemTransformation_87', ''),
            ('acs_MyocardialInfarctionType_53', ''),
            ('stenocardia_ClinicalClassStableIBS_130', ''),
            ('stenocardia_StenocardiaStressClass_131', ''),
            ('heartFailure_HeartFailureType_134', ''),
            ('SystemCoronaryRisk', ''),
            ('SystemCoronaryRiskInterpretation', ''),
            ('FibrillationAtrialType_132', ''),
            ('FibrillationAtrialForm_133', ''),
            ('AnatomicLocalHematomaONMK_id', ''),
            ('PregnancyEvnPS_Period', ''),
            ('EvnSection_BarthelIdx', ''),
            ('EvnSection_BarthelIdxEnd', ''),
            ('transplantation_YearTrans_188', ''),
            ('LeaveTypeFed_id', ''),
            ('LeaveType_id', '380101000000001'),
            ('EvnLeave_UKL', '1'),
            ('ResultDesease_id', '380101000000002'),
            # улучшение (на конце: выздоровление - 1, без перемен - 3, ухудшение - 4)
            ('LeaveCause_id', '5'),
            # планово (самовольный уход - 1, инициатива больного - 2, нарушение режима - 3, эпидпоказания - 4, экстренно - 32)
            ('EvnLeave_IsAmbul', '1'),  # const
            ('Org_oid', ''),
            ('LpuUnitType_oid', ''),
            ('LpuSection_oid', ''),
            ('LpuSectionBedProfile_oid', ''),
            ('LpuSectionBedProfileLink_fedoid', ''),
            ('MedStaffFact_did', ''),
            ('EvnDie_IsWait', ''),
            ('CureResult_id', ''),
            ('EvnSection_IsTerm', ''),
            ('EvnDie_IsAnatom', ''),
            ('EvnDie_expDate', ''),
            ('EvnDie_expTime', ''),
            ('AnatomWhere_id', ''),
            ('Org_aid', ''),
            ('LpuSection_aid', ''),
            ('MedStaffFact_aid', ''),
            ('Diag_aid', ''),
            ('DiagSetPhase_aid', '1'),
            ('PrivilegeType_id', ''),
            ('PayTypeERSB_id', ''),
            ('EvnSection_PlanDisDT', date_end),
            ('PrehospWaifRetired_id', ''),
            ('LeaveType_fedid', ''),
            ('ResultDeseaseType_fedid', ''),
            ('CerebralSymptoms_102', ''),
            ('CorticalActivity_103', ''),
            ('MeningealSyndrome_104', ''),
            ('Speech_105', ''),
            ('CranialNerves_106', ''),
            ('Sensitivity_107', ''),
            ('SpinalLesion_108', ''),
            ('PolyneuriticLesion_109', ''),
            ('MotorSystem_110', ''),
            ('CoordinationSystem_111', ''),
            ('ExtrapyramidalSystem_112', ''),
            ('AutonomicNervousSystem_113', ''),
            ('PelvicFunctions_114', ''),
            ('VertebralSyndrome_115', ''),
            ('IntracerebralHematoma_116', ''),
            ('PatientDynamics_117', ''),
            ('YesNo_118', ''),
            ('YesNo_119', ''),
            ('StopFibrillationAtrial_120', ''),
            ('StopFibrillationAtrialDT_121Date', ''),
            ('StopFibrillationAtrialDT_121Time', ''),
            ('MedPost_180_0', ''),
            ('Recommendations_181', ''),
            ('SpecialRemarks_182', ''),
        ]

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return [response.status_code, response.json()]

    def create_template(self, med_staff_fact_id):
        """Создаёт пустой шаблон выписки"""

        params = {
            'c': 'EvnXml',
            'm': 'createEmpty',
        }

        data = {
            'itemSectionCode': 'EvnXmlEpikriz',
            'Evn_id': self.evn_section_id,
            'XmlTemplate_id': '380101000189495',
            'XmlType_id': '10',
            'isSelect': 'true',
            'MedStaffFact_id': med_staff_fact_id,
            'Server_id': '0',
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.json()

    def update_evn_template(self, template_id, chapter: str, text: str):
        """Заполняет поле рекомендации в выписке"""

        params = {
            'c': 'EvnXml',
            'm': 'updateContent',
        }

        data = {
            'EvnXml_id': f'{template_id}',
            'name': chapter,
            'value': text,
            'isHTML': '1',
        }

        response = self._connect.post('https://ecp38.is-mis.ru/', params=params, headers=self._headers, data=data)
        return response.status_code


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
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'priority': 'u=0, i',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'main',
        'm': 'index',
        'method': 'Logon',
        'login': login,
    }

    data = {
        'login': login,
        'psw': password,
        'swUserRegion': '',
        'swUserDBType': '',
    }

    connect.get('https://ecp38.is-mis.ru/', headers=headers_enter)

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers_enter, data=data)

    return response.json()
