"""
Blockchain client for retrieving data from various blockchain networks
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from typing import Dict, Optional
from web3 import Web3

class BlockchainClient:
    """Client for retrieving blockchain data from various networks"""
    
    def __init__(self):
        self.sessions: Dict[str, aiohttp.ClientSession] = {}
        self.web3_clients: Dict[str, Web3] = {}
        
        # RPC endpoints
        self.rpc_endpoints = {
            'ethereum': 'https://lb.drpc.org/sepolia/AplHGB2v9khYpYVNxc5za0FxucDEi1sR8IqgqhnKxixj',
            'bitcoin': 'https://blockstream.info/api/',
            'polygon': 'https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY'
        }
        
        # Price API endpoints
        self.price_apis = {
            'ethereum': 'https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd',  # Sepolia ETH same price as mainnet
            'bitcoin': 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd',
            'polygon': 'https://api.coingecko.com/api/v3/simple/price?ids=matic-network&vs_currencies=usd'
        }
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
    
    async def close(self):
        """Close all sessions"""
        for session in self.sessions.values():
            await session.close()
    
    async def _get_session(self, chain_name: str) -> aiohttp.ClientSession:
        """Get or create HTTP session for chain"""
        if chain_name not in self.sessions:
            self.sessions[chain_name] = aiohttp.ClientSession()
        return self.sessions[chain_name]
    
    async def get_current_price(self, chain_name: str) -> float:
        """Get current price for a blockchain"""
        try:
            if chain_name not in self.price_apis:
                print(f"⚠️  No price API for {chain_name}, using default")
                return 1000.0  # Default price
            
            session = await self._get_session(chain_name)
            async with session.get(self.price_apis[chain_name]) as response:
                if response.status == 200:
                    data = await response.json()
                    # Extract price based on chain
                    if chain_name == 'ethereum':
                        price = data['ethereum']['usd']
                        print(f"   💰 Ethereum price: ${price}")
                        return price
                    elif chain_name == 'bitcoin':
                        price = data['bitcoin']['usd']
                        print(f"   💰 Bitcoin price: ${price}")
                        return price
                    elif chain_name == 'polygon':
                        price = data['matic-network']['usd']
                        print(f"   💰 Polygon price: ${price}")
                        return price
                else:
                    print(f"   ⚠️  Price API returned status {response.status}")
            
            # Fallback to realistic simulated prices
            fallback_prices = {
                'ethereum': 2500.0,
                'bitcoin': 45000.0,
                'polygon': 0.8
            }
            price = fallback_prices.get(chain_name, 1000.0)
            print(f"   💰 {chain_name} price (fallback): ${price}")
            return price
            
        except Exception as e:
            print(f"❌ Error getting price for {chain_name}: {e}")
            # Fallback to realistic simulated prices
            fallback_prices = {
                'ethereum': 2500.0,
                'bitcoin': 45000.0,
                'polygon': 0.8
            }
            price = fallback_prices.get(chain_name, 1000.0)
            print(f"   💰 {chain_name} price (error fallback): ${price}")
            return price
    
    async def get_volume(self, chain_name: str) -> float:
        """Get trading volume for a blockchain"""
        try:
            # Simulate volume based on chain activity
            volume_map = {
                'ethereum': 5000000000.0,  # $5B
                'bitcoin': 10000000000.0,  # $10B
                'polygon': 500000000.0     # $500M
            }
            return volume_map.get(chain_name, 1000000000.0)
            
        except Exception as e:
            print(f"❌ Error getting volume for {chain_name}: {e}")
            return 1000000000.0
    
    async def get_gas_fee(self, chain_name: str) -> float:
        """Get current gas fee for a blockchain"""
        try:
            if chain_name == 'ethereum':
                # Use Web3 to get gas price from Sepolia RPC
                if 'ethereum' not in self.web3_clients:
                    self.web3_clients['ethereum'] = Web3(Web3.HTTPProvider(self.rpc_endpoints['ethereum']))
                
                web3 = self.web3_clients['ethereum']
                gas_price = web3.eth.gas_price
                return float(gas_price) / 10**9  # Convert to Gwei
            else:
                # Simulate gas fees for other chains
                gas_map = {
                    'bitcoin': 50.0,    # BTC transaction fee
                    'polygon': 30.0     # MATIC gas fee
                }
                return gas_map.get(chain_name, 20.0)
                
        except Exception as e:
            print(f"❌ Error getting gas fee for {chain_name}: {e}")
            return 20.0
    
    async def get_transaction_count(self, chain_name: str) -> int:
        """Get transaction count for a blockchain"""
        try:
            if chain_name == 'ethereum':
                if 'ethereum' not in self.web3_clients:
                    self.web3_clients['ethereum'] = Web3(Web3.HTTPProvider(self.rpc_endpoints['ethereum']))
                
                web3 = self.web3_clients['ethereum']
                latest_block = web3.eth.get_block('latest')
                return len(latest_block.transactions)
            else:
                # Simulate transaction counts
                tx_map = {
                    'bitcoin': 2000,
                    'polygon': 5000
                }
                return tx_map.get(chain_name, 1000)
                
        except Exception as e:
            print(f"❌ Error getting transaction count for {chain_name}: {e}")
            return 1000
    
    async def get_latest_block_number(self, chain_name: str) -> int:
        """Get latest block number for a blockchain"""
        try:
            if chain_name == 'ethereum':
                if 'ethereum' not in self.web3_clients:
                    self.web3_clients['ethereum'] = Web3(Web3.HTTPProvider(self.rpc_endpoints['ethereum']))
                
                web3 = self.web3_clients['ethereum']
                return web3.eth.block_number
            else:
                # Simulate block numbers
                block_map = {
                    'bitcoin': 800000,
                    'polygon': 50000000
                }
                return block_map.get(chain_name, 1000000)
                
        except Exception as e:
            print(f"❌ Error getting block number for {chain_name}: {e}")
            return 1000000
    
    async def get_block_time(self, chain_name: str) -> float:
        """Get average block time for a blockchain"""
        try:
            # Known block times
            block_time_map = {
                'ethereum': 12.0,   # 12 seconds
                'bitcoin': 600.0,   # 10 minutes
                'polygon': 2.0      # 2 seconds
            }
            return block_time_map.get(chain_name, 10.0)
            
        except Exception as e:
            print(f"❌ Error getting block time for {chain_name}: {e}")
            return 10.0
    
    async def get_network_hash_rate(self, chain_name: str) -> float:
        """Get network hash rate for a blockchain"""
        try:
            # Simulate hash rates
            hash_rate_map = {
                'ethereum': 1000000000000000000,  # 1 EH/s
                'bitcoin': 500000000000000000,    # 500 PH/s
                'polygon': 10000000000000000      # 10 TH/s
            }
            return hash_rate_map.get(chain_name, 1000000000000000)
            
        except Exception as e:
            print(f"❌ Error getting hash rate for {chain_name}: {e}")
            return 1000000000000000
