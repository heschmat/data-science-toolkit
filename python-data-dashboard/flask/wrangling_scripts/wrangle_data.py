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

    # append all charts to the figures list
    figures = []
    figures.append(dict(data = graph_one, layout = layout_one))

    return figures
