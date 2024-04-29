import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("CRT Discourse in Partisan News")

st.markdown("### Topics")

df = pd.read_csv("Global BERTopic Model Results.csv")
df.set_index('Topic', inplace=True)
st.dataframe(df, use_container_width=True)

st.markdown("----")

st.markdown("### Prominent Terms Overtime")

col1, col2 = st.columns([1, 3])

with col1:
    multiselect_options = []
    for i in df['Label']:
        multiselect_options.append(i)
    options = st.multiselect(
        'Select one or more topics',
        multiselect_options,
        ['Racist Towards White People'])

with col2:
    df = pd.read_csv("dynamic_model.csv")
    topics = [multiselect_options.index(option) for option in options]
    df = df[df['Topic'].isin(topics)]
    df['Date'] = pd.to_datetime(df['Date'])
    grouped_df = df.groupby(['Topic', 'Date']).agg(
        {'Frequency': 'sum', 'Terms': lambda x: ', '.join(x)}).reset_index()
    labels = [multiselect_options[topic] for topic in grouped_df['Topic']]
    grouped_df['Label'] = labels

    filtered_df = grouped_df.groupby('Topic', group_keys=False).apply(
        lambda x: x.nlargest(4, 'Frequency'))

    filtered_df.reset_index(drop=True, inplace=True)

    fig = px.line(grouped_df,
                  x='Date',
                  y='Frequency',
                  color='Label',
                  title='Frequency vs Date by Topic',
                  hover_data={'Terms': True},
                  labels={'Frequency': 'Frequency',
                          'Date': 'Date', 'Topic': 'Topic'},
                  line_shape='linear',
                  width=1200,
                  height=600)

    fig.add_trace(px.scatter(filtered_df,
                             x='Date',
                             y='Frequency',
                             text='Terms').data[0])

    fig.update_layout(
        title=dict(text="Prominent Terms Overtime",
                   font=dict(size=24, color="black")),
        xaxis=dict(title='Date',
                   title_font=dict(size=20, color='black')),
        yaxis=dict(title='Frequency',
                   title_font=dict(size=20, color='black')),
        font=dict(size=16, color='black')
    )

    st.plotly_chart(fig)
