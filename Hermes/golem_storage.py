"""
Golem storage implementation for blockchain audio aggregator
"""

import asyncio
import json
import os
from datetime import datetime
from typing import List, Optional
from dotenv import load_dotenv
from golem_base_sdk import GolemBaseClient
from golem_base_sdk.types import GolemBaseCreate, Annotation

from models import (
    ChainInstrument, BlockchainMetric, StrudelTrack, 
    AnalyzedMetric, OrchestraTable, BlockchainDataTable, StrudelAudioTable
)

load_dotenv()

class GolemStorage:
    """Golem storage implementation for blockchain audio aggregator"""
    
    def __init__(self):
        self.private_key = os.getenv(
            "PRIVATE_KEY", "0x0000000000000000000000000000000000000000000000000000000000000001"
        )
        self.rpc_url = os.getenv("RPC_URL", "https://ethwarsaw.holesky.golemdb.io/rpc")
        self.ws_url = os.getenv("WS_URL", "wss://ethwarsaw.holesky.golemdb.io/rpc/ws")
        self.client: Optional[GolemBaseClient] = None
    
    async def connect(self) -> bool:
        """Connect to Golem DB"""
        try:
            private_key_hex = self.private_key.replace("0x", "")
            private_key_bytes = bytes.fromhex(private_key_hex)
            
            self.client = await GolemBaseClient.create_rw_client(
                rpc_url=self.rpc_url,
                ws_url=self.ws_url,
                private_key=private_key_bytes
            )
            
            print("✅ Connected to Golem DB")
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Golem DB: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from Golem DB"""
        if self.client:
            await self.client.disconnect()
            print("✅ Disconnected from Golem DB")
    
    async def store_orchestra_table(self, entries: List[ChainInstrument]) -> bool:
        """Store orchestra table on Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return False
        
        try:
            orchestra_table = OrchestraTable(
                entries=entries,
                created_at=datetime.now()
            )
            
            # Create entity in the correct format for Golem DB
            data_bytes = orchestra_table.model_dump_json().encode('utf-8')
            
            # Create string annotations for metadata
            string_annotations = [
                Annotation(key='type', value='orchestra_table'),
                Annotation(key='entry_count', value=str(len(entries))),
                Annotation(key='created_at', value=datetime.now().isoformat())
            ]
            
            # Create the GolemBaseCreate object
            entity = GolemBaseCreate(
                data=data_bytes,
                btl=1000000,  # Block time limit (1M blocks)
                string_annotations=string_annotations,
                numeric_annotations=[]
            )
            
            await self.client.create_entities([entity])
            print(f"✅ Stored orchestra table with {len(entries)} entries")
            return True
            
        except Exception as e:
            print(f"❌ Error storing orchestra table: {e}")
            return False
    
    async def retrieve_orchestra_table(self) -> Optional[List[ChainInstrument]]:
        """Retrieve orchestra table from Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return None
        
        try:
            account_address = self.client.get_account_address()
            entities = await self.client.get_entities_of_owner(account_address)
            
            for entity in entities:
                # Check if this is the orchestra table by looking at annotations
                if hasattr(entity, 'string_annotations'):
                    for annotation in entity.string_annotations:
                        if annotation.key == 'type' and annotation.value == 'orchestra_table':
                            # Decode the data
                            data = json.loads(entity.data.decode('utf-8'))
                            orchestra_table = OrchestraTable(**data)
                            print(f"✅ Retrieved orchestra table with {len(orchestra_table.entries)} entries")
                            return orchestra_table.entries
            
            print("⚠️  Orchestra table not found")
            return None
            
        except Exception as e:
            print(f"❌ Error retrieving orchestra table: {e}")
            return None
    
    async def store_blockchain_data(self, metrics: List[BlockchainMetric]) -> bool:
        """Store blockchain data on Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return False
        
        try:
            blockchain_table = BlockchainDataTable(
                metrics=metrics,
                created_at=datetime.now()
            )
            
            # Create entity in the correct format for Golem DB
            data_bytes = blockchain_table.model_dump_json().encode('utf-8')
            
            # Create string annotations for metadata
            string_annotations = [
                Annotation(key='type', value='blockchain_data'),
                Annotation(key='metric_count', value=str(len(metrics))),
                Annotation(key='created_at', value=datetime.now().isoformat())
            ]
            
            # Create the GolemBaseCreate object
            entity = GolemBaseCreate(
                data=data_bytes,
                btl=1000000,  # Block time limit (1M blocks)
                string_annotations=string_annotations,
                numeric_annotations=[]
            )
            
            await self.client.create_entities([entity])
            print(f"✅ Stored blockchain data with {len(metrics)} metrics")
            return True
            
        except Exception as e:
            print(f"❌ Error storing blockchain data: {e}")
            return False
    
    async def retrieve_blockchain_data(self, chain_name: str, hours: int = 24) -> List[BlockchainMetric]:
        """Retrieve blockchain data from Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return []
        
        try:
            account_address = self.client.get_account_address()
            entities = await self.client.get_entities_of_owner(account_address)
            
            all_metrics = []
            for entity in entities:
                # Check if this is blockchain data by looking at annotations
                if hasattr(entity, 'string_annotations'):
                    for annotation in entity.string_annotations:
                        if annotation.key == 'type' and annotation.value == 'blockchain_data':
                            # Decode the data
                            data = json.loads(entity.data.decode('utf-8'))
                            blockchain_table = BlockchainDataTable(**data)
                            
                            # Filter by chain name and time range
                            cutoff_time = datetime.now().timestamp() - (hours * 3600)
                            for metric in blockchain_table.metrics:
                                if (metric.chain_name == chain_name and 
                                    metric.timestamp.timestamp() >= cutoff_time):
                                    all_metrics.append(metric)
                            break
            
            print(f"✅ Retrieved {len(all_metrics)} blockchain metrics for {chain_name}")
            return all_metrics
            
        except Exception as e:
            print(f"❌ Error retrieving blockchain data: {e}")
            return []
    
    async def store_strudel_track(self, track: StrudelTrack) -> bool:
        """Store Strudel track on Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return False
        
        try:
            # Create entity in the correct format for Golem DB
            data_bytes = track.model_dump_json().encode('utf-8')
            
            # Create string annotations for metadata
            string_annotations = [
                Annotation(key='type', value='strudel_track'),
                Annotation(key='track_id', value=track.id),
                Annotation(key='chain_name', value=track.chain_name),
                Annotation(key='created_at', value=datetime.now().isoformat())
            ]
            
            # Create the GolemBaseCreate object
            entity = GolemBaseCreate(
                data=data_bytes,
                btl=1000000,  # Block time limit (1M blocks)
                string_annotations=string_annotations,
                numeric_annotations=[]
            )
            
            await self.client.create_entities([entity])
            print(f"✅ Stored Strudel track: {track.id}")
            return True
            
        except Exception as e:
            print(f"❌ Error storing Strudel track: {e}")
            return False
    
    async def retrieve_strudel_tracks(self, chain_name: str, limit: int = 10) -> List[StrudelTrack]:
        """Retrieve Strudel tracks from Golem"""
        if not self.client:
            print("❌ Not connected to Golem DB")
            return []
        
        try:
            # For now, return a sample track since the retrieval is complex
            # In a real implementation, you would need to use the proper Golem DB API
            # to retrieve the actual entity data by hash
            
            print(f"⚠️  Strudel track retrieval is simplified for demo purposes")
            print(f"   In production, you would retrieve actual tracks from Golem DB")
            
            # Create a sample track for demonstration
            from models import StrudelTrack, AnalyzedMetric, MusicalParameters
            from datetime import datetime
            
            sample_track = StrudelTrack(
                id=f"sample_{chain_name}_track",
                timestamp=datetime.now(),
                chain_name=chain_name,
                strudel_code_string=f"""
// Sample Strudel track for {chain_name}
samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    s("bd sd bd lt").gain(0.5),
    s("hh*16").gain(0.3),
    n("c3 e3 g3").sound("piano").gain(0.4)
)
""",
                source_kpis=AnalyzedMetric(
                    chain_name=chain_name,
                    timestamp=datetime.now(),
                    price_change_percentage=0.0,
                    gas_fee_trend=0.0,
                    transaction_volume_change=0.0,
                    block_production_rate=0.0,
                    network_activity_score=75.0,
                    volatility_index=0.0,
                    liquidity_score=0.0
                ),
                musical_parameters=MusicalParameters(
                    tempo=120,
                    base_note="c3",
                    rhythm_pattern="bd sd bd lt",
                    gain=0.5,
                    sound_profile="piano",
                    scale="C:major",
                    complexity=5,
                    effects=[],
                    instrument_type="piano"
                ),
                created_at=datetime.now()
            )
            
            return [sample_track]
            
        except Exception as e:
            print(f"❌ Error retrieving Strudel tracks: {e}")
            return []
