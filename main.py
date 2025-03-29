import yfinance as yf
import pandas as pd
from sklearn.preprocessing import StandardScaler
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Load the historical price data
price_df = pd.read_csv('historical_prices2.csv', index_col='Date', parse_dates=True)

# Load the normalized fundamental data
fundamental_df = pd.read_csv('normalized_fundamental_data1.csv', index_col=0)

# Define asset classes
asset_classes = {
    'Stocks': ['AAPL', 'MSFT', 'GOOGL', 'JNJ', 'PFE', 'JPM', 'BAC', 'KO', 'PEP', 'XOM', 'CVX', 'AMZN', 'META', 
               'TSLA', 'BRK-B', 'V', 'WMT', 'PG', 'DIS', 'MA', 'NVDA', 'HD', 'PYPL', 'UNH', 'VZ', 'ADBE', 
               'NFLX', 'CMCSA', 'INTC', 'MRK', 'ABT', 'ABBV', 'T', 'CSCO', 'NKE', 'MCD', 'MDT', 'HON', 
               'AMGN', 'BA', 'SBUX', 'CAT', 'IBM', 'MMM', 'GE', 'RTX', 'GS', 'USB', 'BLK', 'BK', 'SCHW', 
               'C', 'MS', 'WFC', 'AXP', 'SPGI', 'ADP', 'MSCI', 'ICE', 'TROW', 'COF', 'AFL', 'MET', 'PRU', 
               'LNC', 'COST', 'ORCL', 'ACN', 'CRM', 'TXN', 'AVGO', 'QCOM'],
    'ETFs': ['VOO', 'IVV', 'SPY', 'IWM', 'VUG', 'VTV', 'QQQ', 'DIA', 'VOE', 'VBR', 'VB', 'MTUM', 'QUAL', 'VLUE', 
             'EFG', 'EFV', 'IEFA', 'IEMG', 'EEM', 'SPYX', 'ICLN'],
    'Commodities': ['GLD', 'USO', 'SLV'],
    'Cryptocurrencies': ['BTC-USD', 'ETH-USD'],
    'Bonds': ['LQD'],
    'Indices': ['^TNX'],
    'Real Estate': ['VNQ']
}

# Create a reverse mapping from assets to their classes
asset_to_class = {asset: asset_class for asset_class, assets in asset_classes.items() for asset in assets}

# Define colors for each asset class (better visibility on white background)
colors = {
    'Stocks': '#1f77b4',        # Blue
    'ETFs': '#ff7f0e',          # Orange
    'Commodities': '#2ca02c',   # Green
    'Cryptocurrencies': '#d62728', # Red
    'Bonds': 'purple',          # Keeping original color as it's already distinct
    'Indices': 'brown',         # Keeping original color as it's already distinct
    'Real Estate': 'pink'       # Keeping original color as it's already distinct
}

def preprocess_data(price_df):
    # Fill missing values by forward fill method
    price_df.ffill(inplace=True)

    # Calculate returns from price data
    returns_df = price_df.pct_change().dropna()
    returns_df.to_csv('returns.csv')

    return returns_df

def create_graph(returns_df, fundamental_df, threshold=0.5):
    # Calculate the correlation matrix from returns data
    correlation_matrix = returns_df.corr()

    # Create the graph
    G = nx.Graph()

    # Add nodes
    for asset in returns_df.columns:
        G.add_node(asset)

    # Add edges based on correlation threshold
    for i in range(len(correlation_matrix)):
        for j in range(i+1, len(correlation_matrix)):
            if abs(correlation_matrix.iloc[i, j]) > threshold:
                G.add_edge(correlation_matrix.columns[i], correlation_matrix.columns[j], weight=1 - abs(correlation_matrix.iloc[i, j]))

    # Add fundamental data as node attributes
    for asset in G.nodes:
        if asset in fundamental_df.index:
            for column in fundamental_df.columns:
                G.nodes[asset][column] = fundamental_df.loc[asset, column]

    return G

def create_mst(G):
    mst = nx.minimum_spanning_tree(G, weight='weight')
    return mst

def analyze_and_plot_graph(G, title, asset_to_class, colors, zoom=False, centrality_threshold=0.1):
    centrality = nx.degree_centrality(G)
    pos = nx.spring_layout(G, k=0.15, iterations=100)

    if zoom:
        # Filter nodes based on centrality threshold
        filtered_nodes = [node for node, cent in centrality.items() if cent > centrality_threshold]
        G = G.subgraph(filtered_nodes)
        centrality = {node: cent for node, cent in centrality.items() if node in filtered_nodes}
        pos = nx.spring_layout(G, k=0.15, iterations=100)

    fig, ax = plt.subplots(figsize=(18, 18))
    node_colors = [colors[asset_to_class[node]] for node in G.nodes]
    node_sizes = [v * 2000 for v in centrality.values()]
    nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, alpha=0.9, edgecolors='k', linewidths=0.5, ax=ax)
    edges = nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=ax)
    labels = nx.draw_networkx_labels(G, pos, font_size=10, ax=ax, font_color='black', font_weight='bold')
    
    if not zoom:
        # Annotate edges with their weights for the full graph
        edge_labels = nx.get_edge_attributes(G, 'weight')
        formatted_edge_labels = {k: f"{v:.2f}" for k, v in edge_labels.items()}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=formatted_edge_labels, font_color='red', ax=ax)
    
    ax.set_title(title, fontsize=20)
    plt.axis('off')
    
    plt.show()

# Enable interactive mode
plt.ion()

# Preprocess data
returns_df = preprocess_data(price_df)

# Create and analyze graph
G = create_graph(returns_df, fundamental_df)
analyze_and_plot_graph(G, "Original Graph", asset_to_class, colors)

# Zoom into the main cluster by focusing on nodes with high centrality
analyze_and_plot_graph(G, "Zoomed Main Cluster", asset_to_class, colors, zoom=True, centrality_threshold=0.1)

# Create and analyze MST
mst = create_mst(G)
analyze_and_plot_graph(mst, "Minimum Spanning Tree", asset_to_class, colors)

# Keep the plots open for interaction
plt.ioff()
plt.show()
