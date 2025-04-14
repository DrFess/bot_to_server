import datetime
import json

import requests

from settings import proxies, login_l2, password_l2
from utils.ECP.add_operation import get_info_code_operation, save_all_oper_info, add_operation_member, \
    save_oper_anesthesia, create_empty_oper, update_oper
from utils.ECP.classes import PatientECP
from utils.ECP.single_digital_platform import entry, get_all_patients_stac, search_patient, get_evn_number, save_EVN, \
    save_implant_type_link, set_treating_doctor, mkb, get_KSG_KOEF, save_data, create_template, update_evn_template
from utils.L2.parse_l2 import authorization_l2, get_all_patients_in_ward, get_patient_fio_birthday_L2, \
    get_first_examination_number_L2, get_first_examination_data_L2, get_history_count, get_operation_data, \
    get_extracts_number, get_diaries_content, get_extracts_data


def working_with_stories():
    session = requests.Session()  # создание сессии подключения
    session.proxies.update(proxies)

    entry(session, login='daa87', password='Daa026')

    day_today = datetime.datetime.today().strftime('%d.%m.%Y')

    patients_in_ECP = []
    patients_in_ECP_full = []
    patients_in_ecp_request = get_all_patients_stac(session, day_today)

    for patient in patients_in_ecp_request:
        if patient.get('LpuSection_id') == '380101000015688':
            patient_ecp = PatientECP(
                connect=session,
                person_evn_id=patient.get('PersonEvn_id'),
                person_id=patient.get('Person_id'),
                medpersonal_id=patient.get('MedPersonal_id'),
                evn_section_id=patient.get('EvnSection_id'),
                evn_ps_id=patient.get('EvnPS_id'),
                server_id=patient.get('Server_id'),
                ksg=patient.get('EvnSection_KSG')
            )

            patients_in_ECP_full.append(patient_ecp)

            patients_in_ECP.append((patient_ecp.person_fio, patient_ecp.person_birthday))

    authorization_l2(session, login=login_l2, password=password_l2)
    patients_number = get_all_patients_in_ward('C3:C40')  # 'C3:C40'
    patients_number.extend(get_all_patients_in_ward('K3:K40'))
    patients_in_L2 = [get_patient_fio_birthday_L2(session, patient_l2) for patient_l2 in patients_number]

    extracts_patients_number = get_all_patients_in_ward('P3:P40')  # 'P3:P40'
    extracts_patients_in_L2 = [get_patient_fio_birthday_L2(session, patient_l2) for patient_l2 in
                               extracts_patients_number]

    for patient_1 in patients_in_L2:
        """Оформляет случай госпитализации в ЕЦП"""
        if patient_1.get('fio_age') not in patients_in_ECP:
            examination_number = get_first_examination_number_L2(patient_1.get('number'))
            first_examination_data = get_first_examination_data_L2(session, examination_number)

            fio_patient = patient_1.get('fio_age')[0].split(' ')
            name = fio_patient[1]
            surname = fio_patient[0]
            patronymic = fio_patient[2]

            search = search_patient(  # поиск пациента
                session,
                name=name,
                surname=surname,
                patronymic=patronymic,
                birthday=patient_1.get('fio_age')[1],
            )
            evn_number = get_evn_number(session)  # получаем номер случая лечения

            if search:
                if first_examination_data.get(
                        'Вид госпитализации') == 'экстренная':  # сохранение карты выбывшего == госпитализация/оформлен
                    save_EVN(
                        session,
                        patient_id=search[0].get('Person_id'),
                        patient_person_evn_id=search[0]['PersonEvn_id'],
                        patient_server_id=search[0]['Server_id'],
                        date_start=first_examination_data.get('Дата поступления').split('-'),
                        time_start=first_examination_data.get('Время поступления'),
                        numcard=evn_number.get('EvnPS_NumCard'),
                        type_hospitalization='1',
                        date_of_referral='',
                        number_of_referral='',
                        other_hosp='',
                        org_id='',
                        med_personal_id='380101000004549',
                        med_staff_fact_id='380101000010385'
                    )  # ошибка пересечения случаев госпитализации/обращения игнорируется
                    print(f'{patient_1} in ECP! Check')

                elif first_examination_data.get('Вид госпитализации') == 'плановая':
                    save_EVN(
                        session,
                        patient_id=search[0].get('Person_id'),
                        patient_person_evn_id=search[0]['PersonEvn_id'],
                        patient_server_id=search[0]['Server_id'],
                        date_start=first_examination_data.get('Дата поступления'),
                        time_start=first_examination_data.get('Время поступления'),
                        numcard=evn_number.get('EvnPS_NumCard'),
                        type_hospitalization='2',
                        date_of_referral=first_examination_data.get('Дата выдачи направления'),
                        number_of_referral=first_examination_data.get('Номер направления'),
                        other_hosp='2',
                        org_id=first_examination_data.get('Org_id'),
                        med_personal_id='380101000004549',
                        med_staff_fact_id='380101000010385'
                    )
                    print(f'{patient_1} in ECP! Check')
                else:
                    evn_card = 'Ошибка на этапе вида госпитализации'
                    print(evn_card)
            else:
                print(f'Patient not found {patient_1.get("fio_age")}')

    extracts_patients_in_ECP = []
    for patient_3 in extracts_patients_in_L2:
        """Формирует список выписанных пациентов в L2"""
        fio_extract = patient_3.get('fio_age')[0]
        birthday = patient_3.get('fio_age')[1]
        number_L2 = patient_3.get('number')
        for patient_4 in patients_in_ECP_full:
            if patient_4.person_fio == fio_extract and patient_4.person_birthday == birthday:
                extracts_patients_in_ECP.append(
                    {'fio': fio_extract, 'birthday': birthday, 'number_L2': number_L2, 'patient': patient_4}
                )

    with open('jsonS/doctors.json', 'r') as file:  # список словарей с данными врачей
        doctors = json.load(file)

    for extract_patient in extracts_patients_in_ECP:

        history_count = get_history_count(session, int(extract_patient.get('number_L2')))

        if history_count.get('operation') and not extract_patient.get('patient').ksg:
            """Добавляет услугу - операцию"""
            operation_data = get_operation_data(session, extract_patient.get('number_L2'))

            who_operate = operation_data.get('Оперировавший хирург').split(' ')[0]
            who_operate_med_personal_id = doctors.get(who_operate).get('MedPersonal_id')
            who_operate_med_staf_fact_id = doctors.get(who_operate).get('MedStaffFact_id')

            current_oper_code = get_info_code_operation(
                session,
                code=operation_data.get('Код операции').split(' ')[0].rstrip('.').lstrip('A').lstrip('А'),
                oper_date=operation_data.get('Дата проведения'),
                person_id=extract_patient.get('patient').person_id,
                evnsection_id=extract_patient.get('patient').evn_section_id
            )

            first_oper_save = save_all_oper_info(
                session,
                medPersonal_id=who_operate_med_personal_id,
                person_id=extract_patient.get('patient').person_id,
                personEvn_id=extract_patient.get('patient').person_evn_id,
                server_id=extract_patient.get('patient').server_id,
                start_date=operation_data.get('Дата проведения'),
                start_time=operation_data.get('Время начала'),
                end_date=operation_data.get('Дата проведения'),
                end_time=operation_data.get('Время окончания'),
                medStaffFact_id=who_operate_med_staf_fact_id,
                evn_id='0',
                evnUslugaOper_id='0',
                evnPS_id=extract_patient.get('patient').evn_ps_id,
                evnSection_id=extract_patient.get('patient').evn_section_id,
                oper_code=current_oper_code[0].get('UslugaComplex_id')
            )
            oper_id = first_oper_save.get('EvnUslugaOper_id')  # возвращает EvnUslugaOper_id == EvnUslugaOperBrig_pid

            add_operation_member(
                session,
                medPersonal_id=who_operate_med_personal_id,
                evn_usluga_oper_id=oper_id,
                medStaffFact_id=who_operate_med_staf_fact_id,
                surgType_id='1'
            )
            anesthesiolog = operation_data.get('Анестезиолог')
            with open('jsonS/empoyees.json', 'r') as file:
                doctors_list = json.load(file)
            for doctor in doctors_list:
                if anesthesiolog == doctor.get('MedPersonal_Fin') and doctor.get('WorkData_MedStaff_endDate') is None:
                    anesthesiolog_med_personal_id = doctor.get('MedPersonal_id')
                    anesthesiolog_staf_fact_id = doctor.get('MedStaffFact_id')
                    add_operation_member(
                        session,
                        medPersonal_id=anesthesiolog_med_personal_id,
                        evn_usluga_oper_id=oper_id,
                        medStaffFact_id=anesthesiolog_staf_fact_id,
                        surgType_id='4'
                    )
                    break

            if operation_data.get('Вид анестезии') == 'ЭТН':
                anesthesia_class_id = '4'
            elif operation_data.get('Вид анестезии') == 'АМН':
                anesthesia_class_id = '5'
            else:
                anesthesia_class_id = '21'

            save_oper_anesthesia(
                session,
                evn_usluga_oper_anest_id=oper_id,
                anesthesiaClass_id=anesthesia_class_id
            )

            operation_template = create_empty_oper(
                session,
                evn_id=oper_id,
                medStaffFact_id=who_operate_med_staf_fact_id
            )

            update_oper(
                session,
                evn_xml_id=operation_template.get('EvnXml_id'),
                text=operation_data.get('Ход операции')
            )

            """Блок добавления импланта"""
            implants_in_oper = operation_data.get('Ход операции')
            title_operation = operation_data.get('Название операции')
            if 'удаление' not in title_operation.lower():
                if 'спиц' in implants_in_oper or 'стержень' in implants_in_oper or 'TEN' in implants_in_oper:
                    implant_id = '856'  # стержень
                    implant_title = 'Стержень костный ортопедический, нерассасывающийся'
                elif 'винт' in implants_in_oper:
                    implant_id = '857'  # винт
                    implant_title = 'Винт костный ортопедический, нерассасывающийся, стерильный'
                elif 'пластин' in implants_in_oper:
                    implant_id = '859'  # пластина
                    implant_title = 'Пластина накостная для фиксации переломов винтами, нерассасывающаяся, стерильная'
                elif 'фиксатор' in implants_in_oper or 'пуговиц' in implants_in_oper:
                    implant_id = '846'
                    implant_title = 'Фиксатор связок'
                elif 'серкляж' in implants_in_oper:
                    implant_id = '930'  # нить
                    implant_title = 'Нить хирургическая из поли(L-лактид-ко-капролактона)'
                else:
                    implant_id = None
                    implant_title = None
                if implant_id is not None and implant_title is not None:
                    save_implant_type_link(
                        session,
                        evn_usluga_oper_id=oper_id,
                        implant_id=implant_id,
                        implant_name=implant_title
                    )
            print(f'Done! Operation to {extract_patient.get("fio")} added')

        if history_count.get('extracts') == 1:
            extracts_number = get_extracts_number(session, int(extract_patient.get('number_L2')))
            pk_extract = extracts_number.get('data')[0].get('pk')
            extract_content = get_diaries_content(session, pk_extract)
            treatment_doctor = extract_content.get('researches')[0].get('whoConfirmed')
            doctor_surname = str(treatment_doctor).split(', ')[0].split(' ')[0]
            med_personal_id = doctors.get(doctor_surname).get(
                'MedPersonal_id')  # получаем персональное id по фамилии лечащего врача из data
            med_staff_fact_id = doctors.get(doctor_surname).get(
                'MedStaffFact_id_stac')  # получаем рабочее id по фамилии лечащего врача из data

            if extract_patient.get('patient').medpersonal_id != med_personal_id:
                """Меняет лечащего врача по выписке"""
                set_treating_doctor(
                    connect=session,
                    evn_section_id=extract_patient.get('patient').evn_section_id,
                    person_id=extract_patient.get('patient').person_id,
                    person_evn_id=extract_patient.get('patient').person_evn_id,
                    server_id=extract_patient.get('patient').server_id,
                    med_personal_id=med_personal_id,
                    med_staf_fact_id=med_staff_fact_id
                )
                print(f'У пациента {extract_patient.get("fio")} сменен лечащий врач на {doctor_surname}')

            extract_content = get_extracts_data(session, pk_extract)

            diagnosis_id = mkb(session, letter=extract_content.get('Основной диагноз по МКБ'))[0].get('Diag_id')

            ksg_and_koef = get_KSG_KOEF(
                # расчёт КСГ по сроку лечения и коду МКБ -> нужно добавить метод для расчёта по операции
                session,
                date_start=extract_content.get('Дата поступления'),
                date_end=extract_content.get('Дата выписки'),
                patient_id=extract_patient.get('patient').person_id,
                diagnosis_id=diagnosis_id
            )

            save_data(  # функция переводит пациента в выписанные
                session,
                date_start=extract_content.get('Дата поступления'),
                date_end=extract_content.get('Дата выписки'),
                ksg_val=ksg_and_koef.get('KSG'),
                ksg_mes_tid=ksg_and_koef.get('Mes_tid'),
                ksg_mestarif_id=ksg_and_koef.get('MesTariff_id'),
                ksg_mes_old_usluga_complex_id=ksg_and_koef.get('MesOldUslugaComplex_id'),
                ksg_coeff=ksg_and_koef.get('KOEF'),
                patient_id=extract_patient.get('patient').person_id,
                patient_person_evn_id=extract_patient.get('patient').person_evn_id,
                patient_server_id=extract_patient.get('patient').server_id,
                time_start=extract_content.get('Время поступления'),
                time_end=extract_content.get('Время выписки'),
                evn_section_id=extract_patient.get('patient').evn_section_id,
                evn_section_pid=extract_patient.get('patient').evn_ps_id,
                diag_id=diagnosis_id,
                med_personal_id=med_personal_id,
                med_staff_fact_id=med_staff_fact_id
            )

            template = create_template(session, extract_patient.get('patient').evn_section_id,
                                       med_staff_fact_id=med_staff_fact_id)  # создаёт пустой шаблон выписного эпикриза по id шаблона

            update_evn_template(  # обновляет рекомендациями данные шаблона выписного эпикриза
                session,
                template_id=template.get('EvnXml_id'),
                chapter='Condition',
                text=f'{extract_content.get("жалобы при поступлении")}'
                     f'\n{extract_content.get("анамнез заболевания")}'
                     f'\n{extract_content.get("Соматический статус при поступлении")}\n'
            )

            update_evn_template(  # обновляет рекомендациями данные шаблона выписного эпикриза
                session,
                template_id=template.get('EvnXml_id'),
                chapter='recommendations',
                text=f'{extract_content.get("Наблюдение специалистов на амбулаторном этапе (явка на осмотр специалистов не позднее 7 дней после выписки из стационара в поликлинику по месту жительства)")}'
                     f'\n{extract_content.get("Ограничение физических нагрузок")}\n{extract_content.get("Уход за послеоперационной раной")}\n'
            )
            print(f'{extract_patient.get("fio")} выписан')
    session.close()
