import numpy as np
from numerize import numerize
import pandas as pd

class Overall_analysis:

    def __init__(self, app_data):
        self.df = app_data

    def top_rated_apps(self):
        quantile = self.df["Reviews"].quantile(0.9)
        self.temp_df = self.df[self.df["Reviews"]>quantile]
        self.temp_df = self.temp_df[["App","Rating"]].groupby("App")["Rating"].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Rating", ascending=False)
        self.temp_df["index"] = np.arange(1,len(self.temp_df)+1)
        self.temp_df.set_index("index", inplace=True)
        self.temp_df1 = self.temp_df.head(10)
        self.temp_df["Rating"] = self.temp_df["Rating"].apply(lambda x:str(x))
        return self.temp_df, self.temp_df1

    def top_reviewed_apps(self):
        self.temp_df = self.df[["App","Reviews"]].groupby("App")["Reviews"].sum().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Reviews", ascending=False)
        self.temp_df["index"] = np.arange(1,len(self.temp_df)+1)
        self.temp_df.set_index("index", inplace=True)
        self.temp_df1 = self.temp_df.head(10)
        self.temp_df["Reviews"] = self.temp_df["Reviews"].apply(lambda x:str(numerize.numerize(x)))
        return self.temp_df, self.temp_df1

    def most_expensive_apps(self):
        self.temp_df = self.df[["App","Price"]].groupby("App")["Price"].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Price", ascending=False)
        self.temp_df["index"] = np.arange(1,len(self.temp_df)+1)
        self.temp_df.set_index("index", inplace=True)
        self.temp_df1 = self.temp_df.head(10)
        self.temp_df["Price"] = self.temp_df["Price"].apply(lambda x:"$ "+str(round(x,2)))
        return self.temp_df, self.temp_df1

    def free_vs_paid_count(self):
        self.temp_df = pd.DataFrame()
        self.temp_df["Type"] = self.df["Type"]
        self.temp_df["Count"] = 1
        return self.temp_df

    def free_vs_paid_rating(self):
        self.temp_df = self.df[["Type","Rating"]].groupby("Type")['Rating'].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index'])
        self.temp_df["Rating"] = self.temp_df["Rating"].apply(lambda x : round(x, 4))
        return self.temp_df

    def free_vs_paid_reviews(self):
        self.temp_df = self.df[["Type","Reviews"]].groupby("Type")['Reviews'].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index'])
        self.temp_df["Reviews"] = self.temp_df["Reviews"].apply(lambda x : int(x))
        return self.temp_df
    
    def free_vs_paid_installs(self):
        self.temp_df = self.df[["Type","Installs"]].groupby("Type")['Installs'].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index'])
        self.temp_df["Installs"] = self.temp_df["Installs"].apply(lambda x : int(x))
        return self.temp_df

    def category_average_rating(self, selected_type):
        if selected_type!="Both":
            self.temp_df = self.df[self.df["Type"]==selected_type]
            self.temp_df = self.temp_df[["Category","Rating"]].groupby("Category")['Rating'].mean().reset_index()
        else:
            self.temp_df = self.df[["Category","Rating"]].groupby("Category")['Rating'].mean().reset_index()
        self.temp_df["Rating"] = self.temp_df["Rating"].apply(lambda x:round(x, 2))
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Rating", ascending=False)
        return self.temp_df

    def category_average_reviews(self, selected_type):
        if selected_type!="Both":
            self.temp_df = self.df[self.df["Type"]==selected_type]
            self.temp_df = self.temp_df[["Category","Reviews"]].groupby("Category")['Reviews'].mean().reset_index()
        else:
            self.temp_df = self.df[["Category","Reviews"]].groupby("Category")['Reviews'].mean().reset_index()
        self.temp_df["Reviews"] = self.temp_df["Reviews"].apply(lambda x:int(x))
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Reviews", ascending=False)
        return self.temp_df

    def category_average_installs(self, selected_type):
        if selected_type!="Both":
            self.temp_df = self.df[self.df["Type"]==selected_type]
            self.temp_df = self.temp_df[["Category","Installs"]].groupby("Category")['Installs'].mean().reset_index()
        else:
            self.temp_df = self.df[["Category","Installs"]].groupby("Category")['Installs'].mean().reset_index()
        self.temp_df["Installs"] = self.temp_df["Installs"].apply(lambda x:int(x))
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Installs", ascending=False)
        return self.temp_df
    

