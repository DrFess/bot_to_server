import json
from datetime import datetime
from pprint import pprint

from requests import Session

from settings import login_l2, password_l2, login, password, path_to_hospitalsJson
from utils.ECP.classes_ECP import CurrentPatientECP, HistoryEcp
from utils.ECP.single_digital_platform import get_all_patients_stac, entry
from utils.L2.classes_L2 import HistoryL2
from utils.L2.diaries import authorization_l2
from utils.L2.parse_l2 import get_all_patients_in_ward


def add_patients_in_ecp(connect: Session):
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
        ) for patient in patients_in_ecp_request if patient.get('LpuSection_id') == '380101000015688')  # генератор перечень пациентов в ЕЦП

    fio_list = [patient_ecp.person_fio for patient_ecp in current_patients_ecp]

    for item_l2 in current_patients_l2:
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

    return current_patients_l2, current_patients_ecp
