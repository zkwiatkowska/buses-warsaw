"""Mock data for bwaw.insights tests."""
import pandas as pd

ACTIVE_BUSES = pd.DataFrame([
    ['213', 21.0921481, '1001', '2021-02-09 15:45:27', 52.224536, '2'],
    ['213', 21.0911025, '1001', '2021-02-09 15:46:22', 52.2223788, '2'],
    ['138', 21.0921481, '1001', '2021-02-09 15:45:27', 52.224536, '05'],
    ['138', 21.0911025, '1001', '2021-02-09 15:46:22', 52.2223788, '05']
], columns=['Lines', 'Lon', 'VehicleNumber', 'Time', 'Lat', 'Brigade'])
ACTIVE_BUSES['Time'] = pd.to_datetime(ACTIVE_BUSES['Time'])

COORDINATES = pd.DataFrame([
    ['1001', '01', 52.224536, 21.0921481, 'al.Zieleniecka', '2020-10-12 00:00:00.0']
], columns=['ID', 'Number', 'Latitude', 'Longitude', 'Destination', 'Validity'])


TIMETABLE = [{'Brigade': '2', 'Destination': 'al.Zieleniecka', 'Time': '15:46:00'}]

SPEED_INCIDENT = pd.DataFrame([
    [16.378041, 52.223457, 21.091625, '2021-02-09 15:45:54.500']
], columns=['Speed', 'Lat', 'Lon', 'Time'])
SPEED_INCIDENT['Time'] = pd.to_datetime(SPEED_INCIDENT['Time'])


SPEED_INCIDENTS = pd.DataFrame([
    ['213', 16.378041, 52.223457, 21.091625, '2021-02-09 15:45:54.500'],
    ['138', 16.378041, 52.223457, 21.091625, '2021-02-09 15:45:54.500']
], columns=['Lines', 'Speed', 'Lat', 'Lon', 'Time'])
SPEED_INCIDENTS['Time'] = pd.to_datetime(SPEED_INCIDENTS['Time'])
