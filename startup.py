import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='StartUp Analysis')
df=pd.read_csv('startup_cleaned.csv')


df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month

def load_overall_analysis():
    st.title('Overall Analysis')
    
    
    
    

def load_investor_details(investor):
    st.title(investor)
    #load the recent 5 investments of the investors
    last5_df = df[df['investors'].str.contains(investor, na=False)].head()[['date', 'startup', 'vertical', 'city', 'round', 'amount']]

    st.subheader('Five Recent Investments')
    st.dataframe(last5_df)

    col1, col2 =st.columns(2)
    with col1:
        #Biggest Investments
        big_inv_series=df[df['investors'].str.contains('investors',na=False)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax=plt.subplots()
        ax.bar(big_inv_series.index,big_inv_series.values)
        st.pyplot(fig)

    with col2:
        vertical_series=df[df['investors'].str.contains('investors',na=False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors invested in')
        fig1, ax1=plt.subplots()
        ax1.pie(vertical_series.values, labels=vertical_series.index, autopct='%0.01f%%')

        st.pyplot(fig1)
    
    col3, col4=st.columns(2)

    with col3:
        round_series=df[df['investors'].str.contains('investors',na=False)].groupby('round')['amount'].sum()
        st.subheader('Rounds')
        fig2, ax2=plt.subplots()
        ax2.pie(round_series.values, labels=round_series.index, autopct='%0.01f%%')

        st.pyplot(fig2)

    with col4:
        city_series=df[df['investors'].str.contains('investors',na=False)].groupby('city')['amount'].sum()
        st.subheader('Invested Cities')
        fig3, ax3=plt.subplots()
        ax3.pie(city_series.values, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

    
    year_series= df[df['investors'].str.contains('investors',na=False)].groupby('year')['amount'].sum()

    st.subheader('YoY Investment')
    fig4, ax4=plt.subplots()
    ax4.plot( year_series.index,  year_series.values)
    st.pyplot(fig4)

    



st.sidebar.title('Startup Funding Analysis')
option=st.sidebar.selectbox('Select category',['Overall Analysis','StartUp','Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()
        col1, col2, col3, col4= st.columns(4)

        #total_invested_amount
        with col1:
            total_amount=round(df['amount'].sum())
            st.metric('Total',str(total_amount)+' Cr')
        
        #maximum amount infuesd ina startup
        with col2:
            max_funding=df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
            st.metric('Maximum Funding',str(max_funding)+' Cr') 
        #avg ticket size
        with col3:
            avg_amount=df.groupby('startup')['amount'].sum().mean()
            st.metric('Average Funding',str(round(avg_amount))+' Cr')

        #total funded startups
        with col4:
            total_startup=df['startup'].nunique()
            st.metric('Funded StartUps',total_startup)

        st.header('MoM Graph')
        selected_option=st.selectbox('Select Type',['Total','Count'])
        if selected_option=='Total':
            temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
        else:
            temp_df=df.groupby(['year','month'])['amount'].count().reset_index()
        
        temp_df['x_axis'] =temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
        
        fig6, ax6= plt.subplots()
        ax6.plot(temp_df['x_axis'],temp_df['amount'])
        st.pyplot(fig6)
elif option == 'StartUp':
    st.sidebar.selectbox('Select startUp',sorted(df['startup'].unique().tolist()))
    btn1=st.sidebar.button('Find StartUp Details')
    st.title('StartUp Analysis')
else:
     selected_investor=st.sidebar.selectbox('Select Investor',sorted(set(item.strip() for sublist in df['investors'].fillna('').str.split(',') for item in sublist)))
     btn2=st.sidebar.button('Find Investor Details')
     if btn2:
         load_investor_details(selected_investor)
         
     