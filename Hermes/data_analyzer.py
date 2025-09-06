"""
Data analyzer for calculating KPIs from blockchain metrics
"""

import statistics
from datetime import datetime, timedelta
from typing import List, Optional
from models import BlockchainMetric, AnalyzedMetric

class DataAnalyzer:
    """Analyzes blockchain data to calculate KPIs"""
    
    def __init__(self):
        self.historical_data: List[BlockchainMetric] = []
    
    def add_historical_data(self, metrics: List[BlockchainMetric]):
        """Add historical data for analysis"""
        self.historical_data.extend(metrics)
        print(f"📊 Added {len(metrics)} historical metrics for analysis")
    
    def calculate_price_change_percentage(self, current_price: float, historical_prices: List[float]) -> float:
        """Calculate price change percentage"""
        if not historical_prices:
            return 0.0
        
        avg_historical = statistics.mean(historical_prices)
        if avg_historical == 0:
            return 0.0
        
        return ((current_price - avg_historical) / avg_historical) * 100
    
    def calculate_gas_fee_trend(self, current_gas_fee: float, historical_gas_fees: List[float]) -> float:
        """Calculate gas fee trend"""
        if not historical_gas_fees:
            return 0.0
        
        avg_historical = statistics.mean(historical_gas_fees)
        if avg_historical == 0:
            return 0.0
        
        return ((current_gas_fee - avg_historical) / avg_historical) * 100
    
    def calculate_transaction_volume_change(self, current_volume: float, historical_volumes: List[float]) -> float:
        """Calculate transaction volume change"""
        if not historical_volumes:
            return 0.0
        
        avg_historical = statistics.mean(historical_volumes)
        if avg_historical == 0:
            return 0.0
        
        return ((current_volume - avg_historical) / avg_historical) * 100
    
    def calculate_block_production_rate(self, current_blocks: int, historical_blocks: List[int], time_window_hours: float = 1.0) -> float:
        """Calculate block production rate (blocks per hour)"""
        if not historical_blocks:
            return 0.0
        
        if len(historical_blocks) < 2:
            return 0.0
        
        # Calculate blocks produced in time window
        blocks_produced = current_blocks - min(historical_blocks)
        return blocks_produced / time_window_hours
    
    def calculate_network_activity_score(self, tx_count: int, gas_fee: float, volume: float) -> float:
        """Calculate network activity score (0-100)"""
        # Normalize values and create composite score
        tx_score = min(tx_count / 1000, 1.0) * 40  # Max 40 points for transactions
        gas_score = min(gas_fee / 100, 1.0) * 30   # Max 30 points for gas fees
        volume_score = min(volume / 1000000000, 1.0) * 30  # Max 30 points for volume
        
        return tx_score + gas_score + volume_score
    
    def calculate_volatility_index(self, prices: List[float]) -> float:
        """Calculate volatility index"""
        if len(prices) < 2:
            return 0.0
        
        # Calculate standard deviation as volatility measure
        return statistics.stdev(prices) / statistics.mean(prices) * 100
    
    def calculate_liquidity_score(self, volume: float, tx_count: int) -> float:
        """Calculate liquidity score"""
        if tx_count == 0:
            return 0.0
        
        # Volume per transaction as liquidity measure
        return min(volume / tx_count / 1000, 100.0)
    
    def analyze_metrics(self, current_metric: BlockchainMetric, chain_name: str) -> AnalyzedMetric:
        """Analyze current metric against historical data"""
        # Filter historical data for this chain
        chain_data = [m for m in self.historical_data if m.chain_name == chain_name]
        
        # If we don't have enough historical data, simulate some for analysis
        if len(chain_data) < 5:
            historical_prices = self._simulate_historical_prices(current_metric.price, chain_name)
            historical_gas_fees = self._simulate_historical_gas_fees(current_metric.gas_fee, chain_name)
            historical_volumes = self._simulate_historical_volumes(current_metric.volume, chain_name)
            historical_blocks = self._simulate_historical_blocks(current_metric.number_of_blocks, chain_name)
        else:
            # Extract historical values from real data
            historical_prices = [m.price for m in chain_data[-24:]]  # Last 24 data points
            historical_gas_fees = [m.gas_fee for m in chain_data[-24:]]
            historical_volumes = [m.volume for m in chain_data[-24:]]
            historical_blocks = [m.number_of_blocks for m in chain_data[-24:]]
        
        # Calculate KPIs
        price_change = self.calculate_price_change_percentage(current_metric.price, historical_prices)
        gas_fee_trend = self.calculate_gas_fee_trend(current_metric.gas_fee, historical_gas_fees)
        volume_change = self.calculate_transaction_volume_change(current_metric.volume, historical_volumes)
        block_rate = self.calculate_block_production_rate(current_metric.number_of_blocks, historical_blocks)
        activity_score = self.calculate_network_activity_score(
            current_metric.number_of_transactions,
            current_metric.gas_fee,
            current_metric.volume
        )
        volatility = self.calculate_volatility_index(historical_prices + [current_metric.price])
        liquidity = self.calculate_liquidity_score(current_metric.volume, current_metric.number_of_transactions)
        
        return AnalyzedMetric(
            chain_name=chain_name,
            timestamp=current_metric.timestamp,
            price_change_percentage=price_change,
            gas_fee_trend=gas_fee_trend,
            transaction_volume_change=volume_change,
            block_production_rate=block_rate,
            network_activity_score=activity_score,
            volatility_index=volatility,
            liquidity_score=liquidity
        )
    
    def get_analysis_summary(self, analyzed_metrics: List[AnalyzedMetric]) -> dict:
        """Get summary of analysis results"""
        if not analyzed_metrics:
            return {}
        
        return {
            'total_chains_analyzed': len(set(m.chain_name for m in analyzed_metrics)),
            'avg_price_change': statistics.mean([m.price_change_percentage for m in analyzed_metrics]),
            'avg_gas_fee_trend': statistics.mean([m.gas_fee_trend for m in analyzed_metrics]),
            'avg_activity_score': statistics.mean([m.network_activity_score for m in analyzed_metrics]),
            'avg_volatility': statistics.mean([m.volatility_index for m in analyzed_metrics]),
            'most_active_chain': max(analyzed_metrics, key=lambda x: x.network_activity_score).chain_name,
            'most_volatile_chain': max(analyzed_metrics, key=lambda x: x.volatility_index).chain_name
        }
    
    def _simulate_historical_prices(self, current_price: float, chain_name: str) -> List[float]:
        """Simulate historical prices for analysis"""
        import random
        
        # Create 24 historical price points with realistic volatility
        volatility_map = {
            'ethereum': 0.05,  # 5% daily volatility
            'bitcoin': 0.08,   # 8% daily volatility
            'polygon': 0.12    # 12% daily volatility
        }
        
        volatility = volatility_map.get(chain_name, 0.05)
        historical_prices = []
        
        for i in range(24):
            # Add some random variation to simulate price movement
            variation = random.uniform(-volatility, volatility)
            historical_price = current_price * (1 + variation)
            historical_prices.append(historical_price)
        
        return historical_prices
    
    def _simulate_historical_gas_fees(self, current_gas_fee: float, chain_name: str) -> List[float]:
        """Simulate historical gas fees for analysis"""
        import random
        
        historical_gas_fees = []
        for i in range(24):
            # Gas fees vary more dramatically
            variation = random.uniform(-0.3, 0.3)  # ±30% variation
            historical_gas_fee = max(0.1, current_gas_fee * (1 + variation))
            historical_gas_fees.append(historical_gas_fee)
        
        return historical_gas_fees
    
    def _simulate_historical_volumes(self, current_volume: float, chain_name: str) -> List[float]:
        """Simulate historical volumes for analysis"""
        import random
        
        historical_volumes = []
        for i in range(24):
            # Volume varies significantly
            variation = random.uniform(-0.5, 0.5)  # ±50% variation
            historical_volume = max(1000000, current_volume * (1 + variation))
            historical_volumes.append(historical_volume)
        
        return historical_volumes
    
    def _simulate_historical_blocks(self, current_blocks: int, chain_name: str) -> List[int]:
        """Simulate historical block numbers for analysis"""
        historical_blocks = []
        for i in range(24):
            # Blocks increase over time
            historical_blocks.append(current_blocks - (24 - i) * 100)
        
        return historical_blocks
