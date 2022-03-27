import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import base64
from Mypackages import datasets, helper

st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{"jpg"};base64,{base64.b64encode(open("static/bg1.jpg", "rb").read()).decode()});
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

datas = datasets.Data()
app_data, user_data = datas.get_data()

st.sidebar.title("Google App Store Dataset Analysis")
user_menu = st.sidebar.radio(
    'Select a option',
    ('App Summary','Overall Analysis','Category Wise Analysis', 'Type Wise Analysis')
)


if user_menu == 'App Summary':
    apps = list(app_data['App'].unique())
    apps.sort()
    selected_app = st.sidebar.selectbox("Select App", apps)

    temp_df = app_data[app_data['App']==selected_app]

    app_name = str(list(temp_df['App'])[0])
    app_category = str(list(temp_df['Category'])[0])
    app_rating = str(list(temp_df['Rating'])[0])
    app_reviews = str(list(temp_df['Reviews'])[0])
    app_size = str(list(abs(temp_df['Size']))[0])+"M"
    app_installs = str(list(temp_df['Installs'])[0])+"+"
    app_type = str(list(temp_df['Type'])[0])
    app_updated = str(list(temp_df['Last Updated'])[0])
    app_version = str(list(temp_df['Current Ver'])[0])


    st.header("App Summary")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("App")
        st.write(app_name)

    with col2:
        st.subheader("Category")
        st.write(app_category)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Rating")
        st.write(app_rating)

    with col2:
        st.subheader("Reviews")
        st.write(app_reviews)
    
    with col3:
        st.subheader("Last Updated")
        st.write(app_updated)


    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Size")
        st.write(app_size)

    with col2:
        st.subheader("Installs")
        st.write(app_installs)
    
    with col3:
        st.subheader("Type")
        st.write(app_type)
        
    with col4:
        st.subheader("Version")
        st.write(app_version)



