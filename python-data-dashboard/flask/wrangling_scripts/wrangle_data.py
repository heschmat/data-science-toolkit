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

    countries_of_interest = ['United States', 'China', 'Japan', 'Germany',
     'Denmark', 'India', 'France', 'Brazil', 'Russian Federation', 'Canada']

    df = df[df['country_name'].isin(countries_of_interest)]

    # Melt the columns and convert year to date time
    df_melt = df.melt(id_vars = 'country_name', value_vars = value_variables)
    df_melt.columns = ['country', 'year', 'variable']
    df_melt['year'] = pd.to_datetime(df_melt['year']).dt.year



