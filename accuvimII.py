import datetime
import json

from pyModbusTCP import utils
from pyModbusTCP.client import ModbusClient


class AcuvimIITCPMODBUS:
    def __init__(self, server_host, port, unit_id):
        self.c = ModbusClient()
        self.c.host(server_host)
        self.c.port(port)
        self.c.unit_id(unit_id)
        self.map = self.__import_map()

    def __import_map(self):
        with open('map.json') as json_file:
            return json.load(json_file)

    def __read_16_bit(self, address):
        if not self.c.is_open():
            self.c.open()
        return self.c.read_holding_registers(address, 1)[0]

    def __read_32_bit(self, address, number=1):
        if not self.c.is_open():
            self.c.open()
        reg_l = self.c.read_holding_registers(address, number * 2)
        if reg_l:
            return [utils.decode_ieee(f) for f in utils.word_list_to_long(reg_l)][0]
        else:
            return None

    def __what_is_the_access_property(self, dict):
        if dict['Access Property'] == 'R':
            return 0
        if dict['Access Property'] == 'W':
            return 2
        else:
            return 1

    def __get_registry(self, dict):
        if dict['Data Type'] == 'Word':
            return (self.__read_16_bit(dict["Address(D)"]))
        elif dict['Data Type'] == 'Float':
            return (self.__read_32_bit(dict["Address(D)"]))
        elif dict['Data Type'] == 'Dword':
            return (self.__read_32_bit(dict["Address(D)"]))
        elif dict['Data Type'] == 'int':
            return (self.__read_16_bit(dict["Address(D)"]))
        elif dict['Data Type'] == 'Bit':
            return (self.__read_16_bit(dict["Address(D)"]))

    def get_clock(self):
        if not self.c.is_open():
            self.c.open()
        read_datetime = self.c.read_holding_registers(4159, 7)
        return datetime.datetime(read_datetime[1], read_datetime[2], read_datetime[3], read_datetime[4],
                                 read_datetime[5], read_datetime[6])

    def read_value(self, parameter=None, address=None):
        if parameter is not None:
            temp_dict = list(filter(lambda d: d['Parameter'] == parameter, self.map))
            if not len(temp_dict) == 0 and self.__what_is_the_access_property(temp_dict[0]) <= 1:
                return (self.__get_registry(temp_dict[0]))

        elif address is not None:
            temp_dict = list(filter(lambda d: d['Address(D)'] == address, self.map))
            if not len(temp_dict) == 0 and self.__what_is_the_access_property(temp_dict) <= 1:
                return (self.__get_registry(temp_dict[0]))

        else:
            return None
