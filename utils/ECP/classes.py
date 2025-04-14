class PatientECP:
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

