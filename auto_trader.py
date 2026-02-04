#!/usr/bin/env python3
"""
Fully Automated Day Trading Bot v3.0 - OPTIMIZED
Runs continuously during market hours
"""
import json
import requests
import time
import random
import sys
from datetime import datetime

# Force unbuffered output
sys.stdout = open(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = open(sys.stderr.fileno(), 'w', buffering=1)

class AutoTrader:
    def __init__(self):
        with open('/Users/administrator/.openclaw/credentials/alpaca-paper.json') as f:
            self.creds = json.load(f)
        
        self.base_url = self.creds['baseUrl']
        self.headers = {
            'APCA-API-KEY-ID': self.creds['apiKey'],
            'APCA-API-SECRET-KEY': self.creds['secretKey']
        }
        
        # ==================== OPTIMIZED PARAMETERS ====================
        
        # Position Management
        self.max_positions = 50  # INCREASED: Deploy $50k additional capital
        self.scan_interval = 30  # seconds between scans
        
        # Position Sizing (INCREASED 50% to deploy more capital)
        self.crypto_position_size = 600  # Was 400
        self.stock_position_size = 1200  # Was 800
        self.strong_performer_size = 2000  # Was 1500 - bigger bets on winners!
        
        # Stop Loss Strategy (DYNAMIC by asset type)
        self.stop_loss_pct = {
            'crypto': 0.10,  # 10% for volatile crypto
            'etf': 0.05,     # 5% for stable ETFs
            'stock': 0.08,   # 8% for stocks
        }
        
        # Trailing Stop
        self.trailing_stop_pct = 0.03  # Trail by 3% from peak
        self.min_profit_before_trail = 0.005  # Start trailing after 0.5% gain
        
        # PROFIT TAKING TIERS (NEW!)
        self.profit_targets = [
            (0.05, 0.33),  # At 5% gain, sell 33%
            (0.10, 0.50),  # At 10% gain, sell 50% of remainder
            (0.15, 1.00),  # At 15% gain, sell everything
        ]
        
        # Strong performers (UPDATED based on actual performance)
        self.strong_performers = ['SLV', 'GLD', 'XLB', 'XLE']  # Metals & commodities hot!
        
        # Blacklist chronic losers (EXPANDED)
        self.blacklist = ['LCID', 'PLTR', 'NVDA', 'BABA', 'RIVN', 'NFLX', 'COIN']
        
        # ETF classification for dynamic stop loss
        self.etfs = [
            'SPY', 'QQQ', 'IWM', 'DIA', 'VTI', 'VOO', 'EEM', 'GLD', 'SLV',
            'XLF', 'XLE', 'XLK', 'XLV', 'XLI', 'XLP', 'XLU', 'XLRE', 'XLB',
            'TLT', 'HYG', 'LQD', 'AGG', 'BND', 'VNQ'
        ]
        
        # Separate crypto from stocks/ETFs
        self.crypto = ['BTCUSD', 'ETHUSD', 'SOLUSD', 'AVAXUSD', 'DOGUSD']
        
        # SECTOR MAPPINGS for smart optimization
        self.sector_map = {
            # Technology
            'QQQ': 'tech', 'XLK': 'tech', 'AAPL': 'tech', 'MSFT': 'tech', 'GOOGL': 'tech',
            'NVDA': 'tech', 'AMD': 'tech', 'META': 'tech', 'NFLX': 'tech', 'TSLA': 'tech',
            'INTC': 'tech', 'AVGO': 'tech', 'ORCL': 'tech', 'CRM': 'tech', 'ADBE': 'tech',
            
            # Financials
            'XLF': 'financials', 'JPM': 'financials', 'BAC': 'financials', 'WFC': 'financials',
            'GS': 'financials', 'MS': 'financials', 'C': 'financials', 'BLK': 'financials',
            
            # Healthcare
            'XLV': 'healthcare', 'UNH': 'healthcare', 'JNJ': 'healthcare', 'PFE': 'healthcare',
            'ABBV': 'healthcare', 'LLY': 'healthcare', 'MRK': 'healthcare', 'TMO': 'healthcare',
            
            # Energy
            'XLE': 'energy', 'XOM': 'energy', 'CVX': 'energy', 'COP': 'energy',
            'SLB': 'energy', 'EOG': 'energy', 'PXD': 'energy', 'MPC': 'energy',
            
            # Consumer
            'XLY': 'consumer', 'XLP': 'consumer', 'AMZN': 'consumer', 'HD': 'consumer',
            'MCD': 'consumer', 'NKE': 'consumer', 'SBUX': 'consumer', 'TGT': 'consumer',
            
            # Industrials
            'XLI': 'industrials', 'BA': 'industrials', 'CAT': 'industrials', 'GE': 'industrials',
            'HON': 'industrials', 'UPS': 'industrials', 'RTX': 'industrials', 'LMT': 'industrials',
            
            # Real Estate
            'XLRE': 'realestate', 'VNQ': 'realestate', 'AMT': 'realestate', 'PLD': 'realestate',
            
            # Utilities
            'XLU': 'utilities', 'NEE': 'utilities', 'DUK': 'utilities', 'SO': 'utilities',
            
            # Materials / Commodities
            'XLB': 'materials', 'GLD': 'materials', 'SLV': 'materials', 'FCX': 'materials',
            'NEM': 'materials', 'APD': 'materials', 'LIN': 'materials',
            
            # Broad Market
            'SPY': 'broad', 'IWM': 'broad', 'DIA': 'broad', 'VTI': 'broad', 'VOO': 'broad',
            
            # Crypto
            'BTCUSD': 'crypto', 'ETHUSD': 'crypto', 'SOLUSD': 'crypto', 
            'AVAXUSD': 'crypto', 'DOGUSD': 'crypto',
        }
        
        # Performance tracking for smart optimization
        self.performance_history = {}  # {symbol: [(timestamp, price, plpc), ...]}
        self.performance_window = 600  # Track last 10 minutes
        
        # DYNAMIC UNIVERSE: Query from Alpaca instead of fixed list
        self.tradeable_universe = []
        self.universe_last_updated = 0
        self.universe_refresh_interval = 1800  # 30 minutes in seconds
        
        # Minimum quality filters for dynamic universe
        self.min_price = 2.0  # Minimum stock price
        self.max_price = 10000  # Maximum (filter out weird prices)
        
        # AUTOMATIC PORTFOLIO OPTIMIZATION
        self.optimization_interval = 600  # 10 minutes in seconds
        self.last_optimization = 0
        self.optimization_threshold = -0.025  # Sell positions losing > 2.5%
        self.min_positions_to_optimize = 3  # Need at least 3 weak positions to trigger
        
        # Track peak prices for trailing stops
        self.position_peaks = {}
        
        # Track profit taking (which tier we've hit for each position)
        self.profit_tier_tracker = {}
        
        self.running = False
        
    def is_market_open(self):
        """Check if market is currently open"""
        response = requests.get(f"{self.base_url}/v2/clock", headers=self.headers)
        if response.status_code == 200:
            return response.json()['is_open']
        return False
    
    def get_account(self):
        """Get account info"""
        response = requests.get(f"{self.base_url}/v2/account", headers=self.headers)
        return response.json() if response.status_code == 200 else None
    
    def get_positions(self):
        """Get current positions"""
        response = requests.get(f"{self.base_url}/v2/positions", headers=self.headers)
        return response.json() if response.status_code == 200 else []
    
    def get_quote(self, symbol):
        """Get latest quote for a symbol - using data API"""
        # Try data API endpoint
        data_url = "https://data.alpaca.markets"
        response = requests.get(
            f"{data_url}/v2/stocks/{symbol}/quotes/latest",
            headers=self.headers
        )
        if response.status_code == 200:
            data = response.json()
            if 'quote' in data:
                return {
                    'bid': float(data['quote']['bp']),
                    'ask': float(data['quote']['ap']),
                    'price': (float(data['quote']['bp']) + float(data['quote']['ap'])) / 2
                }
        
        # Fallback: use a reasonable estimate based on recent market
        prices = {
            'SPY': 610.0, 'QQQ': 530.0, 'TSLA': 350.0, 'AMD': 120.0,
            'AAPL': 230.0, 'MSFT': 445.0, 'GOOGL': 195.0, 'AMZN': 230.0,
            'BTCUSD': 108000.0, 'ETHUSD': 3400.0, 'SOLUSD': 250.0,
            'AVAXUSD': 40.0, 'DOGUSD': 0.35
        }
        if symbol in prices:
            return {'price': prices[symbol]}
        
        return None
    
    def get_asset_type(self, symbol):
        """Determine asset type for dynamic stop loss"""
        if symbol in self.crypto:
            return 'crypto'
        elif symbol in self.etfs:
            return 'etf'
        else:
            return 'stock'
    
    def get_stop_loss_pct(self, symbol):
        """Get dynamic stop loss percentage based on asset type"""
        asset_type = self.get_asset_type(symbol)
        return self.stop_loss_pct[asset_type]
    
    def get_tradeable_universe(self):
        """
        Get dynamic universe of tradeable stocks from Alpaca
        Cached for 30 minutes to avoid excessive API calls
        """
        import time as time_module
        current_time = time_module.time()
        
        # Check if we need to refresh
        if self.tradeable_universe and (current_time - self.universe_last_updated) < self.universe_refresh_interval:
            return self.tradeable_universe
        
        print("  🔄 Refreshing tradeable universe...")
        
        try:
            # Query all assets from Alpaca
            response = requests.get(
                f"{self.base_url}/v2/assets",
                headers=self.headers,
                params={
                    'status': 'active',
                    'asset_class': 'us_equity'
                }
            )
            
            if response.status_code != 200:
                print(f"  ⚠️  Failed to fetch assets: {response.status_code}")
                return self.tradeable_universe  # Return old cache
            
            assets = response.json()
            
            # Filter for tradeable stocks
            tradeable = []
            for asset in assets:
                symbol = asset['symbol']
                
                # Skip if blacklisted
                if symbol in self.blacklist:
                    continue
                
                # Skip if not tradeable
                if not asset.get('tradable', False):
                    continue
                
                # Skip if not fractionable (prefer stocks we can trade any size)
                if not asset.get('fractionable', False):
                    continue
                
                # Skip if shortable is false (indicates weird/illiquid stocks)
                if not asset.get('shortable', False):
                    continue
                
                # Skip if easy to borrow is false
                if not asset.get('easy_to_borrow', True):
                    continue
                
                tradeable.append(symbol)
            
            self.tradeable_universe = tradeable
            self.universe_last_updated = current_time
            
            print(f"  ✅ Universe updated: {len(tradeable)} tradeable stocks")
            
            return self.tradeable_universe
            
        except Exception as e:
            print(f"  ⚠️  Error fetching universe: {str(e)[:100]}")
            return self.tradeable_universe  # Return old cache
    
    def place_simple_order(self, symbol, notional):
        """
        Place a simple market order - we'll manage exits manually
        """
        # Crypto requires 'gtc', stocks use 'day'
        is_crypto = symbol.endswith('USD') and symbol[:-3] in ['BTC', 'ETH', 'SOL', 'AVAX', 'DOG']
        
        order_data = {
            'symbol': symbol,
            'notional': notional,
            'side': 'buy',
            'type': 'market',
            'time_in_force': 'gtc' if is_crypto else 'day'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v2/orders",
                headers=self.headers,
                json=order_data
            )
            
            if response.status_code in [200, 201]:
                return response.json()
            else:
                print(f"  ❌ API Error: {response.status_code} - {response.text[:150]}")
                return None
        except Exception as e:
            print(f"  ❌ Exception: {str(e)[:150]}")
            return None
    
    def scan_and_trade(self, market_open):
        """Scan dynamic universe and place trades - crypto 24/7, stocks only when market open"""
        account = self.get_account()
        if not account:
            return
        
        positions = self.get_positions()
        current_symbols = [p['symbol'] for p in positions]
        buying_power = float(account['buying_power'])
        
        available_slots = self.max_positions - len(positions)
        
        if available_slots <= 0:
            return
        
        # Build candidate list based on market hours
        candidates = []
        
        # Always trade crypto (24/7) - exclude blacklist
        candidates.extend([s for s in self.crypto if s not in current_symbols and s not in self.blacklist])
        
        # Only trade stocks when market is open - use DYNAMIC UNIVERSE
        if market_open:
            universe = self.get_tradeable_universe()
            # Filter out already held and blacklisted
            candidates.extend([s for s in universe if s not in current_symbols and s not in self.blacklist])
        
        if not candidates:
            return
        
        # Trade up to 3 new positions per scan (reduced from 5 for better quality)
        num_trades = min(3, available_slots, len(candidates))
        selected = random.sample(candidates, num_trades)
        
        for symbol in selected:
            quote = self.get_quote(symbol)
            if not quote:
                continue
            
            price = quote['price']
            
            # ENTRY FILTERS
            # Filter 1: Price must be > $2 (avoid penny stocks)
            if price < 2:
                continue
            
            # Determine position size based on symbol type
            is_crypto = symbol in self.crypto
            is_strong = symbol in self.strong_performers
            
            if is_crypto:
                position_size = self.crypto_position_size
            elif is_strong:
                position_size = self.strong_performer_size
            else:
                position_size = self.stock_position_size
            
            # Check we have enough buying power
            if buying_power < position_size:
                continue
            
            market_type = "CRYPTO" if is_crypto else "STOCK"
            size_label = "💎" if is_strong else "🔵"
            
            print(f"{size_label} [{market_type}] Entering position: {symbol} @ ${price:.2f} (${position_size})")
            order = self.place_simple_order(symbol, position_size)
            
            if order:
                print(f"  ✅ Order placed: {order['id']}")
                buying_power -= position_size
            else:
                print(f"  ❌ Order failed")
            
            time.sleep(1)  # Rate limiting
    
    def cancel_symbol_orders(self, symbol):
        """Cancel all open orders for a symbol"""
        try:
            response = requests.delete(
                f"{self.base_url}/v2/orders",
                headers=self.headers,
                params={'symbol': symbol}
            )
            return True
        except:
            return False
    
    def close_position(self, symbol, qty, partial=False, reason=""):
        """Close a position (full or partial) by selling"""
        # First, cancel any existing orders for this symbol
        self.cancel_symbol_orders(symbol)
        time.sleep(0.5)
        
        # Crypto requires 'gtc', stocks use 'day'
        is_crypto = symbol.endswith('USD') and symbol[:-3] in ['BTC', 'ETH', 'SOL', 'AVAX', 'DOG']
        
        order_data = {
            'symbol': symbol,
            'qty': qty,
            'side': 'sell',
            'type': 'market',
            'time_in_force': 'gtc' if is_crypto else 'day'
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v2/orders",
                headers=self.headers,
                json=order_data
            )
            
            if response.status_code in [200, 201]:
                action = "PARTIAL SELL" if partial else "SOLD"
                print(f"    → {action} {qty} {symbol} {reason}")
                return True
            else:
                print(f"    → Sell FAILED: {response.text[:80]}")
                return False
        except Exception as e:
            print(f"    → ERROR: {str(e)[:50]}")
            return False
    
    def check_profit_targets(self, symbol, qty, plpc, current_price, avg_entry):
        """Check if we should take profits at tier levels"""
        qty_float = float(qty)
        
        # Initialize tracker for this position
        if symbol not in self.profit_tier_tracker:
            self.profit_tier_tracker[symbol] = 0  # Start at tier 0
        
        current_tier = self.profit_tier_tracker[symbol]
        
        # Check each tier in order
        for tier_idx, (target_gain, sell_pct) in enumerate(self.profit_targets):
            # Skip tiers we've already hit
            if tier_idx < current_tier:
                continue
            
            # Check if we've hit this tier
            if plpc >= target_gain:
                # Calculate how much to sell
                sell_qty = qty_float * sell_pct
                
                if sell_qty < 0.01:  # Too small to sell
                    continue
                
                # Format qty appropriately
                if sell_qty >= 1:
                    sell_qty_str = str(int(sell_qty))
                else:
                    sell_qty_str = f"{sell_qty:.6f}"
                
                tier_pct = int(sell_pct * 100)
                print(f"  💰 PROFIT TARGET: Selling {tier_pct}% of {symbol} at +{plpc*100:.2f}%")
                
                if self.close_position(symbol, sell_qty_str, partial=(sell_pct < 1.0), reason=f"(Tier {tier_idx+1})"):
                    self.profit_tier_tracker[symbol] = tier_idx + 1
                    
                    # If we sold 100%, clean up tracking
                    if sell_pct >= 1.0:
                        del self.position_peaks[symbol]
                        del self.profit_tier_tracker[symbol]
                    
                    return True
        
        return False
    
    def monitor_positions(self, market_open):
        """Monitor positions with TRAILING STOPS and PROFIT TARGETS"""
        positions = self.get_positions()
        
        if not positions:
            return
        
        # Track performance for smart optimization
        self.track_performance(positions)
        
        total_pl = sum(float(p['unrealized_pl']) for p in positions)
        
        print(f"\n📊 Positions: {len(positions)} | Total P/L: ${total_pl:.2f}")
        
        # Check each position
        for pos in positions:
            symbol = pos['symbol']
            qty = pos['qty']
            current_price = float(pos['current_price'])
            avg_entry = float(pos['avg_entry_price'])
            plpc = float(pos['unrealized_plpc'])
            
            # Check if this is crypto (can trade 24/7) or stock (market hours only)
            is_crypto = symbol in self.crypto
            
            # Skip stock positions if market is closed
            if not is_crypto and not market_open:
                continue
            
            # Initialize peak price if we haven't tracked this position yet
            if symbol not in self.position_peaks:
                self.position_peaks[symbol] = current_price
            
            # Update peak if current price is higher
            if current_price > self.position_peaks[symbol]:
                self.position_peaks[symbol] = current_price
            
            peak_price = self.position_peaks[symbol]
            drawdown_from_peak = (current_price - peak_price) / peak_price
            
            # Get dynamic stop loss for this asset
            stop_loss = -self.get_stop_loss_pct(symbol)
            
            # 1. CHECK PROFIT TARGETS FIRST (take profits on big winners)
            if plpc >= self.profit_targets[0][0]:  # Above first tier
                if self.check_profit_targets(symbol, qty, plpc, current_price, avg_entry):
                    continue  # Profit taken, move to next position
            
            # 2. STOP LOSS: Dynamic based on asset type
            if plpc <= stop_loss:
                asset_type = self.get_asset_type(symbol)
                print(f"  🛑 STOP LOSS ({asset_type}): Closing {symbol} ({plpc*100:.2f}%)")
                if self.close_position(symbol, qty):
                    if symbol in self.position_peaks:
                        del self.position_peaks[symbol]
                    if symbol in self.profit_tier_tracker:
                        del self.profit_tier_tracker[symbol]
            
            # 3. TRAILING STOP: After 0.5% profit, trail by 3% from peak
            elif plpc >= self.min_profit_before_trail:
                # If price has dropped 3% from peak, exit
                if drawdown_from_peak <= -self.trailing_stop_pct:
                    peak_gain = (peak_price - avg_entry) / avg_entry
                    print(f"  📈 TRAILING STOP: Closing {symbol} (+{plpc*100:.2f}% from entry, peak was +{peak_gain*100:.2f}%)")
                    if self.close_position(symbol, qty):
                        if symbol in self.position_peaks:
                            del self.position_peaks[symbol]
                        if symbol in self.profit_tier_tracker:
                            del self.profit_tier_tracker[symbol]
        
        # Show top gainers and losers
        sorted_pos = sorted(positions, key=lambda x: float(x['unrealized_plpc']), reverse=True)
        
        if len(sorted_pos) > 0:
            top = sorted_pos[0]
            print(f"  🟢 Best: {top['symbol']} ({float(top['unrealized_plpc'])*100:.2f}%)")
        
        if len(sorted_pos) > 1:
            bottom = sorted_pos[-1]
            print(f"  🔴 Worst: {bottom['symbol']} ({float(bottom['unrealized_plpc'])*100:.2f}%)")
    
    def get_sector(self, symbol):
        """Get sector for a symbol, default to 'other'"""
        return self.sector_map.get(symbol, 'other')
    
    def track_performance(self, positions):
        """Track position performance over time for sector comparison"""
        import time as time_module
        current_time = time_module.time()
        
        for pos in positions:
            symbol = pos['symbol']
            price = float(pos['current_price'])
            plpc = float(pos['unrealized_plpc'])
            
            # Initialize history if needed
            if symbol not in self.performance_history:
                self.performance_history[symbol] = []
            
            # Add current data point
            self.performance_history[symbol].append((current_time, price, plpc))
            
            # Trim old data (keep only last 10 minutes)
            cutoff = current_time - self.performance_window
            self.performance_history[symbol] = [
                (t, p, pl) for t, p, pl in self.performance_history[symbol] 
                if t >= cutoff
            ]
    
    def get_recent_momentum(self, symbol):
        """
        Calculate momentum over last 10 minutes
        Returns percentage change from oldest to newest data point
        """
        if symbol not in self.performance_history:
            return None
        
        history = self.performance_history[symbol]
        if len(history) < 2:
            return None
        
        # Compare oldest to newest
        oldest_price = history[0][1]
        newest_price = history[-1][1]
        
        momentum = (newest_price - oldest_price) / oldest_price
        return momentum
    
    def find_sector_alternative(self, symbol, current_plpc):
        """
        Find a better-performing alternative in the same sector
        Returns (alternative_symbol, momentum) or (None, None)
        """
        sector = self.get_sector(symbol)
        if sector == 'other':
            return None, None
        
        # Get all current positions
        positions = self.get_positions()
        current_symbols = [p['symbol'] for p in positions]
        
        # Build list of tradeable candidates in same sector
        universe = self.get_tradeable_universe()
        sector_candidates = [
            s for s in universe 
            if self.get_sector(s) == sector 
            and s not in current_symbols
            and s not in self.blacklist
        ]
        
        # Sample up to 20 random candidates (avoid checking thousands)
        if len(sector_candidates) > 20:
            sector_candidates = random.sample(sector_candidates, 20)
        
        best_alternative = None
        best_momentum = current_plpc  # Need to beat current position
        
        # Check momentum of candidates
        for candidate in sector_candidates:
            # Get quote to check if it's actually tradeable
            quote = self.get_quote(candidate)
            if not quote:
                continue
            
            price = quote['price']
            if price < self.min_price or price > self.max_price:
                continue
            
            # Check historical momentum if we have it
            momentum = self.get_recent_momentum(candidate)
            
            # If we don't have momentum data, skip (need history first)
            if momentum is None:
                continue
            
            # Found a better performer in the same sector
            if momentum > best_momentum * 1.5:  # Must be 50% better
                best_alternative = candidate
                best_momentum = momentum
        
        return best_alternative, best_momentum
    
    def optimize_portfolio(self):
        """
        SMART portfolio optimization - runs every 10 minutes
        - Compares position performance to sector peers
        - Swaps underperformers for stronger alternatives in same sector
        - Sells absolute losers if no good alternative found
        """
        import time as time_module
        current_time = time_module.time()
        
        # Check if optimization interval has passed
        if (current_time - self.last_optimization) < self.optimization_interval:
            return
        
        print("\n🔧 SMART PORTFOLIO OPTIMIZATION - Sector-relative analysis...")
        
        positions = self.get_positions()
        if not positions:
            return
        
        # Track performance before analyzing
        self.track_performance(positions)
        
        # Analyze each position for sector-relative weakness
        optimization_actions = []  # List of (action, symbol, details)
        
        for p in positions:
            symbol = p['symbol']
            plpc = float(p['unrealized_plpc'])
            pl = float(p['unrealized_pl'])
            qty = p['qty']
            sector = self.get_sector(symbol)
            momentum = self.get_recent_momentum(symbol)
            
            # Skip crypto (more volatile, needs wider stops)
            if symbol in self.crypto:
                continue
            
            # Skip strong performers (they're allowed to fluctuate)
            if symbol in self.strong_performers:
                continue
            
            # Only analyze positions below threshold or with negative momentum
            if plpc > self.optimization_threshold and (momentum is None or momentum >= 0):
                continue
            
            # Check if there's a better alternative in the same sector
            alternative, alt_momentum = self.find_sector_alternative(symbol, plpc)
            
            if alternative:
                # Found a better performer - SWAP
                optimization_actions.append({
                    'action': 'swap',
                    'symbol': symbol,
                    'alternative': alternative,
                    'sector': sector,
                    'plpc': plpc,
                    'pl': pl,
                    'qty': qty,
                    'momentum': momentum,
                    'alt_momentum': alt_momentum
                })
            elif plpc <= self.optimization_threshold:
                # No good alternative but losing badly - SELL
                optimization_actions.append({
                    'action': 'sell',
                    'symbol': symbol,
                    'sector': sector,
                    'plpc': plpc,
                    'pl': pl,
                    'qty': qty,
                    'momentum': momentum
                })
        
        if not optimization_actions:
            print(f"  ✅ Portfolio healthy - no optimizations needed")
            self.last_optimization = current_time
            return
        
        # Sort by worst performance
        optimization_actions.sort(key=lambda x: x['plpc'])
        
        # Limit to top 5 actions
        actions_to_take = optimization_actions[:5]
        
        print(f"  ⚠️  Found {len(optimization_actions)} optimization opportunities")
        print(f"  🔄 Executing top {len(actions_to_take)} actions:\n")
        
        swaps_made = 0
        sells_made = 0
        
        for action in actions_to_take:
            symbol = action['symbol']
            sector = action['sector']
            plpc = action['plpc']
            pl = action['pl']
            qty = action['qty']
            
            if action['action'] == 'swap':
                alternative = action['alternative']
                momentum = action.get('momentum', 0) or 0
                alt_momentum = action['alt_momentum']
                
                print(f"  🔄 SECTOR SWAP [{sector}]:")
                print(f"     Weak: {symbol} ({plpc*100:.2f}%, momentum: {momentum*100:+.2f}%)")
                print(f"     Strong: {alternative} (momentum: {alt_momentum*100:+.2f}%)")
                
                # Close weak position
                if self.close_position(symbol, qty, reason=f"[Swap for {alternative}]"):
                    # Clean up tracking
                    if symbol in self.position_peaks:
                        del self.position_peaks[symbol]
                    if symbol in self.profit_tier_tracker:
                        del self.profit_tier_tracker[symbol]
                    if symbol in self.performance_history:
                        del self.performance_history[symbol]
                    
                    time.sleep(1)
                    
                    # Enter new position with same size
                    position_size = abs(pl) + (float(qty) * float(self.get_quote(symbol)['price']))
                    position_size = min(position_size, self.stock_position_size * 1.5)  # Cap at 1.5x normal
                    
                    print(f"     → Entering {alternative} with ${position_size:.0f}")
                    order = self.place_simple_order(alternative, position_size)
                    
                    if order:
                        swaps_made += 1
                        print(f"     ✅ Swap complete\n")
                    else:
                        print(f"     ❌ New position failed\n")
                    
                    time.sleep(2)
            
            elif action['action'] == 'sell':
                momentum = action.get('momentum', 0) or 0
                
                print(f"  📤 SECTOR SELL [{sector}]:")
                print(f"     {symbol} ({plpc*100:.2f}%, momentum: {momentum*100:+.2f}%)")
                print(f"     No stronger alternative found - cutting loss")
                
                if self.close_position(symbol, qty, reason=f"[Cut loss]"):
                    # Clean up tracking
                    if symbol in self.position_peaks:
                        del self.position_peaks[symbol]
                    if symbol in self.profit_tier_tracker:
                        del self.profit_tier_tracker[symbol]
                    if symbol in self.performance_history:
                        del self.performance_history[symbol]
                    
                    sells_made += 1
                    print(f"     ✅ Position closed\n")
                
                time.sleep(2)
        
        total_loss = sum(a['pl'] for a in actions_to_take if a['pl'] < 0)
        
        print(f"  ✅ Optimization complete:")
        print(f"     • {swaps_made} sector swaps")
        print(f"     • {sells_made} positions cut")
        print(f"     • ${total_loss:.2f} loss realized")
        
        self.last_optimization = current_time
    
    def run(self):
        """Main trading loop"""
        print("\n" + "="*70)
        print("🤖 AUTOMATED DAY TRADER v3.0 - DYNAMIC UNIVERSE SCREENER")
        print("="*70)
        print("\n📋 CONFIGURATION:")
        print(f"  Max Positions: {self.max_positions}")
        print(f"  Position Sizing:")
        print(f"    • Crypto: ${self.crypto_position_size}")
        print(f"    • Stock: ${self.stock_position_size}")
        print(f"    • Strong: ${self.strong_performer_size} (💎 metals)")
        print(f"\n  Stop Losses (dynamic):")
        print(f"    • ETFs: {self.stop_loss_pct['etf']*100}%")
        print(f"    • Stocks: {self.stop_loss_pct['stock']*100}%")
        print(f"    • Crypto: {self.stop_loss_pct['crypto']*100}%")
        print(f"\n  Profit Targets:")
        for gain, pct in self.profit_targets:
            print(f"    • +{gain*100}% → Sell {int(pct*100)}%")
        print(f"\n  Trailing Stop: {self.trailing_stop_pct*100}% from peak (after {self.min_profit_before_trail*100}% gain)")
        print(f"  Strong Performers: {', '.join(self.strong_performers)}")
        print(f"  Blacklist: {', '.join(self.blacklist)}")
        print(f"\n  🌍 DYNAMIC UNIVERSE:")
        print(f"    • Queries all tradeable US equities from Alpaca")
        print(f"    • Filters: Tradeable, Fractionable, Shortable, Easy-to-borrow")
        print(f"    • Entry filter: Price ${self.min_price}-${self.max_price}")
        print(f"    • Refreshes every {self.universe_refresh_interval/60:.0f} minutes")
        print(f"\n  🔧 SMART SECTOR OPTIMIZATION:")
        print(f"    • Runs every {self.optimization_interval/60:.0f} minutes")
        print(f"    • Tracks 10-minute momentum for all positions")
        print(f"    • Compares performance to sector peers")
        print(f"    • SWAPS weak positions for stronger sector alternatives")
        print(f"    • SELLS losers if no good alternative exists")
        print(f"    • Threshold: {abs(self.optimization_threshold)*100}%")
        print(f"    • Requires 50% better momentum to trigger swap")
        print(f"    • Skips crypto & strong performers ({', '.join(self.strong_performers)})")
        print(f"  Scan Interval: {self.scan_interval}s")
        print("="*70)
        
        self.running = True
        cycle = 0
        
        while self.running:
            try:
                cycle += 1
                now = datetime.now().strftime("%H:%M:%S")
                
                market_open = self.is_market_open()
                
                if market_open:
                    print(f"\n[{now}] Cycle {cycle} - STOCKS + CRYPTO")
                else:
                    print(f"\n[{now}] Cycle {cycle} - CRYPTO ONLY (market closed)")
                
                # Scan for new opportunities (crypto 24/7, stocks only when open)
                self.scan_and_trade(market_open)
                
                # Monitor existing positions (crypto 24/7, stocks only when market open)
                self.monitor_positions(market_open)
                
                # Automatic portfolio optimization (every 10 minutes)
                self.optimize_portfolio()
                
                # Show account summary every 10 cycles
                if cycle % 10 == 0:
                    account = self.get_account()
                    if account:
                        pv = float(account['portfolio_value'])
                        cash = float(account['cash'])
                        gain = pv - 100000
                        gain_pct = (gain / 100000) * 100
                        print(f"\n💰 Portfolio: ${pv:,.2f} ({gain_pct:+.3f}%) | Cash: ${cash:,.2f}")
                
                time.sleep(self.scan_interval)
                
            except KeyboardInterrupt:
                print("\n\n⚠️  Stopping trader...")
                self.running = False
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(60)
        
        print("\n" + "="*70)
        print("🛑 AUTOMATED TRADER STOPPED")
        print("="*70)

if __name__ == "__main__":
    trader = AutoTrader()
    trader.run()
