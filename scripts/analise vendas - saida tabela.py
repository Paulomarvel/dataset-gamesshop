#A seguir, apresento uma solução em Python usando o pandas que, após ler e unificar os três arquivos CSV, gera duas tabelas:
#
#Tabela Resumo – com o produto mais vendido (e sua quantidade total), o site com maior volume de vendas (e sua quantidade) e o país (delivery_country) com mais vendas (e sua quantidade).
#Tabela de Percentual de Vendas por Produto em Cada País – onde, para cada país, é calculado o percentual que cada produto representa do total de vendas naquele país.
#Você pode usar o código abaixo como referência:

import pandas as pd

# 1. Leitura dos arquivos CSV
df_aliexpress = pd.read_csv("Meganium_Sales_Data_-_AliExpress.csv")
df_etsy       = pd.read_csv("Meganium_Sales_Data_-_Etsy.csv")
df_shopee     = pd.read_csv("Meganium_Sales_Data_-_Shopee.csv")

# 2. Unificação dos dados (garanta que os nomes das colunas sejam consistentes entre os arquivos)
df = pd.concat([df_aliexpress, df_etsy, df_shopee], ignore_index=True)

# 3. Produto mais vendido e sua quantidade total
grouped_products = df.groupby('product_sold')['quantity'].sum()
top_product = grouped_products.idxmax()     # Nome do produto
top_quantity = grouped_products.max()         # Quantidade total vendida

# 4. Percentual de cada produto por delivery_country
#    a) Agrupa por país e produto para somar as quantidades
country_product = df.groupby(['delivery_country', 'product_sold'])['quantity'].sum().reset_index()

#    b) Calcula o total de vendas por país
country_total = df.groupby('delivery_country')['quantity'].sum().reset_index().rename(columns={'quantity': 'total_country'})

#    c) Junta as duas informações
merged = pd.merge(country_product, country_total, on='delivery_country')

#    d) Calcula o percentual
merged['percent'] = (merged['quantity'] / merged['total_country']) * 100
merged['percent'] = merged['percent'].round(2)  # Arredonda para duas casas decimais

# 5. Site com maior volume de vendas
site_sales = df.groupby('site')['quantity'].sum()
top_site = site_sales.idxmax()        # Nome do site
top_site_quantity = site_sales.max()    # Quantidade total vendida no site

# 6. País com mais vendas (delivery_country)
country_sales = df.groupby('delivery_country')['quantity'].sum()
top_country = country_sales.idxmax()        # País com mais vendas
top_country_quantity = country_sales.max()    # Quantidade total de vendas no país

# 7. Montar a Tabela Resumo
summary = pd.DataFrame({
    "Métrica": [
        "Produto mais vendido",
        "Quantidade total do produto",
        "Site com maior volume de vendas",
        "Quantidade total do site",
        "País com mais vendas",
        "Quantidade total do país"
    ],
    "Resultado": [
        top_product,
        top_quantity,
        top_site,
        top_site_quantity,
        top_country,
        top_country_quantity
    ]
})

# Exibir as tabelas
print("Tabela Resumo:")
print(summary)
print("\nTabela de Percentual de Vendas por Produto em Cada País:")
print(merged)
