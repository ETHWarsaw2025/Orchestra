#!/usr/bin/env python3
"""
Real blockchain data fetcher for the last 10 blocks
Fetches data from Ethereum, Optimism, Polygon, and Base networks
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from models import AnalyzedMetric, ChainInstrument
from strudel_generator import StrudelGenerator

class BlockchainDataFetcher:
    """Fetches real blockchain data from multiple networks"""
    
    def __init__(self):
        self.rpc_urls = {
            "ethereum": "https://eth-mainnet.g.alchemy.com/v2/demo",  # Free tier
            "optimism": "https://mainnet.optimism.io",  # Public RPC
            "polygon": "https://polygon-rpc.com",  # Public RPC
            "base": "https://mainnet.base.org"  # Public RPC
        }
        
        self.strudel_generator = StrudelGenerator()
        
    def get_latest_block_number(self, chain: str) -> Optional[int]:
        """Get the latest block number for a chain"""
        try:
            if chain == "ethereum":
                response = requests.post(
                    self.rpc_urls[chain],
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_blockNumber",
                        "params": [],
                        "id": 1
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return int(data.get("result", "0x0"), 16)
            
            elif chain == "optimism":
                response = requests.post(
                    self.rpc_urls[chain],
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_blockNumber",
                        "params": [],
                        "id": 1
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return int(data.get("result", "0x0"), 16)
            
            elif chain == "polygon":
                response = requests.post(
                    self.rpc_urls[chain],
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_blockNumber",
                        "params": [],
                        "id": 1
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return int(data.get("result", "0x0"), 16)
            
            elif chain == "base":
                response = requests.post(
                    self.rpc_urls[chain],
                    json={
                        "jsonrpc": "2.0",
                        "method": "eth_blockNumber",
                        "params": [],
                        "id": 1
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    data = response.json()
                    return int(data.get("result", "0x0"), 16)
                    
        except Exception as e:
            print(f"❌ Error fetching block number for {chain}: {e}")
            
        return None
    
    def get_block_data(self, chain: str, block_number: int) -> Optional[Dict]:
        """Get block data for a specific block number"""
        try:
            response = requests.post(
                self.rpc_urls[chain],
                json={
                    "jsonrpc": "2.0",
                    "method": "eth_getBlockByNumber",
                    "params": [hex(block_number), True],  # True for full transaction details
                    "id": 1
                },
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("result")
                
        except Exception as e:
            print(f"❌ Error fetching block {block_number} for {chain}: {e}")
            
        return None
    
    def analyze_block_data(self, block_data: Dict, chain: str) -> Dict[str, Any]:
        """Analyze block data to extract musical parameters"""
        if not block_data:
            return {}
        
        # Extract basic metrics
        timestamp = int(block_data.get("timestamp", "0x0"), 16)
        gas_used = int(block_data.get("gasUsed", "0x0"), 16)
        gas_limit = int(block_data.get("gasLimit", "0x0"), 16)
        transaction_count = len(block_data.get("transactions", []))
        block_size = len(str(block_data))
        
        # Calculate gas efficiency
        gas_efficiency = (gas_used / gas_limit) if gas_limit > 0 else 0
        
        # Calculate transaction density
        tx_density = transaction_count / max(block_size, 1) * 1000
        
        # Calculate activity score based on transactions and gas usage
        activity_score = min(100, (transaction_count * 2) + (gas_efficiency * 50))
        
        # Calculate volatility based on gas usage variation
        volatility = min(100, abs(gas_efficiency - 0.5) * 200)
        
        # Calculate liquidity score based on transaction count
        liquidity_score = min(100, transaction_count * 5)
        
        return {
            "block_number": int(block_data.get("number", "0x0"), 16),
            "timestamp": timestamp,
            "gas_used": gas_used,
            "gas_limit": gas_limit,
            "gas_efficiency": gas_efficiency,
            "transaction_count": transaction_count,
            "block_size": block_size,
            "tx_density": tx_density,
            "activity_score": activity_score,
            "volatility": volatility,
            "liquidity_score": liquidity_score,
            "chain": chain
        }
    
    def fetch_last_10_blocks(self, chain: str) -> List[Dict[str, Any]]:
        """Fetch and analyze the last 10 blocks for a chain"""
        print(f"🔍 Fetching last 10 blocks for {chain.upper()}...")
        
        # Get latest block number
        latest_block = self.get_latest_block_number(chain)
        if not latest_block:
            print(f"❌ Could not fetch latest block for {chain}")
            return []
        
        print(f"📊 Latest block: {latest_block}")
        
        # Fetch last 10 blocks
        blocks_data = []
        for i in range(10):
            block_number = latest_block - i
            print(f"  📦 Fetching block {block_number}...")
            
            block_data = self.get_block_data(chain, block_number)
            if block_data:
                analyzed = self.analyze_block_data(block_data, chain)
                if analyzed:
                    blocks_data.append(analyzed)
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        
        print(f"✅ Fetched {len(blocks_data)} blocks for {chain}")
        return blocks_data
    
    def create_analyzed_metric_from_blocks(self, blocks_data: List[Dict], chain: str) -> AnalyzedMetric:
        """Create an AnalyzedMetric from the last 10 blocks data"""
        if not blocks_data:
            # Fallback to default values
            return AnalyzedMetric(
                chain_name=chain,
                timestamp=datetime.now(),
                price_change_percentage=0.0,
                gas_fee_trend=0.0,
                transaction_volume_change=0.0,
                block_production_rate=0.0,
                network_activity_score=50.0,
                volatility_index=50.0,
                liquidity_score=50.0
            )
        
        # Calculate averages and trends
        avg_activity = sum(block["activity_score"] for block in blocks_data) / len(blocks_data)
        avg_volatility = sum(block["volatility"] for block in blocks_data) / len(blocks_data)
        avg_liquidity = sum(block["liquidity_score"] for block in blocks_data) / len(blocks_data)
        avg_tx_count = sum(block["transaction_count"] for block in blocks_data) / len(blocks_data)
        avg_gas_efficiency = sum(block["gas_efficiency"] for block in blocks_data) / len(blocks_data)
        
        # Calculate trends (comparing first 5 vs last 5 blocks)
        if len(blocks_data) >= 10:
            first_half_activity = sum(block["activity_score"] for block in blocks_data[:5]) / 5
            second_half_activity = sum(block["activity_score"] for block in blocks_data[5:]) / 5
            activity_trend = ((second_half_activity - first_half_activity) / first_half_activity) * 100
            
            first_half_tx = sum(block["transaction_count"] for block in blocks_data[:5]) / 5
            second_half_tx = sum(block["transaction_count"] for block in blocks_data[5:]) / 5
            tx_trend = ((second_half_tx - first_half_tx) / first_half_tx) * 100 if first_half_tx > 0 else 0
        else:
            activity_trend = 0.0
            tx_trend = 0.0
        
        # Calculate block production rate (blocks per minute)
        if len(blocks_data) >= 2:
            time_diff = blocks_data[0]["timestamp"] - blocks_data[-1]["timestamp"]
            block_production_rate = (len(blocks_data) - 1) / (time_diff / 60) if time_diff > 0 else 0
        else:
            block_production_rate = 0.0
        
        return AnalyzedMetric(
            chain_name=chain,
            timestamp=datetime.now(),
            price_change_percentage=activity_trend,  # Use activity trend as price change proxy
            gas_fee_trend=tx_trend,  # Use transaction trend as gas fee trend
            transaction_volume_change=tx_trend,
            block_production_rate=block_production_rate,
            network_activity_score=avg_activity,
            volatility_index=avg_volatility,
            liquidity_score=avg_liquidity
        )
    
    def fetch_all_chains_data(self) -> Dict[str, Any]:
        """Fetch data for all chains and generate audio tracks"""
        print("🎵 Fetching Real Blockchain Data for Audio Generation")
        print("=" * 60)
        
        all_data = {}
        analyzed_metrics = {}
        chain_instruments = {}
        
        # Define chain instruments
        chain_instruments = {
            "ethereum": ChainInstrument(
                chain_name="ethereum",
                instrument_type="synthesizer",
                rpc_node_url=self.rpc_urls["ethereum"],
                sound_profile="gm_synth_lead",
                created_at=datetime.now()
            ),
            "optimism": ChainInstrument(
                chain_name="optimism",
                instrument_type="lead",
                rpc_node_url=self.rpc_urls["optimism"],
                sound_profile="gm_lead_6_voice",
                created_at=datetime.now()
            ),
            "polygon": ChainInstrument(
                chain_name="polygon",
                instrument_type="drum",
                rpc_node_url=self.rpc_urls["polygon"],
                sound_profile="RolandTR909",
                created_at=datetime.now()
            ),
            "base": ChainInstrument(
                chain_name="base",
                instrument_type="bass",
                rpc_node_url=self.rpc_urls["base"],
                sound_profile="gm_acoustic_bass",
                created_at=datetime.now()
            )
        }
        
        # Fetch data for each chain
        for chain in ["ethereum", "optimism", "polygon", "base"]:
            print(f"\n🔗 Processing {chain.upper()}...")
            
            # Fetch last 10 blocks
            blocks_data = self.fetch_last_10_blocks(chain)
            all_data[chain] = blocks_data
            
            # Create analyzed metric
            analyzed_metric = self.create_analyzed_metric_from_blocks(blocks_data, chain)
            analyzed_metrics[chain] = analyzed_metric
            
            print(f"  📊 Activity Score: {analyzed_metric.network_activity_score:.1f}")
            print(f"  📈 Volatility: {analyzed_metric.volatility_index:.1f}")
            print(f"  💧 Liquidity: {analyzed_metric.liquidity_score:.1f}")
            print(f"  🔄 TX Trend: {analyzed_metric.transaction_volume_change:.1f}%")
        
        # Generate audio tracks
        print(f"\n🎵 Generating Audio Tracks from Real Data")
        print("-" * 40)
        
        strudel_tracks = []
        
        # Generate single-chain tracks
        for chain in ["ethereum", "optimism", "polygon", "base"]:
            print(f"🎼 Generating {chain.upper()} track...")
            
            track = self.strudel_generator.generate_track(
                analyzed_metrics[chain], 
                chain_instruments[chain]
            )
            
            strudel_tracks.append({
                "id": f"{chain}_real_data_{int(datetime.now().timestamp())}",
                "chain": chain,
                "timestamp": track.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": track.musical_parameters.tempo,
                "instrument": track.musical_parameters.instrument_type,
                "effects": ", ".join(track.musical_parameters.effects) if track.musical_parameters.effects else "none",
                "code": track.strudel_code_string,
                "track_obj": track
            })
            
            print(f"  ✅ Generated: {track.id}")
            print(f"  🎵 Tempo: {track.musical_parameters.tempo} BPM")
            print(f"  🎼 Scale: {track.musical_parameters.scale}")
        
        # Generate multi-chain track
        print(f"\n🔗 Generating Multi-Chain Jam Session...")
        multi_track = self.strudel_generator.generate_multi_chain_track(
            list(analyzed_metrics.values()),
            list(chain_instruments.values())
        )
        
        strudel_tracks.append({
            "id": f"multi_chain_real_data_{int(datetime.now().timestamp())}",
            "chain": "multi_real",
            "timestamp": multi_track.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "tempo": multi_track.musical_parameters.tempo,
            "instrument": "orchestra",
            "effects": ", ".join(multi_track.musical_parameters.effects) if multi_track.musical_parameters.effects else "none",
            "code": multi_track.strudel_code_string,
            "track_obj": multi_track
        })
        
        print(f"  ✅ Generated multi-chain track: {multi_track.id}")
        print(f"  🎵 Tempo: {multi_track.musical_parameters.tempo} BPM")
        
        # Save all data to JSON (remove track_obj to avoid serialization issues)
        serializable_tracks = []
        for track in strudel_tracks:
            serializable_track = {
                "id": track["id"],
                "chain": track["chain"],
                "timestamp": track["timestamp"],
                "tempo": track["tempo"],
                "instrument": track["instrument"],
                "effects": track["effects"],
                "code": track["code"]
            }
            serializable_tracks.append(serializable_track)
        
        output_data = {
            "blockchain_data": all_data,
            "analyzed_metrics": {
                chain: {
                    "chain_name": metric.chain_name,
                    "timestamp": metric.timestamp.isoformat(),
                    "price_change_percentage": metric.price_change_percentage,
                    "gas_fee_trend": metric.gas_fee_trend,
                    "transaction_volume_change": metric.transaction_volume_change,
                    "block_production_rate": metric.block_production_rate,
                    "network_activity_score": metric.network_activity_score,
                    "volatility_index": metric.volatility_index,
                    "liquidity_score": metric.liquidity_score
                }
                for chain, metric in analyzed_metrics.items()
            },
            "strudel_tracks": serializable_tracks,
            "generated_at": datetime.now().isoformat()
        }
        
        # Save to JSON file
        with open("real_blockchain_audio_data.json", "w") as f:
            json.dump(output_data, f, indent=2)
        
        print(f"\n💾 Data saved to real_blockchain_audio_data.json")
        print(f"🎵 Generated {len(strudel_tracks)} audio tracks from real blockchain data!")
        
        return output_data

def main():
    """Main function to fetch data and generate tracks"""
    fetcher = BlockchainDataFetcher()
    
    try:
        data = fetcher.fetch_all_chains_data()
        
        print(f"\n🎉 Success! Generated audio tracks from real blockchain data:")
        print(f"📊 Chains: {', '.join(data['analyzed_metrics'].keys())}")
        print(f"🎵 Tracks: {len(data['strudel_tracks'])}")
        print(f"💾 Data saved to: real_blockchain_audio_data.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
