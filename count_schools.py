import csv
import time
import itertools


def school_by_state():
    sch_dict = csv.DictReader(open('school_data.csv', 'r'))
    start_time = time.time()
    # total = 0
    print(" ")
    print("Schools by State: ")
    for key, group in itertools.groupby(sch_dict, lambda x: x['LSTATE05']):
        schools_by_state = sum(1 for x in group)
        # total += schools_by_state 
        print(f'{key} : {schools_by_state}')
    print(f'Search time for school_by_state: {(time.time() - start_time)}')
    # print(f'Total number of schools {total}')

# currently the fastest total count
def total_school_count():
    sch_dict = csv.DictReader(open('school_data.csv', 'r'))
    start_time = time.time()
    row_count = sum(1 for row in sch_dict) 
    print(" ")
    print(f'Total Schools: {row_count}')
    print(f'Search time for total_school_count: {(time.time() - start_time)}')

def schools_by_metro():
    sch_dict = csv.DictReader(open('school_data.csv', 'r'))
    metro_sort = sorted(sch_dict, key=lambda x: x['MLOCALE'])
    start_time = time.time()
    print(" ")
    print("Schools by Metro: ")
    for key, group in itertools.groupby(metro_sort, lambda x: x['MLOCALE']):
        schools_by_metro = sum(1 for x in group) 
        print(f'{key} : {schools_by_metro}')
    print(f'Search time for schools_by_metro: {(time.time() - start_time)}')


def city_most_schools():
    uniquekeys = {}
    sch_dict = csv.DictReader(open('school_data.csv', 'r'))
    city_sort = sorted(sch_dict, key=lambda x: x['LCITY05'])
    start_time = time.time()
    for key, group in itertools.groupby(city_sort, lambda x: x['LCITY05']):
        schools_by_city = sum(1 for x in group)
        newrow = ({key: schools_by_city})
        uniquekeys.update(newrow)
    max_city = max(uniquekeys.items(), key=lambda x: x[1])
    print("")
    print(f'City with the most schools: {max_city[0]} ({max_city[1]} schools)')
    print(f'Search time for city_most_schools: {(time.time() - start_time)}')


def unique_cities():
    uniquekeys = []
    sch_dict = csv.DictReader(open('school_data.csv', 'r'))
    city_sort = sorted(sch_dict, key=lambda x: x['LCITY05'])
    start_time = time.time()
    for key, group in itertools.groupby(city_sort, lambda x: x['LCITY05']):
        uniquekeys.append(key)
    city_count = len(uniquekeys)
    print("")
    print(f'Unique cities with at least one school: {city_count}')
    print(f'Search time for unique_cities: {(time.time() - start_time)}')

# schools_by_metro()
# school_by_state()
city_most_schools()
# total_school_count()
# unique_cities()