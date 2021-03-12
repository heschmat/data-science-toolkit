import pandas as pd
import plotly.graph_objs as go


def clean_data(data_path, keep_columns = ['country_name', '1990', '2015'],
               value_variables = ['1990', '2015']):
    """Clean world bank data for a visualizaiton dashboard
    """
    df = pd.read_csv(data_path, skiprows= 4)
    # Some cleaning for column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    # Keep only the columns of interest (years and country name)
    df = df[keep_columns]
    # Top 10 economies:
    countries_of_interest = ['United States', 'China', 'Japan', 'Germany',
    'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']

    df = df[df['country_name'].isin(countries_of_interest)]

    # Melt the columns and convert year to date time
    df_melt = df.melt(id_vars = 'country_name', value_vars = value_variables)
    df_melt.columns = ['country', 'year', 'variable']
    df_melt['year'] = pd.to_datetime(df_melt['year']).dt.year
    return df_melt


def return_figures():
    """Creates four plotly visualizations

    Returns:
        list (dict): list containing the plotly visualizations
    """
    # ======================================================================
    # 1. plot arable land from 1990 to 2015 in top10 economies as line chart
    # ======================================================================
    graph_one = []

    df = clean_data('data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv')
    df.columns = ['country','year','hectares_arable_land_perperson']
    df.sort_values('hectares_arable_land_perperson',
                   ascending=False, inplace=True)
    countries = df['country'].unique().tolist()

    for country in countries:
        dfcountry = df[df['country'] == country]
        xval = dfcountry['year'].tolist()
        yval = dfcountry['hectares_arable_land_perperson'].tolist()

        graph_one.append(go.Scatter(
            x = xval, y = yval,
            mode = 'lines',
            name = country
        ))

    layout_one = dict(
        title = 'Change in Hectares Arable Land <br> per Person 1990 to 2015',
        xaxis = dict(
            title = 'year',
            autotick = False,
            tick0 = 1990,
            dtick = 25
        ),
        yaxis = dict(title = 'Hectares')
    )

    # ======================================================================
    # 2. plot ararble land for 2015 as a bar chart
    # ======================================================================
    graph_two = []
    df = clean_data('data/API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2.csv')
    df.columns = ['country','year','hectares_arable_land_perperson']
    df.sort_values('hectares_arable_land_perperson',
                   ascending=False, inplace=True)
    df = df[df['year'] == 2015]

    graph_two.append(go.Bar(
        x = df['country'].tolist(),
        y = df['hectares_arable_land_perperson'].tolist()
    ))

    layout_two = dict(
        title = 'Hectares Arable Land per Person in 2015',
        xaxis = dict(title = 'Country'),
        yaxis = dict(title = 'Hectares per person')
    )

    # ======================================================================
    # 3. plot percent of population that is rural from 1990 to 2015
    # ======================================================================
    graph_three = []

    df = clean_data('data/API_SP.RUR.TOTL.ZS_DS2_en_csv_v2_9948275.csv')
    df.columns = ['country', 'year', 'percent_rural']
    df.sort_values('percent_rural', ascending=False, inplace=True)

    for country in countries:
        dfcountry = df[df['country'] == country]
        xval = dfcountry['year'].tolist()
        yval = dfcountry['percent_rural'].tolist()

        graph_three.append(go.Scatter(
            x = xval, y = yval,
            mode = 'lines',
            name = country
        ))

        layout_three = dict(
            title = 'Change in Rural Population <br> (Percent of Total Population)',
            xaxis = dict(
                title = 'Year',
                autotick = False, tick0 = 1990, dtick = 25
            ),
            yaxis = dict(title = 'Percent')
        )

    # ======================================================================
    # 4. show rural population vs arable land
    # ======================================================================
    graph_four = []

    value_vars = [str(x) for x in range(1995, 2016)]
    keep_columns = [str(x) for x in range(1995, 2016)]
    keep_columns.insert(0, 'country_name')

    df1 = clean_data('data/API_SP.RUR.TOTL_DS2_en_csv_v2_9914824.csv', keep_columns, value_vars)
    df2 = clean_data('data/API_AG.LND.FRST.K2_DS2_en_csv_v2_9910393.csv', keep_columns, value_vars)
    
    df1.columns = ['country', 'year', 'variable']
    df2.columns = ['country', 'year', 'variable']
    
    df = df1.merge(df2, on = ['country', 'year'])

    for country in countries:
        dfcountry = df[df['country'] == country]
        xval = dfcountry['variable_x'].tolist()
        yval = dfcountry['variable_y'].tolist()
        year = dfcountry['year'].tolist()
        country_names = dfcountry['country'].tolist()

        txt = []
        for country, year in zip(country_names, year):
            txt.append(str(country) + '-' + str(year))
    
        graph_four.append(go.Scatter(
            x = xval, y = yval,
            mode = 'markers',
            text = txt,
            name = country,
            textposition = 'middle center'
        ))

    layout_four = dict(
        title = 'Rural Population versus <br> Forested Area (Square Km) 1990-2015',
        xaxis = dict(title = 'Rural Population'),
        yaxis = dict(title = 'Forest Area (square km)')
    )

    # append all charts to the figures list
    figures = []
    figures.append(dict(data = graph_one, layout = layout_one))
    figures.append(dict(data = graph_two, layout = layout_two))
    figures.append(dict(data = graph_three, layout = layout_three))
    figures.append(dict(data = graph_four, layout = layout_four))

    return figures
