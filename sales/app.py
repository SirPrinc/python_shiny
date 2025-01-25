from pathlib import Path
import pandas as pd
import calendar


import plotly.express as px
from shiny import reactive
from shiny.express import render, input, ui
from shinywidgets import render_plotly

ui.page_opts(title="Sales Dashboard - video 1 of 5", fillable=True)

ui.input_numeric("n", label="Number of products to show", value=5, min=0, max=20)

@reactive.calc
def dat():
    infile = Path(__file__).parent / "data" / "sales.csv"
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    return df


# @render_plotly
# def plot1():
#     df = dat()
#     top_sales = df.groupby("product")['quantity_ordered'].sum().nlargest(input.n()).reset_index()
#     return px.bar(top_sales, x = 'product', y = 'quantity_ordered', title = f'Top {input.n()} products by quantity sold')
    
ui.input_selectize(
    "city",
    "Select a City",
    ['Dallas (TX)', 'Boston (MA)', 'Los Angeles (CA)', 'San Francisco (CA)', 'Seattle (WA)', 'Atlanta (GA)', 'New York City (NY)', 'Portland (OR)', 'Austin (TX)', 'Portland (ME)'],
    multiple=True
)


@render_plotly
def sales_over_time():
    df = dat()
    sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
    months_orders = calendar.month_name[1:]
    fig = px.bar(sales, x = 'month', y = 'quantity_ordered', color = 'city',category_orders={'month': months_orders}, title = 'Sales over time by city')
    return fig


with ui.card():
    ui.card_header("Sample Sales Data")
    @render.data_frame
    def sample_sales_data():
        return dat().head(10)
