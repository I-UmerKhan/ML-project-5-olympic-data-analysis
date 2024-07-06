import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')

df=preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympic analysis")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal count','Overall analysis','country-wise analysis','athlete wise analysis')
)

if user_menu=='Medal count':
    st.sidebar.header("Medal Count")
    years,country= helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country",country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Overall Performance" )
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " performance in " + str(selected_year) + " olympic")

    st.table(medal_tally)

# overall
if user_menu == 'Overall analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]
    # top stats
    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(cities)
    with col3:
        st.header("Sports")
        st.title(sports)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.header("Events")
        st.title(events)
    with col5:
        st.header("Athletes")
        st.title(athletes)
    with col6:
        st.header("Region")
        st.title(nations)

    # figures
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time, x='Edition', y='No of participating nations')
    st.title("Participating nations over time")
    st.plotly_chart(fig)

    events_over_time = helper.events_each_year(df)
    fig = px.line(events_over_time, x='Edition', y='No of events')
    st.title("Number of events over time")
    st.plotly_chart(fig)

    athletes_over_time = helper.athletes_each_year(df)
    fig = px.line(athletes_over_time, x='Edition', y='No. of athletes')
    st.title("Number of athletes over time")
    st.plotly_chart(fig)

    st.title("No. of events over time (Every sport)")
    fig1,ax = plt.subplots(figsize=(20,20))

    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig1)

    # most successful athletes
    st.title("Most successful athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')
    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'country-wise analysis':
    #line plot
    st.sidebar.title("countrywise medal over the year")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox('Select a country', country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title("countrywise medal over the year")
    st.plotly_chart(fig)

    #heatmap
    st.title("Medals of country in each sport every year")
    pt=helper.country_heatmap(df,selected_country)
    fig1, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig1)

    #most successful athletes by country
    st.title("Top 10 athletes of "+ selected_country)
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'athlete wise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall', 'Gold medalist', 'Silver medalist', 'Bronze medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600, xaxis_title="Age", yaxis_title="Density")
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    famous_sports = df['Sport'].value_counts().head(15).index.tolist()
    x = []
    name = []
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)
    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(
        autosize=False,
        width=1000,
        height=600,
        xaxis_title="Age",
        yaxis_title="Density"
    )
    st.title('Distribution of Age in popular sports (Gold medalist)')
    st.plotly_chart(fig)



    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots()
    palette = {'Gold': 'gold', 'Silver': 'silver', 'Bronze': 'brown', 'No medal': 'black'}
    sns.scatterplot(x='Weight', y='Height', hue='Medal', palette=palette, data=temp_df, ax=ax)
    plt.title('Height vs Weight by Medal Type')
    plt.xlabel('Weight')
    plt.ylabel('Height')
    st.pyplot(fig)

    st.title('Men vs women particpation over the years')
    final=helper.men_vs_women(df)
    fig=px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)



