import streamlit as st
from deap import algorithms, base, creator, tools
import random
import pandas as pd
import numpy as np


st.set_page_config(page_title="Распределение заказов каллиграфов", 
                   page_icon="🧊",
                    layout="wide",
                    initial_sidebar_state="expanded",
                    )

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


calligraphers = [{'name': '', 'productivity': 0, 'work_hours': 0}]
calligraphers_sample = [{'name': 'Новикова Наталья Геннадьевна Каллиграф', 'productivity': 3000, 'work_hours': 40},
{'name': 'Мария Нелюбина ( Крахмалева Ольга)', 'productivity': 3960, 'work_hours': 35},
{'name': 'Хусиянова Динара', 'productivity': 3000, 'work_hours': 0},
{'name': 'Карабанова Полина Анатольевна', 'productivity': 1992, 'work_hours': 20},
{'name': 'Людмила Морозова', 'productivity': 3996, 'work_hours': 52},
{'name': 'Стрелова Елена Каллиграф', 'productivity': 3996, 'work_hours': 30},
{'name': 'Нам Роза Борисовна', 'productivity': 3000, 'work_hours': 40},
{'name': 'Нагай Светлана Витальевна', 'productivity': 12000, 'work_hours': 55},
{'name': 'Руденко Лия Константиновна', 'productivity': 4800, 'work_hours': 0},
{'name': 'Кузнецова Анастасия Дмитриевна', 'productivity': 3000, 'work_hours': 15},
{'name': 'Югай Татьяна Александровна', 'productivity': 3996, 'work_hours': 0},
{'name': 'Кузавкова Ольга Михайловна', 'productivity': 3000, 'work_hours': 35},
{'name': 'Кузнецова Дарья Дмитриевна', 'productivity': 3996, 'work_hours': 40},
{'name': 'Мещерякова Ольга Ивановна', 'productivity': 6000, 'work_hours': 54},
{'name': 'Плеханова Людмила Ивановна', 'productivity': 3000, 'work_hours': 35},
{'name': 'Баранова Наталья Владимировна', 'productivity': 0, 'work_hours': 0},
{'name': 'Татьяна Тюхина', 'productivity': 6000, 'work_hours': 20},
{'name': 'Татьяна Балабанова', 'productivity': 1800, 'work_hours': 20},
{'name': 'Ольга Сомина', 'productivity': 1800, 'work_hours': 40},
{'name': 'Елена Суворова', 'productivity': 3000, 'work_hours': 30},
{'name': 'Ольга Давидян', 'productivity': 4500, 'work_hours': 55},
{'name': 'Света Панина', 'productivity': 3000, 'work_hours': 30},
{'name': 'Баранова Оксана Викторовна', 'productivity': 3000, 'work_hours': 30},
{'name': 'Югай Жанна Сергеевна', 'productivity': 0, 'work_hours': 0},
{'name': 'Луц Анна Евгеньевна', 'productivity': 3000, 'work_hours': 35},
{'name': 'Александрова Альбина Владимировна', 'productivity': 756, 'work_hours': 35},
{'name': 'Мещерякова Олеся Андреевна', 'productivity': 3000, 'work_hours': 15},
{'name': 'Тощенко Анна Александровна', 'productivity': 3600, 'work_hours': 42},
{'name': 'Лисичкина Виктория Геннадьевна', 'productivity': 2400, 'work_hours': 24},
{'name': 'Полева Иринка', 'productivity': 3600, 'work_hours': 21},
{'name': 'Лим Вера Владимировна', 'productivity': 1440, 'work_hours': 10},
{'name': 'Ипатова Юлия Витальевна', 'productivity': 2400, 'work_hours': 15},
{'name': 'Поляничева Светлана Александровна', 'productivity': 2400, 'work_hours': 15},
{'name': 'Демьянова Наталья Анатольевна ', 'productivity': 1992, 'work_hours': 0}]

