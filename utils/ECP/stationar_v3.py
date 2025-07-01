import json
from datetime import datetime
from pprint import pprint

from requests import Session

from settings import login_l2, password_l2, login, password, path_to_hospitalsJson, path_to_doctorsJson, \
    path_to_empoyeesJson, path_to_mkb_code
from utils.ECP.classes_ECP import CurrentPatientECP, HistoryEcp
from utils.ECP.single_digital_platform import get_all_patients_stac, entry
from utils.L2.classes_L2 import HistoryL2
from utils.L2.diaries import authorization_l2
from utils.L2.parse_l2 import get_all_patients_in_ward


def get_current_patients_l2_ecp(connect: Session) -> tuple:
    """Получает списки текущих пациентов L2 и ЕЦП"""
    authorization_l2(connect, login=login_l2, password=password_l2)
    patients_number = get_all_patients_in_ward('C3:C40')  # 'C3:C40'
    patients_number.extend(get_all_patients_in_ward('K3:K40'))

    current_patients_l2 = [
        HistoryL2(
            connect=connect,
            number=int(history_number)
        ) for history_number in patients_number if history_number.isdigit()]  # генератор перечень пациентов в L2

    day_today = datetime.today().strftime('%d.%m.%Y')
    entry(connect, login=login, password=password)
    patients_in_ecp_request = get_all_patients_stac(connect, day_today)

    current_patients_ecp = (
        CurrentPatientECP(
            connect=connect,
            person_evn_id=patient.get('PersonEvn_id'),
            person_id=patient.get('Person_id'),
            medpersonal_id=patient.get('MedPersonal_id'),
            evn_section_id=patient.get('EvnSection_id'),
            evn_ps_id=patient.get('EvnPS_id'),
            server_id=patient.get('Server_id'),
            ksg=patient.get('EvnSection_KSG')
        ) for patient in patients_in_ecp_request if patient.get('LpuSection_id') == '380101000015688')

    return current_patients_l2, current_patients_ecp


def add_patients_in_ecp(connect: Session) -> None:
    """Создаёт случай госпитализации, если пациента нет в госпитализированных"""
    current_patients = get_current_patients_l2_ecp(connect)

    fio_list = [patient_ecp.person_fio for patient_ecp in current_patients[1]]

    for item_l2 in current_patients[0]:
        if item_l2.fio not in list(fio_list):
            name = item_l2.fio.split(' ')[1]
            surname = item_l2.fio.split(' ')[0]
            patronymic = item_l2.fio.split(' ')[2]

            hospitalized_patient = HistoryEcp(
                connect,
                name=name,
                surname=surname,
                patronymic=patronymic,
                birthday=item_l2.birthday,
            )

            if hospitalized_patient.person_id:
                if item_l2.first_examination.get('Вид госпитализации') == 'экстренная':

                    date_start_normal = '.'.join(item_l2.first_examination.get('Дата поступления').split('-')[::-1])
                    hospitalized_patient.create_evn(
                        date_start=date_start_normal,
                        time_start=item_l2.first_examination.get('Время поступления'),
                        type_hospitalization='1',
                        date_of_referral='',
                        number_of_referral='',
                        other_hosp='',
                        org_id='',
                        med_personal_id='380101000004549',
                        med_staff_fact_id='380101000010385'
                    )
                    print(f'{item_l2.fio} добавлен в ЕЦП')
                elif item_l2.first_examination.get('Вид госпитализации') == 'плановая':

                    date_start_normal = '.'.join(item_l2.first_examination.get('Дата поступления').split('-')[::-1])
                    referring_hospital = item_l2.first_examination.get('Кем направлен больной')
                    with open(path_to_hospitalsJson, 'r') as file:
                        hospitals = json.load(file)
                        referring_hospital_id = hospitals.get(referring_hospital).get('Org_id')
                    hospitalized_patient.create_evn(
                        date_start=date_start_normal,
                        time_start=item_l2.first_examination.get('Время поступления'),
                        type_hospitalization='2',
                        date_of_referral=item_l2.first_examination.get('Дата выдачи направления'),
                        number_of_referral=item_l2.first_examination.get('Номер направления'),
                        other_hosp='2',
                        org_id=referring_hospital_id,
                        med_personal_id='380101000004549',
                        med_staff_fact_id='380101000010385'
                    )
                    print(f'{item_l2.fio} добавлен в ЕЦП')
                else:
                    print(f'{item_l2.fio} ошибка на этапе госпитализации - экстренная или плановая')
            else:
                print(f'{item_l2.fio} не могу найти такого в ЕЦП')
        else:
            print(f'{item_l2.fio} уже в ЕЦП')


