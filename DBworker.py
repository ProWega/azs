import sqlite3
import datetime
import time
import pandas as pd
class DBparser:
    def __init__(self):
        self.oil_types_names = ['АИ-95']
        connection = sqlite3.connect('azs.db')
        cursor = connection.cursor()

        cursor.execute('''SELECT * FROM type_oil''')
        oil_types = cursor.fetchall()

        self.oil_types_id = [el[0] for el in oil_types]
        self.oil_types_names = [el[1] for el in oil_types]

        self.oil_type_id_from_name = dict(zip(self.oil_types_names, self.oil_types_id))
        self.name_oil_from_oil_type_id = dict(zip(self.oil_types_id, self.oil_types_names))

        cursor.execute('''SELECT * FROM oil''')
        oil = cursor.fetchall()

        oil_ids = [el[0] for el in oil]
        oil_names = [el[1] for el in oil]

        self.oil_id_from_oil_name = dict(zip(oil_names, oil_ids))
        self.oil_name_from_oil_id = dict(zip(oil_ids,oil_names))

        cursor.execute('''SELECT * FROM station''')
        station = cursor.fetchall()

        id_stations = [el[0] for el in station]
        links_station = [el[1] for el in station]

        self.station_links_from_id = dict(zip(id_stations,links_station))
        self.station_id_from_link = dict(zip(links_station, id_stations))

        cursor.execute('''SELECT * FROM station_company''')
        station_company = cursor.fetchall()
        id_stations = [el[0] for el in station_company]
        id_company = [el[1] for el in station_company]

        cursor.execute('''SELECT * FROM company''')
        company = cursor.fetchall()
        id_company_company = [el[0] for el in company]
        name_company = [el[1] for el in company]
        self.id_company_to_name_company = dict(zip(id_company_company, name_company))
        self.name_company_to_id_company = dict(zip(name_company, id_company_company))

        self.id_company_from_id_station = dict(zip(id_stations, id_company))


        connection.commit()
        connection.close()
    def GetSingleDayDf(self, date, name_oil_type):
        id_oil_type = self.oil_type_id_from_name[name_oil_type]

        connection = sqlite3.connect('azs.db')
        cursor = connection.cursor()

        cursor.execute(f''' SELECT id_oil FROM oil_id_type_oil_id WHERE type_oil_id={id_oil_type}''')
        id_oil_to_df = [el[0] for el in cursor.fetchall()]
        name_oil_to_df = [self.oil_name_from_oil_id[el] for el in id_oil_to_df]
        print(f"Oil id to df: {id_oil_to_df}")


        cursor.execute(f'''SELECT * FROM price WHERE date > {time.mktime(date.timetuple())} and date < {time.mktime(date.timetuple())+24*60*60}''')
        price_table = cursor.fetchall()
        station_links = [self.station_links_from_id[el[0]] for el in price_table]
        oil_names = [self.oil_name_from_oil_id[el[1]] for el in price_table]
        dates = [datetime.datetime.fromtimestamp(el[2]).strftime('%d-%m-%Y') for el in price_table]
        id_company_of_station = [self.id_company_from_id_station[el[0]] for el in price_table]
        name_station = [self.id_company_to_name_company[el] for el in id_company_of_station]
        price_values = [el[3] for el in price_table]

        connection.commit()
        connection.close()
        df = pd.DataFrame(
            data={"Название": name_station,
                  "Ссылка": station_links,
                  "Тип топлива": oil_names,
                  "Цена": price_values}
        )

        return df[df['Тип топлива'].isin(name_oil_to_df)]
