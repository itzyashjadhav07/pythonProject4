import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("startup_cleaned.csv")
st.set_page_config(layout='wide', page_title='Startup Analysis')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
def load_investor_details(investor):
    st.title(investor)

    # most recent investments
    st.subheader('Most Recent Investments')
    last5_df = df[df['investors'].str.contains(investor, na=False)].head(5)[
        ['date', 'startup', 'vertical', 'city', 'round', 'amount']]
    st.dataframe(last5_df)

    # max investments
    st.subheader('Maximum Investment')
    max_investment = df[df['investors'].str.contains(investor, na=False)]['amount'].max()
    st.write(f"The maximum investment by {investor} is: {max_investment}")



    fig_size = (8, 6)
    col1, col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        fig, ax = plt.subplots(figsize=fig_size)
        ax.bar(big_series.index, big_series.values)
        plt.xticks(rotation=45)
        plt.ylabel('Amount')
        st.pyplot(fig)

    with col2:
        fig_size = (10, 6)
        # Your existing code
        dates = df[df['investors'].str.contains(investor, na=False)].groupby('date')['amount'].sum().sort_index()
        st.subheader("Investment Trend Over Time(DATES)")
        fig, ax = plt.subplots(figsize=fig_size)
        ax.bar(dates.index, dates.values, width=0.8, linewidth=2)  # Adjust the linewidth as needed
        plt.xticks(rotation=45)
        plt.ylabel('Amount')
        ax.grid(True, linestyle='--', alpha=0.8)
        st.pyplot(fig)


    col3, col4 = st.columns(2)
    with col3:
        vertical = df[df['investors'].str.contains(investor, na=False)].groupby('vertical')[
            'amount'].sum().sort_values()
        st.subheader('Sectors Invested in')
        fig1, ax1 = plt.subplots(figsize=fig_size)
        ax1.pie(vertical, labels=vertical.index, autopct="%0.01f%%")
        st.pyplot(fig1)

    with col4:
        city = df[df['investors'].str.contains(investor, na=False)].groupby('city').size().sort_values()
        st.subheader('Investments by City')
        fig2, ax2 = plt.subplots(figsize=fig_size)
        ax2.pie(city, labels=city.index, autopct="%0.01f%%")
        st.pyplot(fig2)



    col5, col6 = st.columns(2)
    with col5:
        rounds = df[df['investors'].str.contains(investor, na=False)].groupby(['round']).size().sort_values()
        st.subheader('By Rounds ')
        fig3, ax3 = plt.subplots(figsize=fig_size)
        ax3.pie(rounds, labels=rounds.index, autopct="%0.01f%%")
        st.pyplot(fig3)

    with col6:
        df['year'] = pd.to_datetime(df['date']).dt.year
        year = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
        st.subheader('Yearly Investment')
        fig4, ax4 = plt.subplots(figsize=fig_size)
        ax4.plot(year.index, year.values, marker='o', linestyle='-')
        plt.xlabel('Year')
        plt.ylabel('Amount')
        ax4.grid(True, linestyle='--', alpha=0.5)
        st.pyplot(fig4)


def Overall():
    df = pd.read_csv('startup_cleaned.csv')
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.year
    total = round(df['amount'].sum())

    # Max amount
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # Avg amount
    avg_funding = df.groupby('startup')['amount'].sum().mean()


    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total',str(total) + 'Cr')
    with col2:
        st.metric('Max',str(max_funding)+'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding))+'Cr')
    with col4:
        st.metric('Founded Startups',num_startups)

    # mom graph
    st.title('MoM Graph')
    selected_option = st.selectbox('select type',['total','count'])
    if selected_option == 'total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()
    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig3,ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'],temp_df['amount'])
    st.pyplot(fig3)


    # Sector Analysis
    st.title('Sector Analysis')
    st.write("Top 3 Verticals")
    top_verticals = df['vertical'].value_counts().head(3)
    fig, ax = plt.subplots()
    top_verticals.plot(kind='pie', ax=ax)
    st.pyplot(fig)


    # city wise funding
    st.title('City Wise Funding')
    # Group by city and sum the investment amounts, filling missing values with 0
    total_investment_by_city = df.groupby('city')['amount'].sum().fillna(0)
    # Sorting the result by total investment amount
    total_investment_by_city = total_investment_by_city.sort_values(ascending=False)
    # Resetting index to make city a column again
    total_investment_by_city = total_investment_by_city.reset_index()



    # Plotting a pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(total_investment_by_city['amount'], labels=total_investment_by_city['city'], autopct='%1.1f%%')
    ax.set_title('Total Investment by City')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Displaying the plot
    st.pyplot(fig)
    # Group by investors and find the maximum investment amount for each investor
    investor_max_amount = df.groupby('investors')['amount'].max().sort_values(ascending=False).head(10)




    # Sector Analysis
    st.subheader("Top Startups -> yearwise")
    # Grouping data by year and startup, summing the funding amount for each startup in each year
    yearly_startup = df.groupby(['year', 'startup'])['amount'].sum().reset_index()
    # Sorting values to find the top startup in each year based on funding amount
    sorted_values = yearly_startup.sort_values(by=['year', 'amount'], ascending=[True, False])
    top_startup = sorted_values.groupby('year').head(1).reset_index(drop=True)
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(8, 8))
    labels = [f"{row['year']} - {row['startup']}" for _, row in top_startup.iterrows()]
    ax.pie(top_startup['amount'], labels=labels, autopct='%1.1f%%')
    ax.set_title('Total startups yearwise')
    ax.axis('equal')
    # Displaying the plot in Streamlit
    st.pyplot(fig)




    # top investors
    st.title("Top Investors ")
    # Aggregate investment amounts for each investor
    investor_totals = df.groupby('investors')['amount'].sum().reset_index()
    # Rank investors based on total investment amount
    investor_totals = investor_totals.sort_values(by='amount', ascending=False)
    # Select top investors (e.g., top 10)
    top_investors = investor_totals.head(10)
    # Plotting the pie chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(top_investors['amount'], labels=top_investors['investors'], autopct='%1.1f%%')
    ax.set_title('Top Investors')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)



    st.title('Funding Heatmap')
    st.write('Just a moment if it take long time 🙏🙏')
    # Pivot the DataFrame to create a matrix suitable for a heatmap
    heatmap_data = df.pivot_table(index='startup', columns='year', values='amount', aggfunc='sum', fill_value=0)
    # Create a heatmap using Seaborn
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(heatmap_data, cmap='YlGnBu', annot=True, fmt=".0f", linewidths=.5, ax=ax)
    # Set plot title
    ax.set_title('Funding Heatmap by Startup and Year')
    # Show the plot in Streamlit
    st.pyplot(fig)


