#!/usr/bin/env python3
"""
Alpaca Day Trading Bot
Strategy: High volatility stocks/ETFs with solid P/E ratios
"""
import json
import requests
import time
from datetime import datetime

class AlpacaTrader:
    def __init__(self, creds_path='/Users/administrator/.openclaw/credentials/alpaca-paper.json'):
        with open(creds_path) as f:
            self.creds = json.load(f)
        
        self.base_url = self.creds['baseUrl']
        self.headers = {
            'APCA-API-KEY-ID': self.creds['apiKey'],
            'APCA-API-SECRET-KEY': self.creds['secretKey']
        }
        
        # Trading parameters
        self.max_position_size = 500  # $500 max per trade
        self.stop_loss_pct = 0.20  # 20% stop loss
        self.target_profit_pct = 0.10  # 10% profit target (configurable)
        
    def get_account(self):
        """Get account information"""
        response = requests.get(f"{self.base_url}/v2/account", headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_positions(self):
        """Get current positions"""
        response = requests.get(f"{self.base_url}/v2/positions", headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_market_status(self):
        """Check if market is open"""
        response = requests.get(f"{self.base_url}/v2/clock", headers=self.headers)
        if response.status_code == 200:
            clock = response.json()
            return clock['is_open']
        return False
    
    def screen_stocks(self, min_pe=5, max_pe=30, min_volume=1000000):
        """
        Screen for stocks with:
        - Good P/E ratios (5-30)
        - High volume (liquidity)
        - High volatility
        """
        # Get list of active assets
        response = requests.get(
            f"{self.base_url}/v2/assets",
            headers=self.headers,
            params={
                'status': 'active',
                'asset_class': 'us_equity'
            }
        )
        
        if response.status_code != 200:
            return []
        
        assets = response.json()
        # Filter for tradable, shortable stocks
        candidates = [a for a in assets if a['tradable'] and a['shortable']]
        
        # TODO: Add fundamental screening (P/E, volume, volatility)
        # For now, return a sample of liquid stocks
        return candidates[:50]  # Return top 50 candidates
    
    def place_order(self, symbol, qty=None, notional=None, side='buy'):
        """
        Place a market order
        side: 'buy' or 'sell'
        qty: number of shares
        notional: dollar amount (use this for $500 max)
        """
        order_data = {
            'symbol': symbol,
            'side': side,
            'type': 'market',
            'time_in_force': 'day'
        }
        
        if notional:
            order_data['notional'] = notional
        elif qty:
            order_data['qty'] = qty
        else:
            return None
        
        response = requests.post(
            f"{self.base_url}/v2/orders",
            headers=self.headers,
            json=order_data
        )
        
        return response.json() if response.status_code in [200, 201] else None
    
    def set_stop_loss(self, symbol, qty, entry_price):
        """Set stop loss order at 20% below entry"""
        stop_price = round(entry_price * (1 - self.stop_loss_pct), 2)
        
        order_data = {
            'symbol': symbol,
            'qty': qty,
            'side': 'sell',
            'type': 'stop',
            'time_in_force': 'day',
            'stop_price': stop_price
        }
        
        response = requests.post(
            f"{self.base_url}/v2/orders",
            headers=self.headers,
            json=order_data
        )
        
        return response.json() if response.status_code in [200, 201] else None
    
    def monitor_positions(self):
        """Monitor and manage open positions"""
        positions = self.get_positions()
        
        print(f"\n📊 Current Positions: {len(positions)}")
        for pos in positions:
            symbol = pos['symbol']
            qty = float(pos['qty'])
            entry_price = float(pos['avg_entry_price'])
            current_price = float(pos['current_price'])
            unrealized_pl = float(pos['unrealized_pl'])
            unrealized_plpc = float(pos['unrealized_plpc'])
            
            print(f"{symbol}: {qty} shares @ ${entry_price:.2f} | "
                  f"Current: ${current_price:.2f} | "
                  f"P/L: ${unrealized_pl:.2f} ({unrealized_plpc*100:.2f}%)")
            
            # Take profit if hit target
            if unrealized_plpc >= self.target_profit_pct:
                print(f"  ✓ Taking profit on {symbol}")
                self.place_order(symbol, qty=int(qty), side='sell')
        
        return positions
    
    def run_status(self):
        """Print current status"""
        account = self.get_account()
        if not account:
            print("❌ Failed to connect to Alpaca")
            return
        
        print("\n" + "="*60)
        print("🤖 ALPACA DAY TRADING BOT")
        print("="*60)
        print(f"Account: {account['account_number']}")
        print(f"Status: {account['status']}")
        print(f"Cash: ${float(account['cash']):,.2f}")
        print(f"Buying Power: ${float(account['buying_power']):,.2f}")
        print(f"Portfolio Value: ${float(account['portfolio_value']):,.2f}")
        
        is_open = self.get_market_status()
        print(f"Market: {'🟢 OPEN' if is_open else '🔴 CLOSED'}")
        
        positions = self.monitor_positions()
        print(f"\nMax Positions: {int(float(account['buying_power']) / self.max_position_size)}")
        print(f"Available Position Slots: {int(float(account['buying_power']) / self.max_position_size) - len(positions)}")
        print("="*60)

if __name__ == "__main__":
    trader = AlpacaTrader()
    trader.run_status()