orders = [{'aroma': '', 'length': 0, 'bobbin_quantity': 0, 'quantity': 0}]
orders_sample = [{'aroma': 'ЛС Стекло / Духи концентрированные Rose, Jasmine, Narcissus (50мл)', 'length': 22, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС Стекло / Духи концентрированные Tobacco, Vetiver & Amber (50мл)', 'length': 21, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС Стекло / Духи концентрированные Vetiver, Neroli, Orange (50мл)', 'length': 21, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации Cedarwood & Sandalwood & Amber, Patchouli (85мл)', 'length': 36, 'bobbin_quantity': 500, 'quantity': 1000},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации помещений Fiction (85мл)', 'length': 7, 'bobbin_quantity': 500, 'quantity': 3500},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации помещений Lemongrass & Vetiver, Amber (212,5мл)', 'length': 24, 'bobbin_quantity': 500, 'quantity': 1000},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации помещений Orange & Jasmine, Vanilla (212,5мл)', 'length': 22, 'bobbin_quantity': 500, 'quantity': 2000},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации помещений Rosemary & Lemon, Neroli (85мл)', 'length': 21, 'bobbin_quantity': 500, 'quantity': 2000},
{'aroma': 'ЛС Тубус / Диффузор. Средство для ароматизации помещений Vanilla Blend (85мл)', 'length': 12, 'bobbin_quantity': 500, 'quantity': 1000},
{'aroma': 'ЛС Тубус / Духи концентрированные Apple, Lotus (50мл)', 'length': 11, 'bobbin_quantity': 500, 'quantity': 5000},
{'aroma': 'ЛС Тубус / Духи концентрированные Grapefruit & Rose, Patchouli (50мл)', 'length': 25, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС Тубус / Духи концентрированные Neroli, Patchouli, Honey, Amber (50мл)', 'length': 28, 'bobbin_quantity': 500, 'quantity': 500},
{'aroma': 'ЛС Тубус / Духи концентрированные Powder (50мл)', 'length': 6, 'bobbin_quantity': 500, 'quantity': 500},
{'aroma': 'ЛС Тубус / Духи концентрированные Tobacco, Vetiver & Amber (50мл)', 'length': 21, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС Тубус / Духи концентрированные Vetiver, Neroli, Orange (50мл)', 'length': 21, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС / Жидкое мыло Ylang-Ylang & Vetiver, Musk (300мл)', 'length': 24, 'bobbin_quantity': 500, 'quantity': 5000},
{'aroma': 'ЛС / Крем увлажняющий для вьющихся волос Black Pepper, Vetiver, Neroli, Amber  (200мл)', 'length': 32, 'bobbin_quantity': 500, 'quantity': 3000},
{'aroma': 'ЛС / Масло для тела Pink Pepper, Elemi, Cinnamon, Leather (100мл)', 'length': 33, 'bobbin_quantity': 500, 'quantity': 5000},
{'aroma': 'ЛС / Сыворотка для волос Black Pepper, Vetiver, Neroli, Amber  (50мл)', 'length': 32, 'bobbin_quantity': 500, 'quantity': 5000},
{'aroma': 'ЛС Тубус / Духи концентрированные Pink Pepper, Elemi, Cinnamon, Leather (50мл)', 'length': 33, 'bobbin_quantity': 500, 'quantity': 10000},
{'aroma': 'ЛС Тубус / Духи концентрированные Black Vanilla (50мл)', 'length': 12, 'bobbin_quantity': 500, 'quantity': 5000},
{'aroma': 'ЛС Стекло / Духи концентрированные Pink Pepper, Elemi, Cinnamon, Leather (50мл)', 'length': 33, 'bobbin_quantity': 500, 'quantity': 10000}]


def load_sample_data():
    if sample_data:
        calligraphers = [{'name': '', 'productivity': 0, 'work_hours': 0}]
        orders = [{'aroma': '', 'length': 0, 'bobbin_quantity': 0, 'quantity': 0}]
    else:
        calligraphers = calligraphers_sample.copy()
        orders = orders_sample.copy()
    st.session_state.calligraphers = calligraphers
    st.session_state.edited_calligraphers = st.session_state.calligraphers.copy()
    st.session_state.orders = orders
    st.session_state.edited_orders = st.session_state.orders.copy()


