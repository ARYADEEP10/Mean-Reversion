
# 📈 Mean Reversion Forex Trading Strategy (EUR/USD)  
Automated **Forex trading algorithm** leveraging **mean reversion principles** with **Simple Moving Averages (SMA) and Bollinger Bands**. The strategy is implemented in **Python**, using the **OANDA API** for real-time execution and historical data analysis.

## 🚀 Overview  
This project builds an algorithmic trading strategy for the **EUR/USD currency pair**, based on the idea that prices tend to revert to their mean over time. The model:  
- Uses **SMA (5 day)** and **Bollinger Bands** to identify overbought/oversold conditions.  
- Executes trades automatically using the **OANDA API**.  
- Backtests on **5000 candles** to evaluate performance.  
- Optimizes risk-adjusted returns with dynamic **position sizing and stop-loss mechanisms**.  

## 🔧 Tech Stack  
- **Language:** Python  
- **API:** OANDA (for real-time Forex trading)  
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, OANDA API, Backtester, summaries  

## 📊 Performance Metrics  
- **Return:** 15.23%  
- **Sharpe Ratio:** 1.7  
- **Max Drawdown Reduction:** 2.18%  
- **Trading Frequency:** Daily  

## ⚙️ Installation  
1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/mean-reversion-forex.git
   cd mean-reversion-forex
