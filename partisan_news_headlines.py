import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

st.title("CRT Discourse in Partisan News")

st.markdown("### Topics")

df = pd.read_csv("Global BERTopic Model Results.csv")
df.set_index('Topic', inplace=True)
st.dataframe(df, use_container_width=True)

st.markdown("----")

st.markdown("### Topics Evolution")

col1, col2 = st.columns([1, 3])

with col1:
    multiselect_options = []
    for i in df['Label']:
        multiselect_options.append(i)
    options = st.multiselect(
        'Select one or more topics',
        multiselect_options,
        ['2022 Midterm Elections'])

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

    fig = go.Figure()

    for label, data in grouped_df.groupby('Label'):
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Frequency'], mode='lines',
                                name=label, hoverinfo='text',
                                hovertext=data.apply(lambda row: f"Date: {row['Date'].strftime('%Y-%m-%d')}<br>Frequency: {row['Frequency']}<br>Terms: {row['Terms']}", axis=1)))

    fig.add_trace(go.Scatter(x=filtered_df['Date'], y=filtered_df['Frequency'], mode='markers',
                            hoverinfo='text',
                            hovertext=filtered_df.apply(lambda row: f"Date: {row['Date'].strftime('%Y-%m-%d')}<br>Frequency: {row['Frequency']}<br>Terms: {row['Terms']}", axis=1),
                            marker=dict(symbol='square', size=10),
                            showlegend=False))

    x_anchors = ['right', 'left']
    y_anchors = ['bottom', 'top']
    annotations = [dict(x=x, y=y, text=text, xanchor=x_anchors[i % len(x_anchors)], yanchor=y_anchors[i % len(y_anchors)], showarrow=False, font=dict(size=16))
                   for i, (x, y, text) in enumerate(zip(filtered_df['Date'], filtered_df['Frequency'], filtered_df['Terms']))]

    fig.update_layout(annotations=annotations)

    fig.update_layout(
        title="Prominent Terms Overtime",
        xaxis=dict(title='Date', tickformat="%b %Y"),
        yaxis=dict(title='Frequency'),
        legend=dict(title='Topic'),
        font=dict(size=16, color='black'),
        width=1200,
        height=600
    )

    fig.update_layout(title_font=dict(size=28, color="black"))
    fig.update_xaxes(title_font=dict(size=24, color='black'), tickfont=dict(size=16, color='black'))
    fig.update_yaxes(title_font=dict(size=24, color='black'))
    fig.update_layout(legend_title_font=dict(size=16, color='black'), legend_font=dict(size=16, color='black'))
    st.plotly_chart(fig)
