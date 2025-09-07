"""
Data types and models for the Golem-powered blockchain audio aggregator
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

@dataclass
class ChainInstrument:
    """Represents a blockchain and its associated musical instrument"""
    chain_name: str
    instrument_type: str
    rpc_node_url: str
    sound_profile: str
    created_at: datetime

class BlockchainMetric(BaseModel):
    """Represents raw blockchain data"""
    chain_name: str
    timestamp: datetime
    price: float
    volume: float
    gas_fee: float
    number_of_transactions: int
    fee_per_transaction: float
    number_of_blocks: int
    block_time: float
    network_hash_rate: float

class AnalyzedMetric(BaseModel):
    """Represents calculated KPIs from blockchain data"""
    chain_name: str
    timestamp: datetime
    price_change_percentage: float
    gas_fee_trend: float
    transaction_volume_change: float
    block_production_rate: float
    network_activity_score: float
    volatility_index: float
    liquidity_score: float

class MusicalParameters(BaseModel):
    """Represents musical characteristics derived from KPIs"""
    tempo: int
    base_note: str
    rhythm_pattern: str
    gain: float
    sound_profile: str
    scale: str
    complexity: int
    effects: List[str]
    instrument_type: str

class StrudelTrack(BaseModel):
    """Represents a generated Strudel audio pattern"""
    id: str
    timestamp: datetime
    chain_name: str
    strudel_code_string: str
    source_kpis: AnalyzedMetric
    musical_parameters: MusicalParameters
    created_at: datetime

class OrchestraTable(BaseModel):
    """Container for orchestra table data"""
    entries: List[ChainInstrument]
    created_at: datetime
    version: str = "1.0"

class BlockchainDataTable(BaseModel):
    """Container for blockchain data"""
    metrics: List[BlockchainMetric]
    created_at: datetime
    version: str = "1.0"

class StrudelAudioTable(BaseModel):
    """Container for Strudel audio tracks"""
    tracks: List[StrudelTrack]
    created_at: datetime
    version: str = "1.0"
