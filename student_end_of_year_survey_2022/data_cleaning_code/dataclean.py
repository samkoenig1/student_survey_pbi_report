import pandas as pd

#Read Raw CSV File
df = pd.read_csv(r"*",header=0,encoding = 'unicode_escape')
#remove duplicates
df.drop_duplicates(keep='last')


#Rename Columns to remove spaces, and strange syntax. Mark as specify for free response race/ethnicity questions
df = df.set_axis(['participant_id', 'program', 'background_identity', 'african_american',
                  'specify','specify','asian_american','specify','specify','latinx/histpanic',
                  'specify','specify','native_american',
                  'specify','specify', 'native_alaskan','specify','specify','native_hawaian',
                  'specify','specify', 'white_caucasian', 'specify','specify','middle_eastern',
                  'specify','specify','multiracial','specify','specify',
                  'other','specify','specify','prefer_not_to_respond','gender',
                  'nps_string','nps_numeric', 'valuable_experience','chance_of_job',
                  'experience_in_accelerator','program_community','broader_movement','mentor',
                  'next_generation_leaders','relationships_virtual_hybrid'], axis=1)


#Split program filed into region and cohort based on : delimiter
df[['region', 'cohort']] = df["program"].str.split(': ', expand=True)


#Define seperate column if they identify as low income
def low_income (row):
   if 'low-income' in row['background_identity'] :
      return "Low Income"
   return "Not Low Income"

#add variable to dataframe
df['low_income'] = df.apply(low_income, axis=1)

#Define seperate column if they identify as first generation
def first_gen (row):
   if 'first-generation' in row['background_identity'] :
      return "First Generation"
   return "Not First Generation"

#add variable to dataframe
df['first_gen'] = df.apply(first_gen, axis=1)


#Define seperate column if they identify as first generation
def person_of_color (row):
   if 'person of color' in row['background_identity'] :
      return "Person of Color"
   return "Not Person of Color"

#add variable to dataframe
df['person_of_color'] = df.apply(person_of_color, axis=1)



#Define numeric nps column for promoters, passives and detractors for easy calculation.
def nps_score (row):
   if row['nps_numeric'] >=9: return 1
   elif row['nps_numeric'] >=7: return 0
   elif row['nps_numeric'] >=0: return -1



#add variable to dataframe
df['nps_score'] = df.apply(nps_score, axis=1)


#define student information file
student_information_file = df[['participant_id', 'cohort', 'region', 'person_of_color', 'first_gen', 'low_income', 'gender']]

#define nps file
nps = df[['participant_id', 'nps_string','nps_numeric', 'nps_score']]


#define survey_response file
survey_response = df[['participant_id', 'valuable_experience',	'chance_of_job','program_community',	'broader_movement',	'mentor','next_generation_leaders',	'relationships_virtual_hybrid']]

#export files to csv for import into PowerBI
student_information_file.to_csv('student_information_file.csv')
nps.to_csv('nps.csv')
survey_response.to_csv('survey_response.csv')