def add_operation(connect: Session):
    """Добавляет услугу операции"""

    current_patients = get_current_patients_l2_ecp(connect)

    ecp_fio_dict = {patient_ecp.person_fio: (patient_ecp.ksg, patient_ecp)
                    for patient_ecp in current_patients[1]}

    for item in current_patients[0]:
        if item.operation:
            if len(item.operation) == 1:
                if not ecp_fio_dict.get(item.fio):
                    oper_date = '.'.join(item.operation.get(0).get('Дата проведения').split('-')[::-1])

                    oper_code = item.operation.get(0).get('Код операции').split(' ')[0].rstrip('.').lstrip('A').lstrip('А')

                    current_patient_ecp = ecp_fio_dict.get(item.fio)[1]
                    current_oper_code = current_patient_ecp.get_operation_code(code=oper_code, oper_date=oper_date)

                    with open(path_to_doctorsJson, 'r') as file:  # список словарей с данными врачей
                        doctors = json.load(file)

                    who_operate = item.operation.get(0).get('Оперировал').split(' ')[0]
                    who_operate_med_personal_id = doctors.get(who_operate).get('MedPersonal_id')
                    who_operate_med_staf_fact_id = doctors.get(who_operate).get('MedStaffFact_id')

                    start_date = item.operation.get(0).get('Дата проведения')
                    start_time = item.operation.get(0).get('Время начала')
                    end_date = item.operation.get(0).get('Дата окончания')
                    end_time = item.operation.get(0).get('Время окончания')
                    first_save = current_patient_ecp.save_oper_info(
                        medPersonal_id=who_operate_med_personal_id,
                        start_date=start_date,
                        start_time=start_time,
                        end_date=end_date,
                        end_time=end_time,
                        medStaffFact_id=who_operate_med_staf_fact_id,
                        oper_code=current_oper_code[0].get('UslugaComplex_id'),
                    )

                    oper_id = first_save.get('EvnUslugaOper_id')  # возвращает EvnUslugaOper_id == EvnUslugaOperBrig_pid

                    current_patient_ecp.add_operation_member(
                        medPersonal_id=who_operate_med_personal_id,
                        start_date=start_date,
                        evn_usluga_oper_id=oper_id,
                        medStaffFact_id=who_operate_med_staf_fact_id,
                        surgType_id='1'
                    )

                    anesthetist = item.operation.get(0).get('Анестезиолог')
                    with open(path_to_empoyeesJson, 'r') as file:
                        doctors_list = json.load(file)
                    for doctor in doctors_list:
                        if anesthetist == doctor.get('MedPersonal_Fin') and doctor.get(
                                'WorkData_MedStaff_endDate') is None:
                            anesthesiolog_med_personal_id = doctor.get('MedPersonal_id')
                            anesthesiolog_staf_fact_id = doctor.get('MedStaffFact_id')
                            current_patient_ecp.add_operation_member(
                                medPersonal_id=anesthesiolog_med_personal_id,
                                start_date=start_date,
                                evn_usluga_oper_id=oper_id,
                                medStaffFact_id=anesthesiolog_staf_fact_id,
                                surgType_id='4'
                            )
                            break

                    if item.operation.get(0).get('Метод обезболивания') == 'ЭТН':
                        anesthesia_class_id = '4'
                    elif item.operation.get(0).get('Метод обезболивания') == 'АМН':
                        anesthesia_class_id = '5'
                    else:
                        anesthesia_class_id = '21'

                    current_patient_ecp.save_oper_anesthesia(
                        evn_usluga_oper_anest_id=oper_id,
                        anesthesiaClass_id=anesthesia_class_id
                    )

                    operation_template = current_patient_ecp.create_empty_oper(
                        evn_id=oper_id,
                        medStaffFact_id=who_operate_med_staf_fact_id
                    )

                    protocol_text = item.operation.get(0).get('Ход операции')
                    current_patient_ecp.update_oper(
                        evn_xml_id=operation_template.get('EvnXml_id'),
                        text=protocol_text
                    )

                    title_operation = item.operation.get(0).get('Название операции')
                    if 'удаление' not in title_operation.lower():
                        if 'спиц' in protocol_text or 'стержень' in protocol_text or 'TEN' in protocol_text:
                            implant_id = '856'  # стержень
                            implant_title = 'Стержень костный ортопедический, нерассасывающийся'
                        elif 'винт' in protocol_text:
                            implant_id = '857'  # винт
                            implant_title = 'Винт костный ортопедический, нерассасывающийся, стерильный'
                        elif 'пластин' in protocol_text:
                            implant_id = '859'  # пластина
                            implant_title = 'Пластина накостная для фиксации переломов винтами, нерассасывающаяся, стерильная'
                        elif 'фиксатор' in protocol_text or 'пуговиц' in protocol_text:
                            implant_id = '846'
                            implant_title = 'Фиксатор связок'
                        elif 'серкляж' in protocol_text:
                            implant_id = '930'  # нить
                            implant_title = 'Нить хирургическая из поли(L-лактид-ко-капролактона)'
                        else:
                            implant_id = None
                            implant_title = None

                        if implant_id is not None and implant_title is not None:
                            current_patient_ecp.save_implant_type_link(
                                evn_usluga_oper_id=oper_id,
                                implant_id=implant_id,
                                implant_name=implant_title
                            )
                    print(f'Done! Operation to {item.fio} added')


