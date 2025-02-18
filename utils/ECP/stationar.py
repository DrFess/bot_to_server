import json
from datetime import datetime

import requests

from settings import proxies, LIST_ID, path_to_doctorsJson

from utils.L2.parse_l2 import get_patients_from_table, extract_patient_data_from_L2
from utils.ECP.add_operation import get_info_code_operation, save_all_oper_info, add_operation_member, save_oper_anesthesia, \
    create_empty_oper, update_oper
from utils.ECP.single_digital_platform import (
    entry,
    search_patient,
    get_KSG_KOEF,
    get_evn_number,
    save_EVN,
    save_data,
    mkb,
    create_template,
    update_treatment_evn_template,
    update_recommendation_evn_template,
    update_research_evn_template,
    save_implant_type_link
)


def export_stories_function():
    with open(path_to_doctorsJson, 'r') as file:  # список словарей с данными врачей
        doctors = json.load(file)

    session = requests.Session()  # создание сессии подключения
    session.proxies.update(proxies)

    for item in get_patients_from_table(LIST_ID, 'Y3:Y42'):  # функция получает список номеров выписанных историй (P3:P42)

        try:
            data = extract_patient_data_from_L2(int(item))  # данные из истории в виде словаря
            doctor_surname = data.get('Лечащий врач').split(' ')[0]

            login = doctors.get(doctor_surname).get('login')  # получаем логин по фамилии лечащего врача из data
            password = doctors.get(doctor_surname).get('password')  # получаем пароль по фамилии лечащего врача из data
            med_personal_id = doctors.get(doctor_surname).get('MedPersonal_id')  # получаем персональное id по фамилии лечащего врача из data
            med_staff_fact_id = doctors.get(doctor_surname).get('MedStaffFact_id_stac')  # получаем рабочее id по фамилии лечащего врача из data

            entry(session, login=login, password=password)  # авторизация в ЕЦП с данными лечащего врача
            search = search_patient(  # поиск пациента
                session,
                name=data.get('Имя'),
                surname=data.get('Фамилия'),
                patronymic=data.get('Отчество'),
                birthday=data.get('Дата рождения'),
            )
            patient = search[0].get('Person_id')  # person_id пациента после поиска его в ЕЦП
            diagnosis_id = mkb(session, letter=data.get('Основной диагноз по МКБ'))[0]['Diag_id']  # id диагноза по коду МКБ
            ksg_and_koef = get_KSG_KOEF(  # расчёт КСГ по сроку лечения и коду МКБ -> нужно добавить метод для расчёта по операции
                session,
                date_start=data.get('Дата поступления'),
                date_end=data.get('Дата выписки'),
                patient_id=patient,
                diagnosis_id=diagnosis_id
            )
            evn_number = get_evn_number(session)  # получаем номер случая лечения
            try:
                if data.get('Вид госпитализации') == 'экстренная':  # сохранение карты выбывшего == госпитализация/оформлен
                    evn_card = save_EVN(
                        session,
                        patient_id=patient,
                        patient_person_evn_id=search[0]['PersonEvn_id'],
                        patient_server_id=search[0]['Server_id'],
                        date_start=data.get('Дата поступления'),
                        time_start=data.get('Время поступления'),
                        numcard=evn_number.get('EvnPS_NumCard'),
                        type_hospitalization='1',
                        date_of_referral='',
                        number_of_referral='',
                        other_hosp='',
                        org_id='',
                        med_personal_id=med_personal_id,
                        med_staff_fact_id=med_staff_fact_id
                    )  # ошибка пересечения случаев госпитализации/обращения игнорируется
                elif data.get('Вид госпитализации') == 'плановая':
                    evn_card = save_EVN(
                        session,
                        patient_id=patient,
                        patient_person_evn_id=search[0]['PersonEvn_id'],
                        patient_server_id=search[0]['Server_id'],
                        date_start=data.get('Дата поступления'),
                        time_start=data.get('Время поступления'),
                        numcard=evn_number.get('EvnPS_NumCard'),
                        type_hospitalization='2',
                        date_of_referral=data.get('Дата выдачи направления'),
                        number_of_referral=data.get('Номер направления'),
                        other_hosp='2',
                        org_id=data.get('Org_id'),
                        med_personal_id=med_personal_id,
                        med_staff_fact_id=med_staff_fact_id
                    )
                else:
                    evn_card = 'Ошибка на этапе вида госпитализации'
                    print(evn_card)

                """Здесь блок функций по протоколу операции"""

                if len(data.get('Протоколы операций')) > 0:
                    who_operate = data.get('Протоколы операций')[0].get('Оперировавший хирург').split(' ')[0]
                    who_operate_med_personal_id = doctors.get(who_operate).get('MedPersonal_id')
                    who_operate_med_staf_fact_id = doctors.get(who_operate).get('MedStaffFact_id')

                    current_oper_code = get_info_code_operation(
                        session,
                        code=data.get('Протоколы операций')[0].get('Код операции').split(' ')[0].rstrip('.').lstrip(
                            'A').lstrip('А'),
                        oper_date=data.get('Протоколы операций')[0].get('Дата проведения'),
                        person_id=patient,
                        evnsection_id=evn_card.get('EvnSection_id')
                    )

                    first_oper_save = save_all_oper_info(
                        session,
                        medPersonal_id=med_personal_id,
                        person_id=patient,
                        personEvn_id=search[0].get('PersonEvn_id'),
                        server_id=search[0].get('Server_id'),
                        start_date=data.get('Протоколы операций')[0].get('Дата проведения'),
                        start_time=data.get('Протоколы операций')[0].get('Время начала'),
                        end_date=data.get('Протоколы операций')[0].get('Дата проведения'),
                        end_time=data.get('Протоколы операций')[0].get('Время окончания'),
                        medStaffFact_id=med_staff_fact_id,
                        evn_id='0',
                        evnUslugaOper_id='0',
                        evnPS_id=evn_card.get('EvnPS_id'),
                        evnSection_id=evn_card.get('EvnSection_id'),
                        oper_code=current_oper_code[0].get('UslugaComplex_id')
                    )
                    oper_id = first_oper_save.get(
                        'EvnUslugaOper_id')  # возвращает EvnUslugaOper_id == EvnUslugaOperBrig_pid

                    add_operation_member(
                        session,
                        medPersonal_id=who_operate_med_personal_id,
                        evn_usluga_oper_id=oper_id,
                        medStaffFact_id=who_operate_med_staf_fact_id,
                        surgType_id='1'
                    )
                    anesthesiolog = data.get('Протоколы операций')[0].get('Анестезиолог')
                    with open('utils/jsonS/empoyees.json', 'r') as file:
                        doctors_list = json.load(file)
                    for doctor in doctors_list:
                        if anesthesiolog == doctor.get('MedPersonal_Fin') and doctor.get(
                                'WorkData_MedStaff_endDate') is None:
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

                    if data.get('Протоколы операций')[0].get('Вид анестезии') == 'ЭТН':
                        anesthesia_class_id = '4'
                    elif data.get('Протоколы операций')[0].get('Вид анестезии') == 'АМН':
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
                        medStaffFact_id=med_staff_fact_id
                    )

                    update_oper(
                        session,
                        evn_xml_id=operation_template.get('EvnXml_id'),
                        text=data.get('Протоколы операций')[0].get('Ход операции')
                    )

                    """Блок добавления импланта"""
                    count_implants_in_oper = int(data.get('Протоколы операций')[0].get('Количество имплантов'))
                    implants_in_oper = data.get('Протоколы операций')[0].get('Импланты')
                    for implant in implants_in_oper:
                        if 'спица' in implant or 'nail' in implant or 'стержень' in implant:
                            implant_id = '856'  # стержень
                            implant_title = 'Стержень костный ортопедический, нерассасывающийся'
                        elif 'винт' in implant:
                            implant_id = '857'  # винт
                            implant_title = 'Винт костный ортопедический, нерассасывающийся, стерильный'
                        else:
                            implant_id = '930'  # нить
                            implant_title = 'Нить хирургическая из поли(L-лактид-ко-капролактона)'
                        save_implant_type_link(
                            session,
                            evn_usluga_oper_id=oper_id,
                            implant_id=implant_id,
                            implant_name=implant_title
                        )

                save_data(  # функция переводит пациента в выписанные
                    session,
                    date_start=data.get('Дата поступления'),
                    date_end=data.get('Дата выписки'),
                    ksg_val=ksg_and_koef['KSG'],
                    ksg_mes_tid=ksg_and_koef['Mes_tid'],
                    ksg_mestarif_id=ksg_and_koef['MesTariff_id'],
                    ksg_mes_old_usluga_complex_id=ksg_and_koef['MesOldUslugaComplex_id'],
                    ksg_coeff=ksg_and_koef['KOEF'],
                    patient_id=search[0]['Person_id'],
                    patient_person_evn_id=search[0]['PersonEvn_id'],
                    patient_server_id=search[0]['Server_id'],
                    time_start=data.get('Время поступления'),
                    time_end=data.get('Время выписки'),
                    evn_section_id=evn_card['EvnSection_id'],
                    evn_section_pid=evn_card['EvnPS_id'],
                    diag_id=diagnosis_id,
                    med_personal_id=med_personal_id,
                    med_staff_fact_id=med_staff_fact_id
                )

                template = create_template(session, evn_card['EvnSection_id'], med_staff_fact_id=med_staff_fact_id)  # создаёт пустой шаблон выписного эпикриза по id шаблона

                update_research_evn_template(  # обновляет исследованиями данные шаблона выписного эпикриза
                    session,
                    template_id=template['EvnXml_id'],
                    text=data.get('Анализы')
                )

                update_treatment_evn_template(  # обновляет лечением данные шаблона выписного эпикриза
                    session,
                    template_id=template['EvnXml_id'],
                    text=f'{data.get("Консервативное")}\n{data.get("Оперативные вмешательства (операции), включая сведения об анестезиологическом пособии")}'
                )

                update_recommendation_evn_template(  # обновляет рекомендациями данные шаблона выписного эпикриза
                    session,
                    template_id=template['EvnXml_id'],
                    text=f'{data.get("Наблюдение специалистов на амбулаторном этапе (явка на осмотр специалистов не позднее 7 дней после выписки из стационара в поликлинику по месту жительства)")}'
                         f'\n{data.get("Ограничение физических нагрузок")}\n{data.get("Уход за послеоперационной раной")}\n'
                )
                print(f'{data.get("Фамилия")} в ЕЦП загружен')
                with open('uploaded_stories.txt', 'a') as file:
                    file.write(f'{datetime.now()}: {data.get("Фамилия")} в ЕЦП загружен\n')
            except Exception as error:
                print(f'{error} {data.get("Фамилия")}')
                with open('errors.txt', 'a') as file:
                    file.write(f'{datetime.now()}: {error} {data.get("Фамилия")}\n')
        except Exception as err:
            print(f'Ошибка: {err}')
            with open('errors.txt', 'a') as file:
                file.write(f'{datetime.now()}: {err}\n')

    session.close()