class Category_wise_analysis:

    def __init__(self, app_data, selected_category):
        self.df = app_data[app_data['Category']==selected_category]

    def top_rated_apps(self):
        self.reviews_median = self.df['Reviews'].median()
        self.temp_df = self.df[self.df['Reviews']>self.reviews_median][['App','Category','Rating']]
        self.temp_df = self.temp_df.drop_duplicates(['App', 'Category','Rating'])[['App','Rating']].sort_values(by='Rating', ascending=False)
        indexes = np.arange(1, 11)
        self.temp_df = self.temp_df.head(10).set_index(indexes)
        return self.temp_df

    def top_reviewed_app(self):
        self.temp_df = self.df[['App','Reviews']].drop_duplicates(['App','Reviews']).sort_values(by='Reviews', ascending=False)
        indexes = np.arange(1, 11)
        self.temp_df = self.temp_df.head(10).set_index(indexes)
        return self.temp_df

    def top_expensive_apps(self):
        self.temp_df = self.df[['App','Price']].drop_duplicates(['App','Price']).sort_values(by='Price', ascending=False)
        indexes = np.arange(1, 11)
        self.temp_df = self.temp_df.head(10).set_index(indexes)
        self.temp_df = self.temp_df[self.temp_df["Price"]!=0]
        self.temp_df = self.temp_df.rename(columns={'Price':'Price($)'})
        return self.temp_df

    def max_installed_apps(self):
        self.temp_df = self.df[["App","Installs"]].groupby("App")["Installs"].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Installs", ascending=False).head(10)
        return self.temp_df

    def content_rating(self):
        self.temp_df = pd.DataFrame(self.df['Content Rating'].value_counts()).reset_index()
        self.temp_df.rename(columns={'index':'Content Rating','Content Rating':'Count'}, inplace=True)
        return self.temp_df

    def free_vs_paid_count(self):
        self.temp_df = pd.DataFrame(self.df['Type'].value_counts()).reset_index()
        self.temp_df.rename(columns={'index':'Type','Type':'Count'}, inplace=True)
        return self.temp_df

    def free_vs_paid_rating(self):
        self.temp_df = self.df.groupby(by='Type')['Rating'].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index'])
        return self.temp_df

    def free_vs_paid_reviews(self):
        self.temp_df1 = self.df.groupby(by='Type')['Reviews'].sum().reset_index()
        self.temp_df1.reset_index(inplace=True)
        self.temp_df1 = self.temp_df1.drop(columns=['index'])

        self.temp_df2 = self.df.groupby(by='Type')['Reviews'].mean().reset_index()
        self.temp_df2.reset_index(inplace=True)
        self.temp_df2 = self.temp_df2.drop(columns=['index'])
        self.temp_df2['Reviews'] = self.temp_df2['Reviews'].astype("int")

        return self.temp_df1, self.temp_df2


    def min_android_version(self):
        self.temp_df = pd.DataFrame()
        self.temp_df["Minimum_Android_Version"] = self.df["Minimum Android Ver"]
        self.temp_df["Count"] = 1
        self.temp_df = self.temp_df[self.temp_df["Minimum_Android_Version"]!="-1"]
        return self.temp_df



class Type_wise_analysis:
    
    def __init__(self, app_data, selected_type):
        self.df = app_data[app_data["Type"]==selected_type]

    def top_rated_apps(self):
        q_reviews = self.df["Reviews"].quantile(0.8)
        self.temp_df = self.df[self.df["Reviews"]>q_reviews]
        self.temp_df = self.temp_df[["App","Rating"]].groupby("App")["Rating"].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Rating", ascending=False).head(10)
        return self.temp_df

    def top_reviewed_app(self):
        self.temp_df = self.df[["App","Reviews"]].groupby("App")["Reviews"].sum().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Reviews", ascending=False).head(10)
        return self.temp_df

    def top_expensive_apps(self):
        self.temp_df = self.df[['App','Price']].drop_duplicates(['App','Price']).sort_values(by='Price', ascending=False)
        indexes = np.arange(1, 11)
        self.temp_df = self.temp_df.head(10).set_index(indexes)
        self.temp_df = self.temp_df[self.temp_df["Price"]!=0]
        self.temp_df = self.temp_df.rename(columns={'Price':'Price($)'})
        return self.temp_df


    def max_installed_apps(self):
        self.temp_df = self.df[["App","Installs"]].groupby("App")["Installs"].mean().reset_index()
        self.temp_df.reset_index(inplace=True)
        self.temp_df = self.temp_df.drop(columns=['index']).sort_values("Installs", ascending=False).head(10)
        return self.temp_df

    def content_rating(self):
        self.temp_df = pd.DataFrame(self.df['Content Rating'].value_counts()).reset_index()
        self.temp_df.rename(columns={'index':'Content Rating','Content Rating':'Count'}, inplace=True)
        return self.temp_df

    def min_android_version(self):
        self.temp_df = pd.DataFrame()
        self.temp_df["Minimum_Android_Version"] = self.df["Minimum Android Ver"]
        self.temp_df["Count"] = 1
        self.temp_df = self.temp_df[self.temp_df["Minimum_Android_Version"]!="-1"]
        return self.temp_df