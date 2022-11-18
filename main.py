import pandas as pd
import numpy as np
from prettytable import PrettyTable
from classes import obj, storage
from operations import operation
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('TkAgg')

def main():

    df = pd.read_excel("source.xlsx")
    df.dropna(how='all')
    x = df['x'].values
    y = df['y'].values
    init_data = [] #список объектов
    for i in range(df.shape[0]):
        init_data.append(obj(df['N п/п'].iloc[i], df['Объект'].iloc[i],
                             df['Объем грузопотока, т/год'].iloc[i], df['Тариф руб/ткб'].iloc[i],
                             df['x'].iloc[i], df['y'].iloc[i]))

    #таблица1
    dict_1 = {
        'N п/п': df['N п/п'].values,
        'Объект': df['Объект'].values,
        'xvt': np.array([ob.x * ob.v * ob.t for ob in init_data]),
        'yvt': np.array([ob.y * ob.v * ob.t for ob in init_data]),
        'vt': np.array([ob.v * ob.t for ob in init_data])
    }

    sum_xvt = sum(dict_1['xvt'])
    sum_yvt = sum(dict_1['yvt'])
    sum_vt = sum(dict_1['vt'])

    table_1 = PrettyTable()
    for key, values in dict_1.items():
        table_1.add_column(key, values)
    table_1.add_row(['Сумма', '', sum_xvt, sum_yvt, sum_vt])
    print(table_1)

    x0 = sum_xvt / sum_vt
    y0 = sum_yvt / sum_vt
    stor = storage(x0, y0) #начальные координаты склада
    print(f'x0 = {x0}\ny0 = {y0}')

    fig, ax1 = plt.subplots()
    ax1.scatter(x, y, c='red', label='Объекты')
    ax1.scatter(stor.x, stor.y, c='black', label='Склад')
    for ob in init_data:
        ax1.plot([ob.x, stor.x], [ob.y, stor.y])
        ax1.text(ob.x+1, ob.y, ob.name)
    ax1.grid()
    ax1.legend()
    ax1.set_title("Рисунок 1. Объекты и первоначальные координаты складского комплекса")


    #таблица2
    dict_2 = {
        'N п/п': df['N п/п'].values,
        'Объект': df['Объект'].values,
        'r0': np.array([]),
        'vtr0': np.array([]),
        'xvt/r0': np.array([]),
        'yvt/r0': np.array([]),
        'vt/r0': np.array([])
    }

    tc_dif = [0] #разница tc между итерациями
    i = 0 #итерации
    iter = [i] #список итераций
    tc_list = [] #список tc
    x0_list = [stor.x] #список координаты склада x0
    y0_list = [stor.y] #список координаты склада y0

    operation(init_data, dict_1, stor, dict_2, tc_list, x0_list, y0_list, i)

    eps = 0.01
    flag = False
    while not flag:
        i += 1
        operation(init_data, dict_1, stor, dict_2, tc_list, x0_list, y0_list, i)
        dif = tc_list[i-1] - tc_list[i]
        tc_dif.append(dif)
        iter.append(i)
        flag = dif < eps

    table_3 = PrettyTable()
    table_3.add_column('№ итерации', iter)
    table_3.add_column('x0', x0_list)
    table_3.add_column('y0', y0_list)
    table_3.add_column('TC', tc_list)
    table_3.add_column('TC(i-1) - TC(i)', tc_dif)
    print(table_3)

    fig2, ax2 = plt.subplots()
    ax2.scatter(x0_list, y0_list, c='green')
    ax2.scatter(stor.x, stor.y, c='red')
    ax2.plot(x0_list, y0_list, c='lightblue')
    ax2.grid()
    ax2.set_title("Рисунок 2. Изменение координат складcкого комплекса")

    fig3, ax3 = plt.subplots()
    ax3.scatter(x, y, c='red', label='Объекты')
    ax3.scatter(stor.x, stor.y, c='black', label='Склад')
    for ob in init_data:
        ax3.plot([ob.x, stor.x], [ob.y, stor.y])
        ax3.text(ob.x+1, ob.y, ob.name)
    ax3.grid()
    ax3.legend()
    ax3.set_title("Рисунок 3. Объекты и оптимальные координаты складского комплекса")
    plt.show()


if __name__ == '__main__':
    main()