if user_menu=='Category Wise Analysis':
    categories = list(app_data['Category'].unique())

    selected_category = st.sidebar.selectbox("Select Category", categories)
    
    st.title(f"{selected_category}")

    # Top Rated Apps
    current_category = helper.Category_wise_analysis(app_data, selected_category)
    temp_df = current_category.top_rated_apps()
    fig = px.funnel(temp_df,x="App", y = "Rating", color="App", title=f"Top Rated Apps In {selected_category} Category", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Top Reviewd Apps
    temp_df = current_category.top_reviewed_app()
    fig = px.funnel(temp_df,x="App", y = "Reviews", color="App", title=f"Most Reviewed Apps In {selected_category} Category", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Top Expensive Apps
    temp_df = current_category.top_expensive_apps()
    fig = px.funnel(temp_df,x="App", y = "Price($)", color="App", title=f"Most Expensive Apps In {selected_category} Category", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Max Installed Apps
    temp_df = current_category.max_installed_apps()
    fig = px.funnel(temp_df, x = "App", y = "Installs", color = "App", title=f"Max Installed Apps In {selected_category}", width =800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None, showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Content Rating
    temp_df = current_category.content_rating()
    fig = px.funnel(temp_df,x="Count", y = "Content Rating",color="Content Rating", width=800, height=500, title="Content Rating", color_discrete_sequence=["dodgerblue","darkorchid"])
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Free vs Paid count
    temp_df = current_category.free_vs_paid_count()
    fig = px.funnel(temp_df,x="Count", y = "Type", color="Type", width=800, height=500, title="Free VS Paid Apps Count",  color_discrete_sequence=["yellow","cyan"])
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Free vs Paid Rating
    temp_df = current_category.free_vs_paid_rating()
    fig = px.funnel(temp_df,x="Rating", y = "Type", color="Type", width=800, height=500, title="Free VS Paid Apps Average Rating",  color_discrete_sequence=["indigo","maroon"])
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Free vs Paid Reviews
    col1, col2 = st.columns(2)
    temp_df1, temp_df2 = current_category.free_vs_paid_reviews()

    with col1:
        fig = px.funnel(temp_df1,x="Reviews", y = "Type", color="Type", width=400, height=400, title="Free VS Paid Apps Total Reviews",  color_discrete_sequence=["orange","lightgreen"])
        fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)

    with col2:
        fig = px.funnel(temp_df2,x="Reviews", y = "Type", color="Type", width=400, height=400, title="Free VS Paid Apps Average Reviews",  color_discrete_sequence=["mediumpurple","plum"])
        fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)

    
    # Minimum Andriod Version Required
    temp_df = current_category.min_android_version()
    fig = px.pie(temp_df, names="Minimum_Android_Version", values = "Count", color = "Minimum_Android_Version",title="Minimum Android Version Required",width = 800, height=500 )
    fig.update_traces(textfont_size=12, textposition="outside")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)



if user_menu=='Type Wise Analysis':
    selected_type = st.sidebar.selectbox("Select Category",["Free", "Paid"])

    st.title(f"{selected_type} Apps Analysis")

    
    current_type = helper.Type_wise_analysis(app_data, selected_type)

    # Top Rated Apps
    temp_df = current_type.top_rated_apps()
    fig = px.funnel(temp_df,x="App", y = "Rating", color="App", title=f"Top Rated Apps", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Top Reviewd Apps
    temp_df = current_type.top_reviewed_app()
    fig = px.funnel(temp_df,x="App", y = "Reviews", color="App", title=f"Most Reviewed Apps", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Top Expensive Apps
    if selected_type=="Paid":
        temp_df = current_type.top_expensive_apps()
        fig = px.funnel(temp_df,x="App", y = "Price($)", color="App", title=f"Most Expensive Apps", width=800, height=500)
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)


    # Max Installed Apps
    temp_df = current_type.max_installed_apps()
    fig = px.funnel(temp_df, x = "App", y = "Installs", color = "App", title=f"Max Installed Apps", width =800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None, showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Content Rating
    temp_df = current_type.content_rating()
    fig = px.funnel(temp_df,x="Count", y = "Content Rating",color="Content Rating", width=800, height=500, title="Content Rating", color_discrete_sequence=["dodgerblue","darkorchid"])
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)
 
    # Minimum Andriod Version Required
    temp_df = current_type.min_android_version()
    fig = px.pie(temp_df, names="Minimum_Android_Version", values = "Count", color = "Minimum_Android_Version",title="Minimum Android Version Required",width = 800, height=500 )
    fig.update_traces(textfont_size=12, textposition="outside")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


if user_menu == 'Overall Analysis':
    st.header("Overall Analysis")

    overall = helper.Overall_analysis(app_data)
    
    # Top Rated Apps

    st.subheader("Top Rated Apps")
    temp_df, temp_df1 = overall.top_rated_apps()
    st.dataframe(temp_df)

    fig = px.funnel(temp_df1,x="App", y = "Rating", color="App", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    # Top Reviewed Apps
    st.subheader("Most Reviewed Apps")
    temp_df, temp_df1 = overall.top_reviewed_apps()
    st.dataframe(temp_df)

    fig = px.funnel(temp_df1,x="App", y = "Reviews", color="App", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    # Most Expensive Apps
    st.subheader("Most Expensive Apps")
    temp_df, temp_df1 = overall.most_expensive_apps()
    st.dataframe(temp_df)

    fig = px.funnel(temp_df1,x="App", y = "Price", color="App", width=800, height=500)
    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)
    
    # Free vs Paid
    st.header("Free VS Paid")
    st.subheader("Count")
    temp_df = overall.free_vs_paid_count()
    fig = px.pie(temp_df, names="Type", values = "Count", color ="Type",width = 800, height=500 )
    fig.update_traces(textfont_size=12, textposition="outside")
    fig.update_layout(xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


    col1, col2, col3 = st.columns(3)

    temp_df = overall.free_vs_paid_rating()
    with col1:
        fig = px.funnel(temp_df,x="Type", y = "Rating", color="Type", width=320, height=400,title="Average Rating", color_discrete_sequence=["orange","lightgreen"])
        fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)


    temp_df = overall.free_vs_paid_reviews()
    with col2:
        fig = px.funnel(temp_df,x="Type", y = "Reviews", color="Type", width=320, height=400,title="Average Reviews", color_discrete_sequence=["mediumpurple","red"])
        fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)


    temp_df = overall.free_vs_paid_installs()
    with col3:
        fig = px.funnel(temp_df,x="Type", y = "Installs", color="Type", width=320, height=400,title="Average Installs", color_discrete_sequence=["yellow","dodgerblue"])
        fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
        st.plotly_chart(fig)

    # Average Rating By Category
    st.header("Average Rating By Category")

    selected_type = st.radio("Select By Type", ("Both", "Free", "Paid"))
    temp_df = overall.category_average_rating(selected_type)
    fig = px.funnel(temp_df,x="Rating", y = "Category", color="Category", width=700, height=900)
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Average Reviews By Category
    st.header("Average Reviews By Category")
    temp_df = overall.category_average_reviews(selected_type)
    fig = px.funnel(temp_df,x="Reviews", y = "Category", color="Category", width=700, height=900)
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)

    # Average Installs By Category
    st.header("Average Installs By Category")
    temp_df = overall.category_average_installs(selected_type)
    fig = px.funnel(temp_df,x="Installs", y = "Category", color="Category", width=700, height=900)
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    fig.update_layout(yaxis_title=None,showlegend=False, xaxis_showgrid=False, yaxis_showgrid=False)
    st.plotly_chart(fig)


st.sidebar.header("Contributors")
st.sidebar.markdown("[Sanchi Gandodhar](https://www.linkedin.com/in/sanchi-gandodhar-a497831a9/)")
st.sidebar.markdown("[Aditya Naranje](https://www.linkedin.com/in/anaranje/)")