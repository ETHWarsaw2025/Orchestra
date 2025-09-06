"""
Strudel audio pattern generator based on blockchain KPIs
"""

import random
from datetime import datetime
from typing import List
from models import AnalyzedMetric, MusicalParameters, StrudelTrack, ChainInstrument

class StrudelGenerator:
    """Generates Strudel audio patterns based on blockchain KPIs"""
    
    def __init__(self):
        self.note_scales = {
            'C:major': ['c', 'd', 'e', 'f', 'g', 'a', 'b'],
            'D:mixolydian': ['d', 'e', 'f#', 'g', 'a', 'b', 'c'],
            'G:minor': ['g', 'a', 'bb', 'c', 'd', 'eb', 'f'],
            'F:major': ['f', 'g', 'a', 'bb', 'c', 'd', 'e']
        }
        
        self.rhythm_patterns = {
            'simple': ['bd', 'sd', 'bd', 'lt'],
            'complex': ['bd sd bd lt', 'hh*16'],
            'sparse': ['bd', 'hh', 'lt'],
            'dense': ['bd sd bd lt,hh*16', 'cp <- cp*2 - cp*4>']
        }
        
        self.effects = ['gain', 'lpf', 'hpf', 'reverb', 'delay', 'distort', 'clip']
    
    def calculate_tempo(self, price_change: float, base_tempo: int = 120) -> int:
        """Calculate tempo based on price change"""
        # Price change affects tempo: positive = faster, negative = slower
        tempo_modifier = int(price_change * 2)  # 1% price change = 2 BPM change
        return max(60, min(200, base_tempo + tempo_modifier))
    
    def calculate_base_note(self, gas_fee_trend: float) -> str:
        """Calculate base note based on gas fee trend"""
        # Higher gas fees = higher notes
        if gas_fee_trend > 50:
            return 'g4'
        elif gas_fee_trend > 20:
            return 'c4'
        elif gas_fee_trend > -20:
            return 'g3'
        else:
            return 'c3'
    
    def calculate_rhythm_pattern(self, volume_change: float) -> str:
        """Calculate rhythm pattern based on volume change"""
        if volume_change > 50:
            return 'complex'
        elif volume_change > 20:
            return 'dense'
        elif volume_change > -20:
            return 'simple'
        else:
            return 'sparse'
    
    def calculate_gain(self, gas_fee_trend: float) -> float:
        """Calculate gain based on gas fee trend"""
        # Higher gas fees = higher gain
        base_gain = 0.3
        gain_modifier = min(gas_fee_trend / 100, 0.5)  # Max 0.5 additional gain
        return max(0.1, min(1.0, base_gain + gain_modifier))
    
    def calculate_scale(self, block_production_rate: float) -> str:
        """Calculate scale based on block production rate"""
        if block_production_rate > 300:  # High block rate
            return 'C:major'
        elif block_production_rate > 100:
            return 'D:mixolydian'
        elif block_production_rate > 50:
            return 'G:minor'
        else:
            return 'F:major'
    
    def calculate_complexity(self, activity_score: float) -> int:
        """Calculate complexity based on activity score"""
        return min(10, max(1, int(activity_score / 10)))
    
    def calculate_effects(self, volatility: float, gas_trend: float) -> List[str]:
        """Calculate effects based on volatility and gas trends"""
        effects = []
        
        if volatility > 50:
            effects.extend(['distort', 'reverb'])
        elif volatility > 20:
            effects.append('delay')
        
        if gas_trend > 30:
            effects.extend(['clip', 'lpf'])
        elif gas_trend < -30:
            effects.append('hpf')
        
        return effects[:3]  # Limit to 3 effects
    
    def generate_musical_parameters(self, analyzed_metric: AnalyzedMetric, instrument: ChainInstrument) -> MusicalParameters:
        """Generate musical parameters from analyzed metrics"""
        tempo = self.calculate_tempo(analyzed_metric.price_change_percentage)
        base_note = self.calculate_base_note(analyzed_metric.gas_fee_trend)
        rhythm_type = self.calculate_rhythm_pattern(analyzed_metric.transaction_volume_change)
        rhythm_pattern = random.choice(self.rhythm_patterns[rhythm_type])
        gain = self.calculate_gain(analyzed_metric.gas_fee_trend)
        scale = self.calculate_scale(analyzed_metric.block_production_rate)
        complexity = self.calculate_complexity(analyzed_metric.network_activity_score)
        effects = self.calculate_effects(analyzed_metric.volatility_index, analyzed_metric.gas_fee_trend)
        
        return MusicalParameters(
            tempo=tempo,
            base_note=base_note,
            rhythm_pattern=rhythm_pattern,
            gain=gain,
            sound_profile=instrument.sound_profile,
            scale=scale,
            complexity=complexity,
            effects=effects,
            instrument_type=instrument.instrument_type
        )
    
    def generate_strudel_code(self, musical_params: MusicalParameters, instrument: ChainInstrument) -> str:
        """Generate Strudel code from musical parameters"""
        
        # Base pattern with dynamic parameters
        strudel_code = f"""
// Generated by Golem Blockchain Audio Aggregator
// Timestamp: {datetime.now().isoformat()}
// Chain: {instrument.chain_name}
// Instrument: {instrument.instrument_type}

samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    s("{musical_params.rhythm_pattern}").gain({musical_params.gain:.2f}),
    s("lt sd, cp <- cp*2 - cp*4>").gain({musical_params.gain * 0.8:.2f}),
    samples({{
        '{instrument.sound_profile}': {{
            'g2': '{instrument.sound_profile}/004_Mighty%20{instrument.instrument_type.title()}%20G2.wav',
            'g3': '{instrument.sound_profile}/005_Mighty%20{instrument.instrument_type.title()}%20G3.wav',
            'g4': '{instrument.sound_profile}/006_Mighty%20{instrument.instrument_type.title()}%20G4.wav',
        }},
    }}, 'github:tidalcycles/dirt-samples'),
    
    n("{musical_params.base_note}!2 <bb2 c3>!2, <c4@3 [<eb4 bb3> g4 f4]>")
    .s('{instrument.sound_profile}')
    .clip({musical_params.complexity})
    .gain({musical_params.gain:.2f}),
    
    n("<0 -3>, 2 4 <[6,8] [7, 10] [10, 13]>")
    .scale("{musical_params.scale}/4")
    .sound("piano").gain(0.2),
    
    n("<[c2 c3]*4 [bb1 bb2]*4 [f2 f3]*4 [eb2 eb3]*4>")
    .sound("gm_synth_bass_1")
    .lpf(800).gain({musical_params.gain * 0.8:.2f}),
    
    n(`<
        [~ 0] 2 [0 2] [~ 2]
        [~ 0] 1 [0 1] [~ 1]
        [~ 0] 3 [0 3] [~ 3]
        [~ 0] 2 [0 2] [~ 2]
    >*4`).scale("{musical_params.scale}:minor")
    .sound("gm_synth_strings_2").gain({musical_params.gain * 0.8:.2f}),
    
    note("48 67 63 [62, 58]")
    .sound("piano, gm_electric_guitar_muted").gain({musical_params.gain:.2f})
)
"""
        
        # Add effects if any
        if musical_params.effects:
            effects_code = "\n".join([f".{effect}()" for effect in musical_params.effects])
            strudel_code += f"\n// Effects: {', '.join(musical_params.effects)}\n{effects_code}"
        
        return strudel_code.strip()
    
    def generate_track(self, analyzed_metric: AnalyzedMetric, instrument: ChainInstrument) -> StrudelTrack:
        """Generate a complete Strudel track from analyzed metrics"""
        
        # Generate musical parameters
        musical_params = self.generate_musical_parameters(analyzed_metric, instrument)
        
        # Generate Strudel code
        strudel_code = self.generate_strudel_code(musical_params, instrument)
        
        # Create track ID
        track_id = f"{analyzed_metric.chain_name}_{int(datetime.now().timestamp())}"
        
        return StrudelTrack(
            id=track_id,
            timestamp=analyzed_metric.timestamp,
            chain_name=analyzed_metric.chain_name,
            strudel_code_string=strudel_code,
            source_kpis=analyzed_metric,
            musical_parameters=musical_params,
            created_at=datetime.now()
        )
    
    def generate_multi_chain_track(self, analyzed_metrics: List[AnalyzedMetric], instruments: List[ChainInstrument]) -> StrudelTrack:
        """Generate a track that combines multiple chains"""
        
        if not analyzed_metrics or not instruments:
            raise ValueError("Need at least one analyzed metric and instrument")
        
        # Use the most active chain as primary
        primary_metric = max(analyzed_metrics, key=lambda x: x.network_activity_score)
        primary_instrument = next((i for i in instruments if i.chain_name == primary_metric.chain_name), instruments[0])
        
        # Generate base parameters from primary chain
        musical_params = self.generate_musical_parameters(primary_metric, primary_instrument)
        
        # Create multi-chain Strudel code
        track_id = f"multi_chain_{int(datetime.now().timestamp())}"
        
        # Combine all chains in the pattern
        chain_names = [m.chain_name for m in analyzed_metrics]
        combined_code = f"""
// Multi-Chain Track Generated by Golem Blockchain Audio Aggregator
// Chains: {', '.join(chain_names)}
// Timestamp: {datetime.now().isoformat()}

samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    // Primary chain: {primary_metric.chain_name}
    s("{musical_params.rhythm_pattern}").gain({musical_params.gain:.2f}),
    
    // Additional chains
    {self._generate_additional_chain_patterns(analyzed_metrics[1:], instruments[1:])}
    
    // Combined harmony
    n("{musical_params.base_note}!2 <bb2 c3>!2, <c4@3 [<eb4 bb3> g4 f4]>")
    .s('{primary_instrument.sound_profile}')
    .scale("{musical_params.scale}/4")
    .gain({musical_params.gain:.2f})
)
"""
        
        return StrudelTrack(
            id=track_id,
            timestamp=datetime.now(),
            chain_name="multi_chain",
            strudel_code_string=combined_code.strip(),
            source_kpis=primary_metric,
            musical_parameters=musical_params,
            created_at=datetime.now()
        )
    
    def _generate_additional_chain_patterns(self, metrics: List[AnalyzedMetric], instruments: List[ChainInstrument]) -> str:
        """Generate additional chain patterns for multi-chain tracks"""
        patterns = []
        
        for metric, instrument in zip(metrics, instruments):
            pattern = f"""
    // {metric.chain_name} chain
    s("bd sd").gain({metric.network_activity_score / 100:.2f}),
    n("{self.calculate_base_note(metric.gas_fee_trend)}")
    .s('{instrument.sound_profile}')
    .gain({self.calculate_gain(metric.gas_fee_trend):.2f}),"""
            patterns.append(pattern)
        
        return "\n".join(patterns)
