"""
Main orchestrator that coordinates all processes in the blockchain audio aggregator
"""

import asyncio
import uuid
from datetime import datetime
from typing import List, Optional

from models import ChainInstrument, BlockchainMetric, AnalyzedMetric, StrudelTrack
from golem_storage import GolemStorage
from blockchain_client import BlockchainClient
from data_analyzer import DataAnalyzer
from strudel_generator import StrudelGenerator

class BlockchainAudioOrchestrator:
    """Main orchestrator for the blockchain audio aggregator pipeline"""
    
    def __init__(self):
        self.golem_storage = GolemStorage()
        self.blockchain_client = BlockchainClient()
        self.data_analyzer = DataAnalyzer()
        self.strudel_generator = StrudelGenerator()
        
        # Initialize orchestra table
        self.orchestra_table = self._create_initial_orchestra_table()
    
    def _create_initial_orchestra_table(self) -> List[ChainInstrument]:
        """Create initial orchestra table with blockchain-instrument mappings"""
        return [
            ChainInstrument(
                chain_name="ethereum",
                instrument_type="guitar",
                rpc_node_url="https://lb.drpc.org/sepolia/AplHGB2v9khYpYVNxc5za0FxucDEi1sR8IqgqhnKxixj",
                sound_profile="moog",
                created_at=datetime.now()
            ),
            ChainInstrument(
                chain_name="bitcoin",
                instrument_type="drum",
                rpc_node_url="https://bitcoin-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
                sound_profile="bd",
                created_at=datetime.now()
            ),
            ChainInstrument(
                chain_name="polygon",
                instrument_type="bass",
                rpc_node_url="https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
                sound_profile="gm_synth_bass_1",
                created_at=datetime.now()
            )
        ]
    
    async def run_pipeline(self):
        """Run the complete pipeline"""
        print("🚀 Starting Blockchain Audio Aggregator Pipeline")
        print("=" * 60)
        
        try:
            # Step 1: Store Orchestra Table on Golem
            await self._step_1_store_orchestra_table()
            
            # Step 2: Retrieve Blockchain Data
            blockchain_metrics = await self._step_2_retrieve_blockchain_data()
            
            # Step 3: Store Blockchain Data on Golem
            await self._step_3_store_blockchain_data(blockchain_metrics)
            
            # Step 4: Analyze Data with KPIs
            analyzed_metrics = await self._step_4_analyze_data(blockchain_metrics)
            
            # Step 5: Generate Strudel Audio Tracks
            strudel_tracks = await self._step_5_generate_strudel_tracks(analyzed_metrics)
            
            # Step 6: Store Strudel Audio Table
            await self._step_6_store_strudel_tracks(strudel_tracks)
            
            # Display results
            await self._display_results(analyzed_metrics, strudel_tracks)
            
        except Exception as e:
            print(f"❌ Pipeline error: {e}")
            raise
        finally:
            await self.golem_storage.disconnect()
            await self.blockchain_client.close()
    
    async def _step_1_store_orchestra_table(self):
        """Step 1: Store Orchestra Table on Golem"""
        print("\n📋 Step 1: Storing Orchestra Table on Golem")
        print("-" * 40)
        
        # Connect to Golem
        if not await self.golem_storage.connect():
            raise Exception("Failed to connect to Golem DB")
        
        # Store orchestra table
        success = await self.golem_storage.store_orchestra_table(self.orchestra_table)
        if not success:
            raise Exception("Failed to store orchestra table")
        
        print(f"✅ Stored orchestra table with {len(self.orchestra_table)} entries")
        for entry in self.orchestra_table:
            print(f"   - {entry.chain_name} -> {entry.instrument_type} ({entry.sound_profile})")
    
    async def _step_2_retrieve_blockchain_data(self) -> List[BlockchainMetric]:
        """Step 2: Retrieve Blockchain Data"""
        print("\n🔍 Step 2: Retrieving Blockchain Data")
        print("-" * 40)
        
        blockchain_metrics = []
        
        async with self.blockchain_client:
            for instrument in self.orchestra_table:
                print(f"   📊 Fetching data for {instrument.chain_name}...")
                
                try:
                    # Fetch all metrics for this chain
                    price = await self.blockchain_client.get_current_price(instrument.chain_name)
                    volume = await self.blockchain_client.get_volume(instrument.chain_name)
                    gas_fee = await self.blockchain_client.get_gas_fee(instrument.chain_name)
                    tx_count = await self.blockchain_client.get_transaction_count(instrument.chain_name)
                    block_number = await self.blockchain_client.get_latest_block_number(instrument.chain_name)
                    block_time = await self.blockchain_client.get_block_time(instrument.chain_name)
                    hash_rate = await self.blockchain_client.get_network_hash_rate(instrument.chain_name)
                    
                    # Calculate fee per transaction
                    fee_per_tx = gas_fee / tx_count if tx_count > 0 else 0
                    
                    metric = BlockchainMetric(
                        chain_name=instrument.chain_name,
                        timestamp=datetime.now(),
                        price=price,
                        volume=volume,
                        gas_fee=gas_fee,
                        number_of_transactions=tx_count,
                        fee_per_transaction=fee_per_tx,
                        number_of_blocks=block_number,
                        block_time=block_time,
                        network_hash_rate=hash_rate
                    )
                    
                    blockchain_metrics.append(metric)
                    print(f"      ✅ {instrument.chain_name}: ${price:.2f}, {tx_count} txs, {gas_fee:.2f} gas")
                    
                except Exception as e:
                    print(f"      ❌ Error fetching {instrument.chain_name}: {e}")
                    continue
        
        print(f"✅ Retrieved data for {len(blockchain_metrics)} chains")
        return blockchain_metrics
    
    async def _step_3_store_blockchain_data(self, metrics: List[BlockchainMetric]):
        """Step 3: Store Blockchain Data on Golem"""
        print("\n💾 Step 3: Storing Blockchain Data on Golem")
        print("-" * 40)
        
        success = await self.golem_storage.store_blockchain_data(metrics)
        if not success:
            raise Exception("Failed to store blockchain data")
        
        print(f"✅ Stored {len(metrics)} blockchain metrics")
    
    async def _step_4_analyze_data(self, metrics: List[BlockchainMetric]) -> List[AnalyzedMetric]:
        """Step 4: Analyze Data with KPIs"""
        print("\n📊 Step 4: Analyzing Data with KPIs")
        print("-" * 40)
        
        # Add historical data for analysis
        self.data_analyzer.add_historical_data(metrics)
        
        analyzed_metrics = []
        for metric in metrics:
            analyzed = self.data_analyzer.analyze_metrics(metric, metric.chain_name)
            analyzed_metrics.append(analyzed)
            
            print(f"   📈 {metric.chain_name}:")
            print(f"      Price Change: {analyzed.price_change_percentage:.2f}%")
            print(f"      Gas Trend: {analyzed.gas_fee_trend:.2f}%")
            print(f"      Volume Change: {analyzed.transaction_volume_change:.2f}%")
            print(f"      Activity Score: {analyzed.network_activity_score:.1f}/100")
            print(f"      Volatility: {analyzed.volatility_index:.2f}")
        
        # Get analysis summary
        summary = self.data_analyzer.get_analysis_summary(analyzed_metrics)
        print(f"\n📋 Analysis Summary:")
        print(f"   Most Active Chain: {summary.get('most_active_chain', 'N/A')}")
        print(f"   Most Volatile Chain: {summary.get('most_volatile_chain', 'N/A')}")
        print(f"   Average Activity Score: {summary.get('avg_activity_score', 0):.1f}")
        
        return analyzed_metrics
    
    async def _step_5_generate_strudel_tracks(self, analyzed_metrics: List[AnalyzedMetric]) -> List[StrudelTrack]:
        """Step 5: Generate Strudel Audio Tracks"""
        print("\n🎵 Step 5: Generating Strudel Audio Tracks")
        print("-" * 40)
        
        strudel_tracks = []
        
        # Generate individual tracks for each chain
        for metric in analyzed_metrics:
            # Find corresponding instrument
            instrument = next((i for i in self.orchestra_table if i.chain_name == metric.chain_name), None)
            if not instrument:
                print(f"   ⚠️  No instrument found for {metric.chain_name}")
                continue
            
            try:
                track = self.strudel_generator.generate_track(metric, instrument)
                strudel_tracks.append(track)
                
                print(f"   🎼 {metric.chain_name} track generated:")
                print(f"      Tempo: {track.musical_parameters.tempo} BPM")
                print(f"      Base Note: {track.musical_parameters.base_note}")
                print(f"      Scale: {track.musical_parameters.scale}")
                print(f"      Effects: {', '.join(track.musical_parameters.effects)}")
                
            except Exception as e:
                print(f"   ❌ Error generating track for {metric.chain_name}: {e}")
                continue
        
        # Generate multi-chain track if we have multiple chains
        if len(analyzed_metrics) > 1:
            try:
                multi_track = self.strudel_generator.generate_multi_chain_track(
                    analyzed_metrics, self.orchestra_table
                )
                strudel_tracks.append(multi_track)
                print(f"   🎼 Multi-chain track generated with {len(analyzed_metrics)} chains")
            except Exception as e:
                print(f"   ❌ Error generating multi-chain track: {e}")
        
        print(f"✅ Generated {len(strudel_tracks)} Strudel tracks")
        return strudel_tracks
    
    async def _step_6_store_strudel_tracks(self, tracks: List[StrudelTrack]):
        """Step 6: Store Strudel Audio Table"""
        print("\n💾 Step 6: Storing Strudel Audio Tracks")
        print("-" * 40)
        
        for track in tracks:
            success = await self.golem_storage.store_strudel_track(track)
            if success:
                print(f"   ✅ Stored track: {track.id}")
            else:
                print(f"   ❌ Failed to store track: {track.id}")
        
        print(f"✅ Stored {len(tracks)} Strudel tracks")
    
    async def _display_results(self, analyzed_metrics: List[AnalyzedMetric], strudel_tracks: List[StrudelTrack]):
        """Display final results"""
        print("\n" + "=" * 60)
        print("🎉 PIPELINE RESULTS")
        print("=" * 60)
        
        print(f"\n📊 Blockchain Analysis:")
        for metric in analyzed_metrics:
            print(f"   {metric.chain_name}:")
            print(f"      Price Change: {metric.price_change_percentage:.2f}%")
            print(f"      Activity Score: {metric.network_activity_score:.1f}/100")
            print(f"      Volatility: {metric.volatility_index:.2f}")
        
        print(f"\n🎵 Generated Tracks:")
        for track in strudel_tracks:
            print(f"   {track.id}:")
            print(f"      Chain: {track.chain_name}")
            print(f"      Tempo: {track.musical_parameters.tempo} BPM")
            print(f"      Instrument: {track.musical_parameters.instrument_type}")
            print(f"      Effects: {', '.join(track.musical_parameters.effects)}")
        
        print(f"\n💾 Data Stored on Golem:")
        print(f"   - Orchestra Table: {len(self.orchestra_table)} entries")
        print(f"   - Blockchain Metrics: {len(analyzed_metrics)} chains")
        print(f"   - Strudel Tracks: {len(strudel_tracks)} tracks")
        
        print(f"\n✅ Pipeline completed successfully!")
        print(f"   All data has been processed and stored on Golem DB")
        print(f"   Strudel tracks are ready for playback!")
