import pandas as pd  
import matplotlib.pyplot as plt  
import numpy as np  
import os  
from datetime import datetime  

def load_stock_data(filepath='data/stock_data.csv'):  
    """Load stock data from CSV or generate sample data."""  
    try:  
        df = pd.read_csv(filepath, parse_dates=['Date'])  
    except FileNotFoundError:  
        print("CSV not found. Using sample data.")  
        dates = pd.date_range(start='2023-01-01', periods=100)  
        prices = 100 + np.cumsum(np.random.randn(100))  
        df = pd.DataFrame({'Date': dates, 'Close': prices})  
    return df  

def analyze_stock(df):  
    """Calculate rolling average and detect peaks/troughs."""  
    df['Rolling_7D'] = df['Close'].rolling(7).mean()  
    df['Peak'] = df['Close'] == df['Close'].rolling(7, center=True).max()  
    df['Trough'] = df['Close'] == df['Close'].rolling(7, center=True).min()  
    return df  

def plot_stock_data(df):  
    """Generate the stock price visualization."""  
    plt.figure(figsize=(12, 6))  
    plt.plot(df['Date'], df['Close'], label='Closing Price', color='#1f77b4', linewidth=2)  
    plt.plot(df['Date'], df['Rolling_7D'], label='7-Day Avg', color='#ff7f0e', linestyle='--')  

    # Highlight peaks & troughs  
    peaks = df[df['Peak']]  
    troughs = df[df['Trough']]  
    plt.scatter(peaks['Date'], peaks['Close'], color='red', label='Peaks', zorder=5)  
    plt.scatter(troughs['Date'], troughs['Close'], color='green', label='Troughs', zorder=5)  

    # Annotate highest/lowest points  
    max_price = df['Close'].max()  
    min_price = df['Close'].min()  
    plt.annotate(f'Max: {max_price:.2f}',  
                 xy=(df.loc[df['Close'].idxmax(), 'Date'], df['Close'].max()),  
                 xytext=(10, 10), textcoords='offset points',  
                 bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),  
                 arrowprops=dict(arrowstyle='->'))  

    plt.title('Stock Price Analysis', fontsize=16, pad=20)  
    plt.xlabel('Date', fontsize=12)  
    plt.ylabel('Price ($)', fontsize=12)  
    plt.legend()  
    plt.grid(True, linestyle='--', alpha=0.6)  
    plt.tight_layout()  

    # Save and show  
    os.makedirs('assets', exist_ok=True)  
    plt.savefig('assets/stock_analysis.png', dpi=120, bbox_inches='tight')  
    plt.show()  

if __name__ == "__main__":  
    df = load_stock_data()  
    df = analyze_stock(df)  
    plot_stock_data(df)