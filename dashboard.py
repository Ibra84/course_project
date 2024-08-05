import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import duckdb

# Инициализация Dash приложения
app = dash.Dash(__name__)

# Функция для получения данных из DuckDB
def get_data_from_db(query):
    conn = duckdb.connect('my.db')
    df = conn.execute(query).fetchdf()
    conn.close()
    return df

# Загрузка данных
products_df = get_data_from_db("SELECT * FROM products")
regions_df = get_data_from_db("SELECT * FROM regions")
sales_df = get_data_from_db("SELECT * FROM sales")

# Создание графиков
def create_charts(filtered_sales_df=None):
    # График продаж по продуктам
    sales_by_product = sales_df.merge(products_df, on='product_id')
    fig_sales_by_product = px.bar(
        sales_by_product,
        x='product_name',
        y='amount',
        title='Sales by Product'
    )
    
    # График продаж по регионам
    fig_sales_by_region = px.pie(
        values=[],
        names=[],
        title='Sales by Region'
    )
    
    # График продаж по времени
    if filtered_sales_df is not None:
        filtered_sales_df.loc[:, 'date'] = pd.to_datetime(filtered_sales_df['date'])
        fig_sales_over_time = px.line(
            filtered_sales_df,
            x='date',
            y='amount',
            title='Sales Over Time'
        )
    else:
        fig_sales_over_time = px.line(
            x=[],
            y=[],
            title='Sales Over Time'
        )
    
    # График топ-5 продуктов по объему продаж
    if filtered_sales_df is not None:
        top_products = filtered_sales_df.groupby('product_id').agg({'amount': 'sum'}).reset_index()
        top_products = top_products.merge(products_df, on='product_id')
        top_products = top_products.nlargest(5, 'amount')
        fig_top_products = px.bar(
            top_products,
            x='product_name',
            y='amount',
            title='Top 5 Products by Sales Volume'
        )
    else:
        fig_top_products = px.bar(
            x=[],
            y=[],
            title='Top 5 Products by Sales Volume'
        )

    return fig_sales_by_product, fig_sales_by_region, fig_sales_over_time, fig_top_products

# Создание дашборда
app.layout = html.Div([
    html.H1('Sales Dashboard'),
    
    # Элементы управления фильтрацией
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': name, 'value': id} for id, name in products_df[['product_id', 'product_name']].values],
        value=products_df['product_id'].iloc[0]
    ),
    dcc.Dropdown(
        id='region-dropdown',
        options=[{'label': name, 'value': id} for id, name in regions_df[['region_id', 'region_name']].values],
        value=regions_df['region_id'].iloc[0]
    ),
    
    # Графики
    dcc.Graph(id='sales-by-product'),
    dcc.Graph(id='sales-by-region'),
    dcc.Graph(id='sales-over-time'),
    dcc.Graph(id='top-products')
])

# Обработчик для обновления графиков на основе фильтров
@app.callback(
    [Output('sales-by-product', 'figure'),
     Output('sales-by-region', 'figure'),
     Output('sales-over-time', 'figure'),
     Output('top-products', 'figure')],
    [Input('product-dropdown', 'value'),
     Input('region-dropdown', 'value')]
)
def update_charts(selected_product, selected_region):
    # Фильтрация данных по выбранному региону
    filtered_sales_df = sales_df[sales_df['region_id'] == selected_region]
    
    # Обновление графиков
    fig_sales_by_product, fig_sales_by_region, fig_sales_over_time, fig_top_products = create_charts(filtered_sales_df)
    
    # Обновление данных в графиках на основе фильтров
    fig_sales_by_product.update_traces(
        selector=dict(type='bar'),
        x=products_df['product_name'],
        y=filtered_sales_df.groupby('product_id')['amount'].sum().values
    )
    
    # Рассчитываем проценты
    total_sales_in_region = filtered_sales_df['amount'].sum()
    selected_product_sales = filtered_sales_df[filtered_sales_df['product_id'] == selected_product]['amount'].sum()
    other_products_sales = total_sales_in_region - selected_product_sales
    
    # Получаем имя выбранного продукта
    selected_product_name = products_df[products_df['product_id'] == selected_product]['product_name'].values[0]
    
    fig_sales_by_region = px.pie(
        values=[selected_product_sales, other_products_sales],
        names=[selected_product_name, 'Other Products'],
        title='Sales Percentage in Region'
    )
    
    fig_sales_over_time.update_traces(
        selector=dict(type='line'),
        x=filtered_sales_df['date'],
        y=filtered_sales_df['amount']
    )
    
    return fig_sales_by_product, fig_sales_by_region, fig_sales_over_time, fig_top_products

# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)
