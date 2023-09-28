import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
import ast

st.set_page_config(page_title="Plotting Demo")
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title('Analytics')

new_df = pd.read_csv("datasets/data_viz1.csv")

with open('datasets/feature_text', 'rb') as file:
    feature_text = pickle.load(file)

group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longtitude']].mean()

# 2)
st.header('Sector Price per Sqft Geomap')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longtitude", color="price_per_sqft", size="built_up_area",
                        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                        mapbox_style="open-street-map", width=1200, height=700, hover_name=group_df.index)

st.plotly_chart(fig, use_container_width=True)

# 2)
st.header('Features Wordcloud')

wordcloud_df = pd.read_csv("datasets/wordcloud.csv")

# Create a Sector Selector Widget
selected_sector = st.selectbox("Select Sector:", ['All'] + list(wordcloud_df['sector'].unique()))


# Define a function to update the word cloud based on the selected sector
def update_wordcloud(selected_sector):
    if selected_sector == 'All':
        filtered_data = wordcloud_df
    else:
        filtered_data = wordcloud_df[wordcloud_df['sector'] == selected_sector]

    main = [item for items in filtered_data['features'].dropna().apply(ast.literal_eval) for item in items]
    feature_text = ' '.join(main)

    wordcloud = WordCloud(width=800, height=800,
                          background_color='black',
                          stopwords={'s'},  # Any stopwords you'd like to exclude
                          min_font_size=10).generate(feature_text)

    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot()


update_wordcloud(selected_sector)

# 3) Area Vs Price

st.header("Area Vs Price")

property_type = st.selectbox("Select property Type:", ['All'] + list(new_df['property_type'].unique()))

if property_type == "All":
    fig1 = px.scatter(new_df, x="built_up_area", y="price", color="bedRoom", title="Area Vs Price",
                      color_continuous_scale=px.colors.cyclical.IceFire)
    st.plotly_chart(fig1, use_container_width=True)
elif property_type == "flat":
    fig1 = px.scatter((new_df[new_df['property_type'] == 'flat']), x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price",
                      color_continuous_scale=px.colors.cyclical.IceFire)
    st.plotly_chart(fig1, use_container_width=True)

else:
    fig1 = px.scatter((new_df[new_df['property_type'] == 'house']), x="built_up_area", y="price", color="bedRoom",
                      title="Area Vs Price",
                      color_continuous_scale='Viridis')
    st.plotly_chart(fig1, use_container_width=True)

# 4 Pie Chart

st.header("Pie Char of Bedroom % Sector Wise ")

col1, col2 = st.columns(2)

with col1:
    property_type = st.selectbox("Select Property Type:", ['Both'] + list(new_df['property_type'].unique()))

with col2:
    sector_type = st.selectbox("Select Sector:", ['Overall'] + list(new_df['sector'].unique()))

if property_type == 'Both' and sector_type == 'Overall':
    fig2 = px.pie(new_df, names='bedRoom', title="Sector Wise Bedroom %")
    st.plotly_chart(fig2, use_container_width=True)
else:
    filtered_df = new_df[(new_df['sector'] == sector_type) & (new_df['property_type'] == property_type)]
    fig2 = px.pie(filtered_df, names='bedRoom')
    st.plotly_chart(fig2, use_container_width=True)

# plot 5

st.header('Side by Side BHK price comparision')
fig3 = px.box(new_df[new_df['bedRoom'] <= 4], x = 'bedRoom', y='price', title='BHK price Range')
st.plotly_chart(fig3, use_container_width=True)

#plot 6 sns.displot(data=data, x="total_bill", kind="kde")
st.header('Distribution plot Property Type Vs Price')

fig4 = plt.figure(figsize= (10,4))
sns.distplot(new_df[new_df['property_type']=='flat']['price'], label='house')
sns.distplot(new_df[new_df['property_type']=='house']['price'], label='flat')
#st.plotly_chart(fig4, use_container_width=True)
plt.legend()
st.pyplot(fig4)