def discharge_patient(connect: Session):
    """Выписывает пациентов"""
    authorization_l2(connect, login=login_l2, password=password_l2)
    patients_number = get_all_patients_in_ward('P3:P40')

    current_discharged_patients_l2 = [
        HistoryL2(
            connect=connect,
            number=int(history_number)
        ) for history_number in patients_number if history_number.isdigit()]  # генератор перечень пациентов в L2

    day_today = datetime.today().strftime('%d.%m.%Y')
    entry(connect, login=login, password=password)
    patients_in_ecp_request = get_all_patients_stac(connect, day_today)

    current_patients_ecp = (
        CurrentPatientECP(
            connect=connect,
            person_evn_id=patient.get('PersonEvn_id'),
            person_id=patient.get('Person_id'),
            medpersonal_id=patient.get('MedPersonal_id'),
            evn_section_id=patient.get('EvnSection_id'),
            evn_ps_id=patient.get('EvnPS_id'),
            server_id=patient.get('Server_id'),
            ksg=patient.get('EvnSection_KSG')
        ) for patient in patients_in_ecp_request if patient.get('LpuSection_id') == '380101000015688')

    ecp_fio_dict = {patient_ecp.person_fio: patient_ecp
                    for patient_ecp in current_patients_ecp}

    with open(path_to_mkb_code, 'r') as file:
        diagnosis_info = json.load(file)

    for patient in current_discharged_patients_l2:
        if patient.finally_examination:
            if patient.fio in list(ecp_fio_dict.keys()):
                treatment_doctor = patient.finally_examination.get('Лечащий врач')
                doctor_surname = treatment_doctor.split(' ')[0]
                with open(path_to_doctorsJson, 'r') as file:  # список словарей с данными врачей
                    doctors = json.load(file)
                med_personal_id = doctors.get(doctor_surname).get(
                    'MedPersonal_id')  # получаем персональное id по фамилии лечащего врача из data
                med_staff_fact_id = doctors.get(doctor_surname).get(
                    'MedStaffFact_id_stac')
                current_ecp_patient = ecp_fio_dict.get(patient.fio)
                current_ecp_patient.set_treating_doctor(
                    med_personal_id=med_personal_id,
                    med_staf_fact_id=med_staff_fact_id
                )
                print(f'У пациента {patient.fio} сменен лечащий врач на {doctor_surname}')

                diagnosis_id = ''
                for diagnosis in diagnosis_info:

                    if diagnosis.get('Diag_Code') in patient.finally_examination.get('Основной диагноз по МКБ'):
                        diagnosis_id = diagnosis.get('Diag_id')  # .get('Diag_id')

                ksg_koeff = current_ecp_patient.get_KSG_KOEF(
                    date_start=patient.first_examination.get('Дата поступления'),
                    date_end=patient.finally_examination.get('Дата выписки'),
                    diagnosis_id=diagnosis_id
                )

                current_ecp_patient.save_data(
                    date_start=patient.first_examination.get('Дата поступления'),
                    date_end=patient.finally_examination.get('Дата выписки'),
                    koiko_dni=patient.finally_examination.get('Проведено койко-дней'),
                    ksg_val=ksg_koeff.get('KSG'),
                    ksg_mes_tid=ksg_koeff.get('Mes_tid'),
                    ksg_mestarif_id=ksg_koeff.get('MesTariff_id'),
                    ksg_mes_old_usluga_complex_id=ksg_koeff.get('MesOldUslugaComplex_id'),
                    time_start=patient.first_examination.get('Время поступления'),
                    time_end=patient.finally_examination.get('Время выписки'),
                    ksg_coeff=ksg_koeff.get('KOEF'),
                    diag_id=diagnosis_id,
                    med_staff_fact_id=med_staff_fact_id,
                    med_personal_id=med_personal_id
                )

                template = current_ecp_patient.create_template(med_staff_fact_id=med_staff_fact_id)

                current_ecp_patient.update_evn_template(
                    template_id=template.get('EvnXml_id'),
                    chapter='Condition',
                    text=f'{patient.finally_examination.get("жалобы при поступлении")}'
                         f'\n{patient.finally_examination.get("анамнез заболевания")}'
                         f'\n{patient.finally_examination.get("осмотр(поступление)")}'
                )

                current_ecp_patient.update_evn_template(
                    template_id=template.get('EvnXml_id'),
                    chapter='recommendations',
                    text=f'{patient.finally_examination.get("Наблюдение специалистов на амбулаторном этапе (явка на осмотр специалистов не позднее 7 дней после выписки из стационара в поликлинику по месту жительства)")}\n'
                         f'{patient.finally_examination.get("Ограничение физических нагрузок", "")}\n'
                         f'{patient.finally_examination.get("Режим иммобилизации", "")}\n'
                         f'{patient.finally_examination.get("Рекомендации по рентгену", "")}\n'
                         f'{patient.finally_examination.get("Реабилитация", "")}\n'
                         f'{patient.finally_examination.get("Уход за послеоперационной раной", "")}'
                )
                print(f'Пациента {patient.fio} выписан')

        else:
            print(f'Проверь выписку {patient.fio}')


# session = Session()
# discharge_patient(session)
# session.close()
