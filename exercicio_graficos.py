import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Carregar os dados
df = pd.read_csv('C:/Users/Matheus/Desktop/curso/ecommerce_preparados.csv')

# Exibir informações básicas do DataFrame
df.info()

# Verificar valores ausentes
print("Valores ausentes por coluna:")
print(df.isnull().sum())

# Gráfico de dispersão entre 'Preço' e 'Qtd_Vendidos_Cod'
plt.figure(figsize=(10, 6))  # Ajustar o tamanho da figura
sns.scatterplot(x='Preço', y='Qtd_Vendidos_Cod', data=df)
plt.title('Dispersão entre Preço e Quantidade Vendida')
plt.show()

# Selecionar apenas colunas numéricas
numeric_df = df.select_dtypes(include=['number'])
print("\nColunas numéricas selecionadas para análise:")
print(numeric_df.columns)

# Calcular a matriz de correlação
correlation_matrix = numeric_df.corr()

# Criar o mapa de calor de correlação
plt.figure(figsize=(12, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".2f", cmap='coolwarm', square=True, cbar_kws={"shrink": .8})
plt.title('Mapa de Calor da Correlação entre Variáveis')
plt.show()

# Converter para minúsculas e remover espaços ao redor
df['Gênero'] = df['Gênero'].str.lower().str.strip()

# Verificar valores únicos após a padronização
print(df['Gênero'].unique())

# Dicionário de mapeamento para agrupar gêneros semelhantes
mapa_genero = {
    'masculino': 'masculino',
    'bebês': 'bebês',
    'meninos': 'infantil',
    'menino': 'infantil',
    'bermuda feminina brilho blogueira': 'feminino',
    'meninas': 'infantil',
    'roupa para gordinha pluss p ao 52': 'feminino',
    'short menina verao look mulher': 'feminino',
    'feminino': 'feminino',
    'mulher': 'feminino',
    'sem gênero': 'sem gênero',
    'unissex': 'sem gênero',
    'sem gênero infantil': 'infantil'}

# Aplicar o mapeamento
df['Gênero'] = df['Gênero'].replace(mapa_genero)

# Verificar os valores únicos após o mapeamento
print(df['Gênero'].unique())

# Calcular a quantidade total vendida por gênero
quantidade_vendida_por_genero = df.groupby('Gênero')['Qtd_Vendidos_Cod'].sum().reset_index()

# Criar o gráfico de barras para a quantidade vendida por gênero
plt.figure(figsize=(14, 8))  # Aumentar o tamanho da figura
bar_plot = sns.barplot(x='Gênero', y='Qtd_Vendidos_Cod', data=quantidade_vendida_por_genero, hue='Gênero', palette='muted', legend=False)

# Adicionar título e rótulos aos eixos
plt.title('Quantidade Vendida por Gênero')
plt.xlabel('Gêneros')
plt.ylabel('Quantidade Vendida')

# Rotacionar rótulos do eixo x e ajustar o tamanho da fonte
plt.xticks(rotation=45, fontsize=10)

# Adicionar anotações com os valores acima das barras
for p in bar_plot.patches:
    bar_plot.annotate(format(p.get_height(), '.0f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center', va='bottom', fontsize=10)

# Ajustar o layout manualmente
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.3)

# Exibir o gráfico
plt.show()

# Verificar o tipo de dado da coluna 'Qtd_Vendidos'
print("\nTipo de dado da coluna 'Qtd_Vendidos_Cod':")
print(df['Qtd_Vendidos_Cod'].dtype)

# Remover valores ausentes na coluna 'Material' e 'Qtd_Vendidos_Cod'
df = df.dropna(subset=['Material', 'Qtd_Vendidos_Cod'])

# Dicionário de mapeamento para agrupar materiais semelhantes
mapa_material = {
    'algodão cotton': 'algodão',
    'jean': 'jeans',
    'jeans que estica muito': 'jeans',
}

# Aplicar o mapeamento, se necessário
df['Material'] = df['Material'].replace(mapa_material)

# Calcular a quantidade total vendida por material
quantidade_vendida_por_material = df.groupby('Material')['Qtd_Vendidos_Cod'].sum().reset_index()

# Calcular a quantidade total vendida
total_vendas = quantidade_vendida_por_material['Qtd_Vendidos_Cod'].sum()

# Calcular a porcentagem de cada material em relação ao total
quantidade_vendida_por_material['Porcentagem'] = (quantidade_vendida_por_material['Qtd_Vendidos_Cod'] / total_vendas) * 100

# Filtrar materiais com porcentagem superior a 1%
quantidade_vendida_por_material = quantidade_vendida_por_material[quantidade_vendida_por_material['Porcentagem'] > 1]

# Criar um gráfico de pizza para a quantidade vendida por material
plt.figure(figsize=(10, 8))
plt.pie(quantidade_vendida_por_material['Qtd_Vendidos_Cod'],
        labels=quantidade_vendida_por_material['Material'],
        autopct='%1.1f%%',
        startangle=140)
plt.title('Quantidade Vendida por Material (Apenas Materiais com Mais de 1%)')
plt.axis('equal')
plt.show()

# Remover valores negativos
df_clean = df[df['Qtd_Vendidos_Cod'] >= 0]

#grafico de densidade
plt.figure(figsize=(12, 6))
sns.histplot(df_clean['Qtd_Vendidos_Cod'], bins=30, kde=True, color='blue', stat="density", alpha=0.5)
plt.title('Histograma de Quantidade Vendida com Curva de Densidade')
plt.xlabel('Quantidade Vendida')
plt.ylabel('Densidade')
plt.grid()
plt.show()