with st.sidebar:
    calculation_type = st.radio(
    "Выберите параметр запуска",
    ["Разбить заказы на бобины", "Распределить заказы целиком"],
    )
    sample_data = st.toggle('Пример данных', 
                            on_change = load_sample_data)
    compute_length = st.select_slider(
    'Выберите точность расчёта. Чем выше точность, тем длиннее время работы алгоритмма',
    options=['глазом не моргнуть', 'посмотрю как крутится кружочек прогресса', 'пойду покурю... и кофе попью', 'а незамахнуться ли на всю Матрицу'])


st.title("Распределение заказов каллиграфов")

# Initialize session state with dataframes
# Include initialization of "edited" slots by copying originals
if 'calligraphers' not in st.session_state:
    st.session_state.calligraphers = calligraphers
    st.session_state.edited_calligraphers = st.session_state.calligraphers.copy()
    st.session_state.orders = orders
    st.session_state.edited_orders = st.session_state.orders.copy()


# Создание списка каллиграфов
st.header("Список каллиграфов")
st.session_state.edited_calligraphers = st.data_editor(st.session_state.calligraphers, num_rows='dynamic', column_config={
        "name": st.column_config.TextColumn(label="ФИО каллиграфа", width=400), 
        "productivity": st.column_config.NumberColumn(label="Производительность каллиграфа в символах в час", min_value=1),
        "work_hours": st.column_config.NumberColumn(label="Время работы каллиграфа в неделю в часах", min_value=1)
    })

# Создание списка заказов
st.header("Список заказов")
st.session_state.edited_orders = st.data_editor(st.session_state.orders, num_rows='dynamic',  column_config={
        "aroma": st.column_config.TextColumn(label="Название маркировки", width=1000), 
        "length": st.column_config.NumberColumn(label="Длина символов аромата в маркировке", min_value=1),
        "bobbin_quantity": st.column_config.NumberColumn(label="Количество маркировок в бобине", min_value=1),
        "quantity": st.column_config.NumberColumn(label="Количество маркировок в заказе", min_value=1),
    })

# Save edits by copying edited dataframes to "original" slots in session state
def save_edits():
    st.session_state.calligraphers = st.session_state.edited_calligraphers.copy()
    st.session_state.orders = st.session_state.edited_orders.copy()

def split_orders(orders):
    split_orders = []
    for order in orders:
        n_bobbins = int(order['quantity'] // order['bobbin_quantity'])
        for _ in range(n_bobbins):
            split_order = order.copy()
            split_order['quantity'] = order['bobbin_quantity']
            split_orders.append(split_order)
    return split_orders

def fitness(chromosome, calligraphers, orders):
    times = [0] * len(calligraphers)
    for i in range(len(chromosome)):
        calligrapher_index = chromosome[i]
        calligrapher = calligraphers[calligrapher_index]
        order = orders[i]
        time = round((order['length'] * order['quantity']) / calligrapher['productivity'], 1)
        times[calligrapher_index] += time
    max_time = max(times)
    
    penalty = 0
    mean_time = np.mean(times)
    for time in times:
        penalty += abs(time - mean_time)
    
    unique_calligraphers = len(set(chromosome))
    penalty += penalty * (2 ** (len(calligraphers) - unique_calligraphers))
    
    return max_time + penalty,

def genetic_algorithm(calligraphers, orders, population_size=200, max_generations=1000):
    
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    
    toolbox = base.Toolbox()
    
    toolbox.register("indices", random.choices, range(len(calligraphers)), k=len(orders))
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", fitness, calligraphers=calligraphers, orders=orders)
    
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
    
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    population = toolbox.population(n=population_size)
    
    hof = tools.HallOfFame(1)
    
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", np.mean)
    stats.register("std", np.std)
    stats.register("min", np.min)
    stats.register("max", np.max)
    
    population, logbook = algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=max_generations,
                        stats=stats, halloffame=hof)

    best_chromosome = hof[0]
   
    return best_chromosome

