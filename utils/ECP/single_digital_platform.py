from datetime import datetime

from fake_useragent import FakeUserAgent


def calculate_date(start_date: str, end_date: str) -> int:
    s_date = datetime.strptime(start_date, '%d.%m.%Y')
    e_date = datetime.strptime(end_date, '%d.%m.%Y')
    delta = (e_date - s_date).days
    return delta


def entry(connect, login: str, password: str):
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


def search_patient(connect, name: str, surname: str, patronymic: str, birthday: str):
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
        'PersonSurName_SurName': surname,
        'ParentARM': '',
        'PersonFirName_FirName': name,
        'PersonSecName_SecName': patronymic,
        'PersonBirthDay_BirthDay': birthday,
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

    response_search = connect.post('https://ecp38.is-mis.ru/', params=params_search, headers=headers_search,
                                   data=data_search)
    return response_search.json().get('data')


def get_evn_number(connect):
    """Получает номер случая или выписки"""

    headers = {
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

    params = {
        'c': 'EvnPS',
        'm': 'getEvnPSNumber',
    }

    data = {
        'year': '2025',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_EVN(
        connect,
        patient_id: str,
        patient_person_evn_id: str,
        patient_server_id: str,
        numcard: str,
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
    """Создаёт карту выбывшего из стационара"""
    headers = {
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
        ('Person_id', patient_id),
        ('PersonEvn_id', patient_person_evn_id),
        ('Server_id', patient_server_id),
        ('EvnPS_IsZNO', '1'),
        ('EvnPS_IsZNORemove', ''),
        ('EvnInfectNotifyPediculos_id', ''),
        ('PrimaryInspectionONMKPatient_id', ''),
        ('EvnInfectNotifyScabies_id', ''),
        ('EvnPS_IsCont', '1'),
        ('EvnPS_NumCard', numcard),
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

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_data(
        connect,
        date_start: str,
        date_end: str,
        ksg_val: str,
        ksg_mes_tid: str,
        ksg_mestarif_id: str,
        patient_id: str,
        patient_person_evn_id: str,
        patient_server_id: str,
        ksg_mes_old_usluga_complex_id: str,
        time_start: str,
        time_end: str,
        ksg_coeff: str,
        evn_section_id,
        evn_section_pid,
        diag_id,
        med_staff_fact_id: str,
        med_personal_id: str
):
    """Сохраняет данные выписки и переводит пациенты в выписанных"""
    headers = {
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
        'x-requested-with': 'XMLHttpRequest',
    }

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
        ('EvnSection_disDate', f'{date_start}'),
        ('EvnSection_setDate', f'{date_end}'),
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
        ('EvnSection_KoikoDni', f'{calculate_date(date_start, date_end)}'),
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
        ('EvnSection_id', f'{evn_section_id}'),
        ('EvnSection_pid', f'{evn_section_pid}'),
        ('EvnSection_IsPaid', ''),
        ('EvnSection_IndexRep', ''),
        ('EvnSection_IndexRepInReg', ''),
        ('MedPersonal_aid', '0'),
        ('MedPersonal_did', '0'),
        ('MedPersonal_id', med_personal_id),
        ('Person_id', f'{patient_id}'),
        ('PersonEvn_id', f'{patient_person_evn_id}'),
        ('Server_id', f'{patient_server_id}'),
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
        ('EvnSection_setDate', f'{date_start}'),
        ('EvnSection_disDate', f'{date_end}'),
        ('EvnSection_setTime', f'{time_start}'),
        ('EvnSection_disTime', f'{time_end}'),
        ('EvnSection_IsAdultEscort', '1'),  # const
        ('EvnSection_IsMedReason', '1'),  # проверить не индекс ли заключительного диагноза, если да -> const
        ('EvnSection_AdultEscortPeriod', ''),
        ('LpuSection_id', '380101000015688'),  # Травматологии и ортопедии
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
        ('Diag_id', f'{diag_id}'),
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
        ('ResultDesease_id', '380101000000002'),  # улучшение (на конце: выздоровление - 1, без перемен - 3, ухудшение - 4)
        ('LeaveCause_id', '5'), # планово (самовольный уход - 1, инициатива больного - 2, нарушение режима - 3, эпидпоказания - 4, экстренно - 32)
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
        ('EvnSection_PlanDisDT', f'{date_end}'),
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

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return [response.status_code, response.json()]


def mkb(connect, letter: str):
    """Все коды МКБ по литере"""

    headers_mkb = {
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

    params_mkb = {
        'c': 'MongoDBWork',
        'm': 'getData',
        'object': 'Diag',
    }

    data_mkb = f"where=where%20(Diaglevel_id%20%3D%204%20)%20and%20Diag_Code%20like%20'{letter}%25'%20and%20(Diag_begDate%20is%20null%20or%20Diag_begDate%20%3C%3D%20'2023-10-23')%20and%20(Diag_endDate%20is%20null%20or%20Diag_endDate%20%3E%3D%20'2023-10-23')%20&Diag_id=&Diag_pid=&DiagLevel_id=&Diag_Code=&Diag_Name=&Diag_begDate=&Diag_endDate=&PersonAgeGroup_Code=&Sex_Code=&DiagFinance_IsOms=&DiagFinance_IsAlien=&DiagFinance_IsFacult=&DiagFinance_IsHealthCenter=&DiagFinance_IsRankin=&PersonRegisterType_List=&MorbusType_List=&DeathDiag_IsLowChance=&Diag_IsPairedOrgans=&DiagRRS=&VimisDiag_id=&VimisType_id=&VimisDiag_group=&remove=&intersection=&object=Diag"

    response = connect.post('https://ecp38.is-mis.ru/', params=params_mkb, headers=headers_mkb, data=data_mkb)
    return response.json()


def get_KSG_KOEF(connect, date_start: str, date_end: str, patient_id: str, diagnosis_id: str):
    """Запрос на получение КСГ и коэффициента"""

    headers = {
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

    params = {
        'c': 'EvnSection',
        'm': 'loadKSGKPGKOEF',
    }

    data = {
        'EvnSection_setDate': f'{date_start}',
        'EvnSection_disDate': f'{date_end}',
        'Person_id': f'{patient_id}',
        'EvnSection_id': '0',
        'PayType_id': '380101000000021',
        'Diag_id': f'{diagnosis_id}',
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

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def create_template(connect, person_evn_id, med_staff_fact_id):
    """Создаёт пустой шаблон выписки"""
    headers = {
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

    params = {
        'c': 'EvnXml',
        'm': 'createEmpty',
    }

    data = {
        'itemSectionCode': 'EvnXmlEpikriz',
        'Evn_id': f'{person_evn_id}',
        'XmlTemplate_id': '380101000189495',
        'XmlType_id': '10',
        'isSelect': 'true',
        'MedStaffFact_id': med_staff_fact_id,
        'Server_id': '0',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def update_research_evn_template(connect, template_id, text):
    """Заполняет поле обследование в выписке"""

    headers = {
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
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'updateContent',
    }

    data = {
        'EvnXml_id': f'{template_id}',
        'name': 'autoname31',
        'value': f'<p><br>5. Результаты проведенного исследования: {text}</p>',
        'isHTML': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.status_code


def update_treatment_evn_template(connect, template_id, text):
    """Заполняет поле лечение в выписке"""

    headers = {
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
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'updateContent',
    }

    data = {
        'EvnXml_id': f'{template_id}',
        'name': 'autoname91',
        'value': f'<p><br>6. Проведенное лечение и его эффективность: {text}</p>',
        'isHTML': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.status_code


def update_recommendation_evn_template(connect, template_id, text):
    """Заполняет поле рекомендации в выписке"""

    headers = {
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
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EvnXml',
        'm': 'updateContent',
    }

    data = {
        'EvnXml_id': f'{template_id}',
        'name': 'autoname96',
        'value': f'<p><br>7. Рекомендации: {text}</p>',
        'isHTML': '1',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.status_code


def get_EMD_data(connect):
    """Пока не понятное что-то для электронной подписи"""
    headers = {
        'authority': 'ecp38.is-mis.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-kl-kav-ajax-request': 'Ajax_Request',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EMD',
        'm': 'loadEMDSignWindow',
        '_dc': '1699334062413',
    }

    data = {
        'EMDRegistry_Objects': 'false',
        'EMDRegistry_ObjectName': 'EvnXml',
        'EMDRegistry_ObjectIDs': '["380101021673847"]', # const
        'isMOSign': 'false',
        'isDocArray': 'false',
        'isMedikata': 'false',
        'MedService_id': '',
        'page': '1',
        'start': '0',
        'limit': '25',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_EMD_list(connect):
    """Получает данные для подписи"""

    headers = {
        'authority': 'ecp38.is-mis.ru',
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://ecp38.is-mis.ru',
        'referer': 'https://ecp38.is-mis.ru/?c=promed',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-kl-kav-ajax-request': 'Ajax_Request',
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EMD',
        'm': 'loadEMDCertificateList',
        '_dc': '1699334062689',
    }

    data = {
        'excludeExpire': 'true',
        'excludeIsNotUse': 'true',
        'pmUser_id': '418031072342',
        'isMOSign': '',
        'page': '1',
        'start': '0',
        'limit': '25',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def create_certificate(connect, med_staff_fact_id): # разобрать
    """Создаёт сертификат для подписи"""
    headers = {
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
        'x-requested-with': 'XMLHttpRequest',
    }

    params = {
        'c': 'EMD',
        'm': 'generateEMDRegistry',
    }

    data = {
        'EMDRegistry_ObjectName': 'EvnXml',
        'EMDRegistry_ObjectID': '380101022087844',
        'MedStaffFact_id': med_staff_fact_id,
        'EMDCertificate_id': '11908',
        'isDocArray': 'false',
        'isPreview': '',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.status_code


def get_referral_for_hospitalization(connect,
                                     beg_date: str,
                                     end_date: str,
                                     surname: str,
                                     name: str,
                                     patronymic: str):
    """Возвращает направления на госпитализацию.
    Можно забрать Diag_Code (код МКБ), Diag_Name (код МКБ с описанием), Diag_id (идентификатор кода МКБ из бд ЕЦП),
    DirType_Name (тип госпитализации), DirType_id (идентификатор типа госпитализации в бд ЕЦП),
    LpuSectionBedProfile_id (профиль койки "380101000000332"-травматология, указывается не всегда),
    LpuSectionProfile_id (профиль отделения "380101000000301"-травматология),
    EvnDirection_Descr (текст обоснования), EvnDirection_Num (номер обоснования(?))"""
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
        'c': 'EvnDirection',
        'm': 'loadEvnDirectionJournal',
    }

    data = {
        'EvnDirection_id': '',
        'Lpu_id': '',
        'PayType_id': '',
        'Lpu_Name': '',
        'Org_Nick': '',
        'Org_Name': '',
        'Org_id': '',
        'EvnDirection_Num': '',
        'DirType_id': '1',
        'DirType_Code': '',
        'DirType_Name': '',
        'DirFailType_Name': '',
        'LpuSectionProfile_id': '380101000000301',  # профиль "Травматология и ортопедия"
        'LpuSectionProfile_Name': '',
        'LpuSection_id': '380101000001853',  # ID отделения
        'LpuSection_did': '',
        'LpuSection_Name': '',
        'EvnQueue_Days': '',
        'EvnVK_id': '',
        'LpuVK_did': '',
        'EvnDirectionVK_id': '',
        'SMEvnPrescrVK_id': '',
        'HTMEvnPrescrVK_id': '',
        'EvnDirectionHTMCount': '',
        'EvnDirection_setDate': '',
        'EvnDirection_setTime': '',
        'TimetableStac_setDate': '',
        'PrehospStatus_Name': '',
        'EvnDirection_desDT': '',
        'Person_id': '',
        'PersonEvn_id': '',
        'Server_id': '',
        'Person_Fio': '',
        'Person_Birthday': '',
        'Diag_Name': '',
        'EvnDirection_Descr': '',
        'MedPersonal_id': '',
        'MedPersonal_Fio': '',
        'MedPersonalProfile_Name': '',
        'IsWaitingVK': '',
        'EvnStatusHistory_Cause': '',
        'LeaveType_Name': '',
        'EvnStatus_id': '',
        'TalonHTM_id': '',
        'EvnPrescrVkTalon_id': '',
        'VkProtocol_id': '',
        'CareStageType_id': '',
        'TalonHTM_IsSigned': '',
        'EvnDirectionHTM_id': '',
        'object': 'EvnDirection',
        'limit': '100',
        'start': '0',
        'beg_date': beg_date,
        'end_date': end_date,
        'Person_SurName': surname,
        'Person_FirName': name,
        'Person_SecName': patronymic,
        'Lpu_isFmo': 'false',
        'Lpu_isHtm': 'true',
        'EvnStatusCause_id': '',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def get_list_of_discharge_notes_for_signature(connect):  # разобрать!!!
    """Список не подписанных выписных"""

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
        'c': 'EMDSignWin',
        'm': 'searchDocs',
        '_dc': '1711851258257',  # ???
    }

    data = {
        'EMDDocumentTypeLocal_id': '100067',
        'Lpu_id': '10379',
        'EMDOrg_id': '10379',
        'LpuBuilding_id': '380101000001853',
        'LpuSection_id': '380101000015688',
        'MedPersonal_id': '380101000004549',
        'PersonWork_id': 'null',
        'Evn_insDT_period': '',
        'Evn_updDT_period': '',
        'Doc_Num': '',
        'Person_FIO': '',
        'isWithoutSign': 'on',
        'isNecessaryES': '1',
        'hidedeletedoc': '1',
        'page': '1',
        'start': '0',
        'limit': '100',
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data)
    return response.json()


def save_implant_type_link(connect, evn_usluga_oper_id: str, implant_id: str, implant_name: str):
    """Добавляет имплантированное изделие (тестировать)"""
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
        'm': 'saveEvnUslugaImplantTypeLink',
    }

    data = {
        'EvnUslugaImplantTypeLink_id': '',
        'EvnUsluga_id': evn_usluga_oper_id,  # EvnUslugaOper_id
        'ImplantType_id': implant_id,  # из implant_info.json
        'EvnUslugaImplantTypeLink_SerNum': '0000',  # серийный номер
        'ImplantType_Name': implant_name,   # из implant_info.json, можно не указывать
    }

    response = connect.post('https://ecp38.is-mis.ru/', params=params, headers=headers, data=data).json()
    return response
