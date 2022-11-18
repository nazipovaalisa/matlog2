import numpy as np
import math
from prettytable import PrettyTable

def r0(ob, s):
    return math.sqrt((ob.x - s.x)**2 + (ob.y - s.y)**2)

def operation(init_data, dict_1, stor, dict_2, tc_list, x0_list, y0_list, i):
    #заполнение второй таблицы
    dict_2['r0'] = np.array([r0(ob, stor) for ob in init_data])
    dict_2['vtr0'] = dict_1['vt'] * dict_2['r0']
    dict_2['xvt/r0'] = dict_1['xvt'] / dict_2['r0']
    dict_2['yvt/r0'] = dict_1['yvt'] / dict_2['r0']
    dict_2['vt/r0'] = dict_1['vt'] / dict_2['r0']

    tc = sum(dict_2['vtr0'])#расчет total costs
    tc_list.append(tc)
    sum_xvtr = sum(dict_2['xvt/r0'])
    sum_yvtr = sum(dict_2['yvt/r0'])
    sum_vtr = sum(dict_2['vt/r0'])

    print(f'{i} приближение')
    table_2 = PrettyTable()
    for key, values in dict_2.items():
        table_2.add_column(key, values)
    table_2.add_row(['Сумма', '', '-', tc, sum_xvtr, sum_yvtr, sum_vtr])
    print(table_2)
    print(f'TC = {tc}')
    stor.x = sum_xvtr / sum_vtr #уточнение координат склада
    stor.y = sum_yvtr / sum_vtr
    print(f'x0 = {stor.x}\ny0 = {stor.y}')
    if i > 0:
        x0_list.append(stor.x)
        y0_list.append(stor.y)