def format_report_time_by_calligrapher(best_chromosome, calligraphers):

    data = []
    order_counts = {}
    calligrapher_times = {}
    calligrapher_work_hours = {}
    for i in range(len(best_chromosome)):
        calligrapher_index = best_chromosome[i]
        calligrapher_name = calligraphers[calligrapher_index]['name']
        calligrapher_work_hours[calligrapher_name] = calligraphers[calligrapher_index]['work_hours']
        order_name = orders[i]['aroma']
        if order_name not in order_counts:
            order_counts[order_name] = {}
        if calligrapher_name not in order_counts[order_name]:
            order_counts[order_name][calligrapher_name] = 0
        order_counts[order_name][calligrapher_name] += orders[i]['quantity']
        
        if calligrapher_name not in calligrapher_times:
            calligrapher_times[calligrapher_name] = 0
        time = round((orders[i]['length'] * orders[i]['quantity']) / calligraphers[calligrapher_index]['productivity'], 1)
        calligrapher_times[calligrapher_name] += time
            
    total_time = 0
    for calligrapher_name in calligrapher_times:
        time = calligrapher_times[calligrapher_name]
        total_time += time
        weeks = round(time / calligrapher_work_hours[calligrapher_name], 1)
        data.append([calligrapher_name, time, calligrapher_work_hours[calligrapher_name], weeks])

    return data


def format_report_orders_by_calligrapher(best_chromosome, calligraphers):

    data = []

    times = [0] * len(calligraphers)

    for i in range(len(best_chromosome)):
            calligrapher_index = best_chromosome[i]
            calligrapher = calligraphers[calligrapher_index]
            order = orders[i]
            time = round((order['length'] * order['quantity']) / calligrapher['productivity'], 1)
            times[calligrapher_index] += time

    for i, calligrapher in enumerate(calligraphers):
        calligrapher_orders = [orders[j] for j in range(len(best_chromosome)) if best_chromosome[j] == i]
        aroma_totals = {}
        for order in calligrapher_orders:
            if order['aroma'] not in aroma_totals:
                aroma_totals[order['aroma']] = 0
            aroma_totals[order['aroma']] += order['quantity']
        for aroma, total in aroma_totals.items():
            weeks = round(times[i] / calligrapher['work_hours'], 1)
            data.append([calligrapher['name'], aroma, total, calligrapher['productivity'], calligrapher['work_hours'], times[i], weeks])

    return data


# def format_report_calligraphers_by_order(best_chromosome, calligraphers):
#     # Вывод результата
#     order_counts = {}
#     calligrapher_times = {}
#     for i in range(len(best_chromosome)):
#         calligrapher_index = best_chromosome[i]
#         calligrapher_name = calligraphers[calligrapher_index]['name']
#         order_name = orders[i]['aroma']
#         if order_name not in order_counts:
#             order_counts[order_name] = {}
#         if calligrapher_name not in order_counts[order_name]:
#             order_counts[order_name][calligrapher_name] = 0
#         order_counts[order_name][calligrapher_name] += orders[i]['quantity']
        
#         if calligrapher_name not in calligrapher_times:
#             calligrapher_times[calligrapher_name] = 0
#         time = (orders[i]['length'] * orders[i]['quantity']) / calligraphers[calligrapher_index]['productivity']
#         calligrapher_times[calligrapher_name] += time

#     for order_name in order_counts:
#         print(f"Order: {order_name}")
#         for calligrapher_name in order_counts[order_name]:
#             quantity = order_counts[order_name][calligrapher_name]
#             print(f"Calligrapher {calligrapher_name} assigned {quantity} labels")
            
#     print("\nTotal time by calligrapher:")
#     total_time = 0
#     for calligrapher_name in calligrapher_times:
#         time = calligrapher_times[calligrapher_name]
#         total_time += time
#         print(f"Calligrapher {calligrapher_name} total time: {time:.1f} hours") 
#     print(f"Total time: {total_time:.2f} hours")

#     times = [0] * len(calligraphers)

