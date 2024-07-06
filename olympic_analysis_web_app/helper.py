import numpy as np

#medal count
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['Total'] = medal_tally['Total'].astype('int')

    return medal_tally

def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')
    return(years,country)

#functions for graphs
def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Edition', 'No of participating nations']
    nations_over_time = nations_over_time.sort_values('Edition')
    return nations_over_time

def events_each_year(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    events_over_time.columns = ['Edition', 'No of events']
    events_over_time = events_over_time.sort_values('Edition')
    return events_over_time

def athletes_each_year(df):
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athletes_over_time.columns = ['Edition', 'No. of athletes']
    athletes_over_time = athletes_over_time.sort_values('Edition')
    return athletes_over_time

#function  to return top athletes in selected sport
def most_successful(df, sport):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])
    # Filter by sport if it's not 'Overall'
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    # Count the number of medals for each athlete
    temp_df = temp_df['Name'].value_counts().reset_index().head(15)
    temp_df.columns = ['Name', 'Medal_Count']
    # Ensure the 'Name' columns are of type string for merging
    df['Name'] = df['Name'].astype(str)
    temp_df['Name'] = temp_df['Name'].astype(str)
    # Merge with the original DataFrame
    merged_df = temp_df.merge(df, on='Name', how='left')
    # Print the columns of the merged DataFrame for debugging
    print("Columns in merged_df:", merged_df.columns)
    # Select and rename the relevant columns, dropping duplicates
    result = merged_df[['Name', 'Medal_Count', 'Sport', 'region']].drop_duplicates('Name')
    return result


def fetch_medal_tally(df,year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    elif year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['Total'] = x['Total'].astype('int')

    return x

#medals of a country each year
def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    # counting team medal as 1
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

#medal of country in each sport every year
def country_heatmap(df,selected_country):
    temp_df = df.dropna(subset=['Medal'])
    # counting team medal as 1
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'],inplace=True)
    new_df = temp_df[temp_df['region'] == selected_country]
    pt=new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0)
    return pt

#most successful athletes by country
def most_successful_countrywise(df, selected_country):
    # Drop rows where 'Medal' is NaN
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == selected_country]

    # Count the number of medals for each athlete
    temp_df = temp_df['Name'].value_counts().reset_index().head(10)
    temp_df.columns = ['Name', 'Medal_Count']

    # Ensure the 'Name' columns are of type string for merging
    df['Name'] = df['Name'].astype(str)
    temp_df['Name'] = temp_df['Name'].astype(str)

    # Merge with the original DataFrame
    merged_df = temp_df.merge(df, on='Name', how='left')

    # Print the columns of the merged DataFrame for debugging
    print("Columns in merged_df:", merged_df.columns)

    # Select and rename the relevant columns, dropping duplicates
    result = merged_df[['Name', 'Medal_Count', 'Sport']].drop_duplicates('Name')

    return result

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    men = athlete_df[athlete_df['Sex']=='M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year').count()['Name'].reset_index()

    final=men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final



