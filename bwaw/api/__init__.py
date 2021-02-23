"""Module for keeping all constants related to UM WAW API (https://api.um.warszawa.pl/api/)."""

from types import SimpleNamespace

TABLE = SimpleNamespace(
    BUSES='busestrams_get',
    TIMETABLES='dbtimetable_get',
    STOPS='dbstore_get'
)

RESOURCE_ID = SimpleNamespace(
    BUSES_ACTIVE='f2e5503e-927d-4ad3-9500-4ab9e55deb59',
    TIMETABLE_FOR_LINE='e923fa0e-d96c-43f9-ae6e-60518c9f3238',
    BUSES_ON_STOP='88cd555f-6f31-43ca-9de4-66c479ad5942',
    BUS_STOP_BY_NAME='b27f4c17-5c50-4a5b-89dd-236b282bc499',
    BUS_STOP_COORDINATE='ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'
)


PARAMETER = SimpleNamespace(
    API_KEY='apikey',
    BUS_STOP_ID='busstopId',
    BUS_STOP_NR='busstopNr',
    LINE_NR='line',
    BUS_STOP_NAME='name',
    RESOURCE_ID1='resource_id',
    RESOURCE_ID2='id',
    TYPE='type'
)


CONSTANTS = SimpleNamespace(
    API_URL='https://api.um.warszawa.pl/api/action/',
    ACTIVE_BUS_STATIC_TYPE=1
)