#     for i in range(len(best_chromosome)):
#             calligrapher_index = best_chromosome[i]
#             calligrapher = calligraphers[calligrapher_index]
#             order = orders[i]
#             time = (order['length'] * order['quantity']) / calligrapher['productivity']
#             times[calligrapher_index] += time

#     for i, calligrapher in enumerate(calligraphers):
#         print(f"{calligrapher['name']}: {times[i]:.2f} hours")
#         calligrapher_orders = [orders[j] for j in range(len(best_chromosome)) if best_chromosome[j] == i]
#         aroma_totals = {}
#         for order in calligrapher_orders:
#             if order['aroma'] not in aroma_totals:
#                 aroma_totals[order['aroma']] = 0
#             aroma_totals[order['aroma']] += order['quantity']
#         for aroma, total in aroma_totals.items():
#             print(f"\t{aroma}: {total} units")
    
# Запуск расчета распределения заказов по каллиграфам
if st.button('Запустить расчет'):
    
    save_edits()
    
    valid_calligraphers = [c for c in st.session_state.calligraphers if c['productivity'] > 0 and c['work_hours'] > 0] 
    
    if calculation_type == "Разбить заказы на бобины":
        orders = split_orders(st.session_state.orders) 
    else:
        orders = st.session_state.orders
    
    match compute_length:
        case 'глазом не моргнуть':
            gen = 100
            population = 10
        case 'посмотрю как крутится кружочек прогресса':
            gen = 1000
            population = 200
        case 'пойду покурю... и кофе попью':
            gen = 10000
            population = 500
        case 'а незамахнуться ли на всю Матрицу':
            gen = 50000
            population = 1000
        case _:
            gen = 1000
            population = 200
    with st.spinner('Расчет распределения заказов по каллиграфам...'):
        best_chromosome = genetic_algorithm(valid_calligraphers, orders, population_size=population, max_generations = gen)

        st.success('Расчет завершен!')

        # Вывод результатов расчета

        data = format_report_time_by_calligrapher(best_chromosome, valid_calligraphers)
        result = pd.DataFrame(data,
                              columns=['name', 'time', 'work_hours', 'weeks'])

        st.header("Суммарное время выполнения заказов")
        st.dataframe(result, column_config={
                "name": st.column_config.TextColumn("ФИО каллиграфа", width=400), 
                "time": st.column_config.NumberColumn("Время выполнения заказов, часы", format="%.1f"),
                "work_hours": st.column_config.NumberColumn("Рабочих часов в неделю", format="%d"),
                "weeks": st.column_config.NumberColumn("Недель", format="%.1f")
            })
        st.header("Суммарное время выполнения заказов в часах")
        st.bar_chart(result,
            x='name',
            y='time'
        )

        st.header("Суммарное время выполнения заказов в неделях")
        st.bar_chart(result,
            x='name',
            y='weeks'
        )

        data = format_report_orders_by_calligrapher(best_chromosome, valid_calligraphers)
        result = pd.DataFrame(data,
                              columns=['name', 'aroma', 'quantity', 'productivity', 'work_hours', 'time', 'weeks'])
        st.header("Список заказов по каллиграфам")
        st.dataframe(result, column_config={
                "name": st.column_config.TextColumn("ФИО каллиграфа", width=400), 
                "aroma": st.column_config.TextColumn("Название маркировки", width=1000),
                "quantity": st.column_config.NumberColumn("Количество маркировок", format="%d"),
                "productivity": st.column_config.NumberColumn("Производительность, символов/час", format="%d"),
                "work_hours": st.column_config.NumberColumn("Рабочих часов в неделю", format="%d"),
                "time": st.column_config.NumberColumn("Время выполнения заказа, часы", format="%.1f"),
                "weeks": st.column_config.NumberColumn("Время выполнения заказа, недели", format="%.1f")
            })

        csv = result.to_csv(sep=';', decimal=',').encode('utf-8-sig')

        st.download_button(
            label="Сохранить в формате CSV",
            data=csv,
            file_name='каллиграфы_заказы.csv',
            mime='text/csv',
        )
