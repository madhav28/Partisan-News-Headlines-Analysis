import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("CRT Discourse in Partisan News")

st.markdown("### Global Topics")

df = pd.read_csv("Global BERTopic Model Results.csv")
df.set_index('Topic', inplace=True)
st.dataframe(df, use_container_width=True)

st.markdown("----")

st.markdown("### Topics Evolution")

col1, col2 = st.columns([1, 3])

with col1:
    multiselect_options = []
    for i in range(30):
        multiselect_options.append('Topic '+str(i))
    options = st.multiselect(
    'Select one or more topics',
    multiselect_options,
    ['Topic 0', 'Topic 1', 'Topic 2'])

with col2:
    df = pd.read_csv("dynamic_model.csv")
    options = [int(x.split()[1]) for x in options]
    df = df[df['Topic'].isin(options)]
    df['Date'] = pd.to_datetime(df['Date'])
    grouped_df = df.groupby(['Topic', 'Date']).agg({'Frequency': 'sum', 'Terms': lambda x: ', '.join(x)}).reset_index()

    fig = px.line(grouped_df, 
                x='Date', 
                y='Frequency', 
                color='Topic', 
                title='Frequency vs Date by Topic',
                hover_data={'Terms': True},
                labels={'Frequency': 'Frequency', 'Date': 'Date', 'Topic': 'Topic'},
                line_shape='linear',
                width=1200,  
                height=600)

    st.plotly_chart(fig)