def startup(startup):
    # giving title

    st.title(startup)
    # Assuming startup variable holds the name of the startup
    st.header('Founders:')
    # Filter the DataFrame to select rows where the 'startup' column
    a = df[df['startup'] == startup]
    # Print the names of investors in the startup
    b = a['investors']
    # Create a DataFrame from the 'investors' column
    investors_df = pd.DataFrame(b, columns=['investors']).reset_index()
    # Display the DataFrame
    st.write(investors_df)



    st.header('Industry:')
    st.write('By amount')
    # Filter the DataFrame to select rows where the 'startup'
    a = df[df['startup'] == startup]
    # Aggregate funding amounts by sector
    sector_funding = a.groupby('vertical')['amount'].sum().reset_index()
    # Display the aggregated funding amounts by sector as a DataFrame
    st.write(sector_funding)


    # Filter the DataFrame to select rows where the 'startup'
    a = df[df['startup'] == startup]
    # Aggregate funding amounts by sector
    sector_funding = a.groupby('vertical')['amount'].sum()
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(sector_funding, labels=sector_funding.index, autopct='%1.1f%%')
    ax.set_title('Funding Distribution by Sector ')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)




    st.header('Subindustry:')
    st.write('By amount:')
    # Filter the DataFrame to select rows where the 'startup'
    shuttl_df = df[df['startup'] == startup]
    # Aggregate funding amounts by subvertical
    sector_funding = shuttl_df.groupby('subvertical')['amount'].sum().reset_index()
    # Display the aggregated funding amounts by subvertical as a DataFrame
    st.write(sector_funding)


    # Filter the DataFrame to select rows where the 'startup'
    shuttl_df = df[df['startup'] == startup]
    # Aggregate funding amounts by sector
    sector_funding = shuttl_df.groupby('subvertical')['amount'].sum()
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(sector_funding, labels=sector_funding.index, autopct='%1.1f%%')
    # ax.set_title('Funding Distribution by Sector ')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)



    st.header('Location:')
    st.write('By amount:')
    # Filter the DataFrame to select rows where the 'startup' column equals the specified startup
    startup_df = df[df['startup'] == startup]
    # Remove NaN values from the 'city' column
    startup_df = startup_df.dropna(subset=['city'])
    # Extract unique cities and aggregate funding amounts by city
    city_funding = startup_df.groupby('city')['amount'].sum().reset_index()
    # Display the aggregated funding amounts by city in a DataFrame
    st.dataframe(city_funding)

    # Filter the DataFrame to select rows where the 'startup' column equals the specified startup
    startup_df = df[df['startup'] == startup]
    # Remove NaN values from the 'city' column
    startup_df = startup_df.dropna(subset=['city'])
    # Extract unique cities and aggregate funding amounts by city
    city_funding = startup_df.groupby('city')['amount'].sum()
    # Plotting the pie chart
    fig, ax = plt.subplots()
    ax.pie(city_funding, labels=city_funding.index, autopct='%1.1f%%')
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    # Display the pie chart using Streamlit
    st.pyplot(fig)

    st.subheader('Funding Rounds:')
    funding_rounds_info = df[['round', 'investors', 'date']].sort_values('date', ascending=False)
    st.dataframe(funding_rounds_info)





st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])
st.markdown("""
### my favourite movies
- Aditya kale
- Fw23ai001
 """)
if option == 'Overall Analysis':
    st.title('Overall Analysis')
    Overall()
elif option == 'Startup':
    st.title("Startup Analysis")

    startup2 = st.sidebar.selectbox('Select One', df['startup'].unique().tolist())
    btn1 = st.sidebar.button('Find Startup Details')
    if btn1:

        startup(startup2)

else:
    st.title('Investor')
    selected_investor = st.sidebar.selectbox('Select One',
                                             sorted(set(df['investors'].astype(str).str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investors Details')
    if btn2:
        load_investor_details(selected_investor)