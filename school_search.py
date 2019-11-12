import csv
import time
import itertools

global search
global search_terms
global search_combos
sch_dict = csv.DictReader(open('school_data.csv', 'r'))
iter_name_sort = sorted(sch_dict, key=lambda x: x['SCHNAM05'])

def format_data():
   grade_level = {'HIGH ', 'ELEMENTARY', 'MIDDLE ', 'ELEM ', 'PRIMARY', 'CONTINUATION'}
     
   for col in iter_name_sort:
      # search_str = col['SCHNAM05'] + " " + col['LCITY05'] + " " + col['LSTATE05']
      search_str = col['SCHNAM05']
      col['SEARCHCOL'] = search_str
      col['COUNT'] = 0
      col['CITYMATCH'] = "False"
      col['NAMEMATCH'] = "False" 
      col['SCH_TYPE'] = ""
      #if grade_level term is in the search(name)col, then it's the school type
      for x in grade_level:
         if x in col['SEARCHCOL']:
            col['SCH_TYPE'] = x
      col['SCH_TYPE_SEARCH'] = ""
      col['SCH_SPECIAL'] = ""

def format_search_input(search_var):
   s_upper = search_var.upper()
   search_terms = s_upper.split()
   #  print(search_terms)
   return search_terms

def gen_search_combinations(search_var):
   search_combos = []
   s_upper = search_var.upper()
   search_terms_combo = s_upper.split()
   # print(search_terms_combo)
   iter_combo = itertools.permutations(search_terms_combo)
   
   for x in iter_combo:
      search_combos.append(x)
   return search_combos

def run_search(search_var, search_terms_var, search_combos_var):
   s_upper = search_var.upper()
   global start_time
   results = []
   results_rnd2 = []
   exclude_common = ['HIGH ', 'SCHOOL', 'ELEMENTARY', 'MIDDLE ', 'ELEM ', 'CHARTER']
   grade_level = ['HIGH ', 'ELEMENTARY', 'MIDDLE ', 'ELEM ','PRIMARY', 'CONTINUATION']
   special = ['CHARTER', "CENTER ", 'ACADEMY', 'COMMUNITY', 'ALTERNATIVE']
   sch_type = ""
   start_time = time.time()
   i = 0
   j = 0
   
      
   while i < len(iter_name_sort):
      appears=0
      #if search input is an exact match to school name, add 30
      if s_upper == iter_name_sort[i]['SCHNAM05']:
            appears += 30
            # iter_name_sort[i]['COUNT'] = appears
      #if search input combination is an exact match to school name, add 25
      for x in search_combos_var:
         if " ".join(x) == iter_name_sort[i]['SCHNAM05']:
            # print('printing match')
            # print(x)
            appears +=25
      for x in search_terms_var:
         #if search term is in searchcol/name but not in exclude_common term, it's probably a unique name, add frequency
         if x in iter_name_sort[i]['SEARCHCOL'] and x not in exclude_common:
            appears += 20
            if x in iter_name_sort[i]['SCHNAM05']:
               iter_name_sort[i]['NAMEMATCH'] = "True"
         #if a search term not in name, not in exclude, not in city, -25
         if x not in iter_name_sort[i]['SEARCHCOL'] and x not in exclude_common and x not in iter_name_sort[i]['LCITY05'] :
            appears -= 25
         #if search term is in city, then there's a city match, add 8
         if x in iter_name_sort[i]['LCITY05'] and x not in exclude_common:
            iter_name_sort[i]['CITYMATCH'] = "True"
            appears += 8 
         #if search term is in name and in special column, it's a special school, add 30
         if x in iter_name_sort[i]['SCHNAM05'] and x in special:
            iter_name_sort[i]['SCH_SPECIAL'] = "True"
            appears += 30
         #if search term is in name column and in grade_level, then that's the type of school being searched for, add 5
         if x in iter_name_sort[i]['SCHNAM05'] and x in grade_level:
            sch_type = x
            iter_name_sort[i]['SCH_TYPE_SEARCH'] = sch_type
            appears += 5
         else:
            iter_name_sort[i]['SCH_TYPE_SEARCH'] = sch_type
      iter_name_sort[i]['COUNT'] = appears
      i += 1
      
   for row in iter_name_sort:
      #if the count is > 0 or the city matches, add the row
      if row['COUNT'] > 0 or row['CITYMATCH'] == "True":
         # print(row)
         results.append(row)
   
   while j < len(results):
      count_common = 0
      type_match = 0
      current = results[j]['COUNT']
      for x in search_terms_var:
         if results[j]['SCH_TYPE'] and results[j]['SCH_TYPE_SEARCH']:
            if results[j]['SCH_TYPE'] != results[j]['SCH_TYPE_SEARCH']:
               type_match = -30
            if results[j]['SCH_TYPE'] == results[j]['SCH_TYPE_SEARCH']:
               type_match = 30
         
      results[j]['COUNT'] = current + count_common + type_match 

      j += 1
   
   for row in results:
      results_rnd2.append(row)

   match_city_or_name = [x for x in results_rnd2 if (x['CITYMATCH'] == "True" or x['NAMEMATCH'] == "True" or ['SCH_SPECIAL'] == "True") and x['COUNT']>=1 ]
   sort_count_name = sorted(match_city_or_name, key=lambda x: (-x['COUNT'], x['SCHNAM05'],  ))
   
   return sort_count_name

def print_results(file_var, search_var):
   print(f'Results for: "{search_var}"" search took: {(time.time() - start_time)}s')

   j=1
   for col in file_var:
      if col["COUNT"] > 0 and j < 4:
         print(f'{j}. {col["SCHNAM05"]}')
         print(f'{col["LCITY05"]} {col["LSTATE05"]}')
         j += 1

def school_search(search):
   format_data()
   search_terms = format_search_input(search)
   search_combos = gen_search_combinations(search)
   sort_count_name = run_search(search, search_terms,search_combos)
   print_results(sort_count_name, search)
    
# school_search("elementary school highland park") #yes
# school_search("jefferson belleville") #yes
# school_search("riverside school 44") #yes
# school_search("granada charter school") #yes
# school_search("foley high alabama") #yes, one result
# school_search("KUSKOKWIM") #yes
# school_search("montessori glendale")
# school_search("fairview center")
# school_search("NANAIKAPONO")
