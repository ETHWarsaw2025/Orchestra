
"""
Dynamic Strudel audio pattern generator based on blockchain KPIs
Creates complex, non-hardcoded patterns similar to strudel examples
"""

import random
import math
from datetime import datetime
from typing import List, Dict, Any, Tuple
from models import AnalyzedMetric, MusicalParameters, StrudelTrack, ChainInstrument

class StrudelGenerator:
    """Generates dynamic Strudel audio patterns based on blockchain KPIs"""
    
    def __init__(self):
        # Musical scales and modes
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
        }
        
        # Root notes
        self.root_notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
        
        # Drum samples
        self.drum_samples = {
            'kick': ['bd', 'kick', 'kick2'],
            'snare': ['sd', 'sn', 'snare'],
            'hihat': ['hh', 'hh27', 'hh808'],
            'open_hihat': ['ohh', 'oh'],
            'rim': ['rim', 'rimshot'],
            'crash': ['crash', 'crash2'],
            'ride': ['ride', 'ride2']
        }
        
        # Melodic samples
        self.melodic_samples = {
            'lead': ['gm_lead_6_voice', 'gm_lead_3_calliope', 'gm_lead_2_sawtooth'],
            'bass': ['gm_acoustic_bass', 'gm_synth_bass_1', 'gm_electric_bass_finger'],
            'pad': ['gm_synth_strings_2', 'gm_synth_pad_2_warm', 'gm_synth_pad_3_polysynth'],
            'piano': ['gm_acoustic_grand_piano', 'gm_electric_piano_1_rhodes', 'gm_electric_piano_2_chorused_rhodes'],
            'organ': ['gm_organ_1_drawbar', 'gm_organ_2_percussive', 'gm_organ_3_rock'],
            'guitar': ['gm_electric_guitar_clean', 'gm_electric_guitar_muted', 'gm_acoustic_guitar_nylon']
        }
        
        # Effect parameters
        self.effects = {
            'filter': ['lpf', 'hpf', 'bpf', 'bpq'],
            'reverb': ['room', 'size', 'dry', 'wet'],
            'delay': ['delay', 'delaytime', 'delayfeedback'],
            'distortion': ['distort', 'crush', 'clip'],
            'modulation': ['phaser', 'flanger', 'chorus'],
            'dynamics': ['gain', 'shape', 'compress']
        }
        
        # Pattern generators
        self.pattern_generators = {
            'rhythmic': self._generate_rhythmic_pattern,
            'melodic': self._generate_melodic_pattern,
            'harmonic': self._generate_harmonic_pattern,
            'textural': self._generate_textural_pattern
        }
    
    def _normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to a 0-1 range"""
        return max(0, min(1, (value - min_val) / (max_val - min_val)))
    
    def _map_to_range(self, value: float, target_min: float, target_max: float) -> float:
        """Map normalized value to target range"""
        return value * (target_max - target_min) + target_min
    
    def _generate_rhythmic_pattern(self, metric: AnalyzedMetric) -> Dict[str, Any]:
        """Generate dynamic rhythmic patterns based on blockchain data"""
        activity = self._normalize_value(metric.network_activity_score, 0, 100)
        volatility = self._normalize_value(metric.volatility_index, 0, 100)
        
        # Determine pattern complexity
        complexity = int(self._map_to_range(activity, 1, 4))
        
        # Generate kick pattern
        kick_patterns = [
            "bd",
            "bd*2",
            "bd ~ bd",
            "bd ~ bd ~",
            "bd*2 ~ bd",
            "bd ~ bd*2 ~",
            "bd*4",
            "bd ~ ~ bd"
        ]
        
        # Generate snare pattern
        snare_patterns = [
            "~ sd",
            "~ sd ~",
            "~ sd ~ sd",
            "~ sd*2 ~",
            "~ ~ sd ~",
            "~ sd ~ ~ sd",
            "~ sd*3 ~",
            "~ ~ ~ sd"
        ]
        
        # Generate hihat pattern
        hihat_patterns = [
            "hh*8",
            "hh*16",
            "hh*4",
            "hh*2",
            "hh ~ hh ~",
            "hh*8 ~ hh*8",
            "hh*12",
            "hh*6"
        ]
        
        # Select patterns based on complexity
        kick_idx = min(complexity - 1, len(kick_patterns) - 1)
        snare_idx = min(complexity - 1, len(snare_patterns) - 1)
        hihat_idx = min(complexity, len(hihat_patterns) - 1)
        
        return {
            'kick': kick_patterns[kick_idx],
            'snare': snare_patterns[snare_idx],
            'hihat': hihat_patterns[hihat_idx],
            'complexity': complexity,
            'activity': activity,
            'volatility': volatility
        }
    
    def _generate_melodic_pattern(self, metric: AnalyzedMetric) -> Dict[str, Any]:
        """Generate dynamic melodic patterns based on blockchain data"""
        price_change = self._normalize_value(abs(metric.price_change_percentage), 0, 50)
        gas_trend = self._normalize_value(metric.gas_fee_trend, -50, 50)
        
        # Select scale and root
        scale_names = list(self.scales.keys())
        scale_idx = int(self._map_to_range(price_change, 0, len(scale_names) - 1))
        scale_idx = max(0, min(scale_idx, len(scale_names) - 1))  # Ensure valid index
        scale_name = scale_names[scale_idx]
        
        root_idx = int(self._map_to_range(gas_trend + 0.5, 0, len(self.root_notes) - 1))
        root_idx = max(0, min(root_idx, len(self.root_notes) - 1))  # Ensure valid index
        root_note = self.root_notes[root_idx]
        
        # Generate note patterns
        scale_degrees = self.scales[scale_name]
        octave = int(self._map_to_range(gas_trend + 0.5, 2, 5))
        
        # Create note sequences
        note_sequences = []
        for i in range(4):
            degree = scale_degrees[i % len(scale_degrees)]
            note_num = degree + (octave * 12)
            note_sequences.append(str(note_num))
        
        # Generate pattern variations
        pattern_variations = [
            f"<{' '.join(note_sequences)}>",
            f"<{' '.join(note_sequences[:2])} {' '.join(note_sequences[2:])}>",
            f"<{' '.join(note_sequences)}*2>",
            f"<{' '.join(note_sequences[:3])} ~ {' '.join(note_sequences[3:])}>"
        ]
        
        pattern_idx = int(self._map_to_range(price_change, 0, len(pattern_variations) - 1))
        
        return {
            'scale': f"{root_note}:{scale_name}",
            'pattern': pattern_variations[pattern_idx],
            'octave': octave,
            'root_note': root_note,
            'scale_name': scale_name,
            'price_change': price_change,
            'gas_trend': gas_trend
        }
    
    def _generate_harmonic_pattern(self, metric: AnalyzedMetric) -> Dict[str, Any]:
        """Generate harmonic patterns based on blockchain data"""
        volume_change = self._normalize_value(metric.transaction_volume_change, -50, 50)
        block_rate = self._normalize_value(metric.block_production_rate, 0, 500)
        
        # Generate chord progressions
        chord_progressions = [
            "0 2 4",  # I-iii-V
            "0 3 5",  # I-iv-V
            "0 2 5",  # I-iii-VI
            "0 3 6",  # I-iv-VII
            "0 4 6",  # I-V-VII
            "0 2 4 6",  # I-iii-V-VII
            "0 3 5 6",  # I-iv-V-VII
            "0 2 3 5"   # I-iii-iv-V
        ]
        
        # Select chord progression
        chord_idx = int(self._map_to_range(volume_change + 0.5, 0, len(chord_progressions) - 1))
        chord_idx = max(0, min(chord_idx, len(chord_progressions) - 1))  # Ensure valid index
        chord_progression = chord_progressions[chord_idx]
        
        # Generate voicing patterns (Strudel format)
        voicing_patterns = [
            "root",
            "root:3",
            "root:5", 
            "root:7",
            "root:9",
            "root:11",
            "root:13"
        ]
        
        voicing_idx = int(self._map_to_range(block_rate, 0, len(voicing_patterns) - 1))
        voicing_idx = max(0, min(voicing_idx, len(voicing_patterns) - 1))  # Ensure valid index
        voicing = voicing_patterns[voicing_idx]
        
        return {
            'chord_progression': chord_progression,
            'voicing': voicing,
            'volume_change': volume_change,
            'block_rate': block_rate
        }
    
    def _generate_textural_pattern(self, metric: AnalyzedMetric) -> Dict[str, Any]:
        """Generate textural patterns based on blockchain data"""
        volatility = self._normalize_value(metric.volatility_index, 0, 100)
        liquidity = self._normalize_value(metric.liquidity_score, 0, 100)
        
        # Generate texture patterns
        texture_patterns = [
            "sine.range(0.1, 0.9).slow(8)",
            "saw.range(0.2, 0.8).slow(4)",
            "tri.range(0.3, 0.7).slow(6)",
            "perlin.range(0.1, 1.0).slow(2)",
            "rand.range(0.2, 0.8).slow(3)",
            "cosine.range(0.1, 0.9).slow(5)",
            "square.range(0.3, 0.7).slow(7)"
        ]
        
        # Generate modulation patterns
        modulation_patterns = [
            "sine.range(200, 20000).slow(4)",
            "saw.range(500, 15000).slow(3)",
            "tri.range(300, 12000).slow(5)",
            "perlin.range(100, 18000).slow(2)",
            "rand.range(400, 16000).slow(6)",
            "cosine.range(250, 14000).slow(4)",
            "square.range(600, 10000).slow(3)"
        ]
        
        texture_idx = int(self._map_to_range(volatility, 0, len(texture_patterns) - 1))
        texture_idx = max(0, min(texture_idx, len(texture_patterns) - 1))  # Ensure valid index
        mod_idx = int(self._map_to_range(liquidity, 0, len(modulation_patterns) - 1))
        mod_idx = max(0, min(mod_idx, len(modulation_patterns) - 1))  # Ensure valid index
        
        return {
            'texture': texture_patterns[texture_idx],
            'modulation': modulation_patterns[mod_idx],
            'volatility': volatility,
            'liquidity': liquidity
        }
    
    def _generate_effects_chain(self, metric: AnalyzedMetric) -> List[str]:
        """Generate dynamic effects chain based on blockchain data"""
        volatility = self._normalize_value(metric.volatility_index, 0, 100)
        gas_trend = self._normalize_value(metric.gas_fee_trend, -50, 50)
        activity = self._normalize_value(metric.network_activity_score, 0, 100)
        
        effects = []
        
        # Filter effects based on volatility
        if volatility > 0.7:
            effects.append(f".lpf({random.choice(['sine', 'saw', 'tri', 'perlin'])}.range(200, 20000).slow({random.randint(2, 8)}))")
        elif volatility > 0.4:
            effects.append(f".hpf({random.choice(['sine', 'saw', 'tri'])}.range(100, 5000).slow({random.randint(3, 6)}))")
        
        # Reverb based on gas trend
        if gas_trend > 0.3:
            effects.append(f".room({random.uniform(0.5, 2.0):.1f})")
            effects.append(f".size({random.uniform(0.3, 0.8):.1f})")
        
        # Modulation based on activity
        if activity > 0.6:
            effects.append(f".{random.choice(['phaser', 'flanger', 'chorus'])}({random.randint(2, 8)})")
        
        # Distortion based on volatility
        if volatility > 0.8:
            effects.append(f".{random.choice(['distort', 'crush', 'clip'])}()")
        
        # Delay based on gas trend (reduced for better vibe)
        if abs(gas_trend) > 0.7:  # Higher threshold
            effects.append(f".delay({random.uniform(0.05, 0.15):.2f})")  # Much less delay
        
        return effects
    
    def _generate_dynamic_track(self, metric: AnalyzedMetric, instrument: ChainInstrument) -> str:
        """Generate a complete dynamic strudel track"""
        
        # Generate all pattern types
        rhythmic = self._generate_rhythmic_pattern(metric)
        melodic = self._generate_melodic_pattern(metric)
        harmonic = self._generate_harmonic_pattern(metric)
        textural = self._generate_textural_pattern(metric)
        
        # Calculate tempo based on price change
        price_change = abs(metric.price_change_percentage)
        tempo = int(self._map_to_range(self._normalize_value(price_change, 0, 50), 60, 180))
        
        # Generate effects chain
        effects_chain = self._generate_effects_chain(metric)
        
        # Select samples based on instrument type
        lead_sample = random.choice(self.melodic_samples['lead'])
        bass_sample = random.choice(self.melodic_samples['bass'])
        pad_sample = random.choice(self.melodic_samples['pad'])
        
        # Generate the complete strudel code
        strudel_code = f"""// Dynamic Blockchain Audio Pattern
// Generated: {datetime.now().isoformat()}
// Chain: {metric.chain_name}
// Activity: {metric.network_activity_score:.1f}
// Volatility: {metric.volatility_index:.1f}

setcps({tempo/60:.2f})

stack(
  // RHYTHMIC LAYER
  stack(
    s("{rhythmic['kick']}").gain({random.uniform(0.6, 1.0):.2f}),
    s("{rhythmic['snare']}").gain({random.uniform(0.4, 0.8):.2f}),
    s("{rhythmic['hihat']}").gain({random.uniform(0.2, 0.6):.2f})
  ).bank('RolandTR909'),
  
  // LEAD MELODY
  n("{melodic['pattern']}")
  .scale("{melodic['scale']}")
  .s("{lead_sample}")
  .clip({textural['texture']})
  .jux(rev)
  .room({random.uniform(0.5, 2.0):.1f})
  .lpf({textural['modulation']})
  {''.join(effects_chain[:3])},
  
  // BASS LINE
  n("{harmonic['chord_progression']}")
  .scale("{melodic['scale']}")
  .s("{bass_sample}")
  .gain({random.uniform(0.3, 0.7):.2f})
  .lpf({random.randint(200, 800)})
  {''.join(effects_chain[1:2])},
  
  // HARMONIC PAD
  n("{harmonic['chord_progression']}")
  .scale("{melodic['scale']}")
  .s("{pad_sample}")
  .gain({random.uniform(0.2, 0.5):.2f})
  .room({random.uniform(0.5, 1.5):.1f})  // Reduced reverb
  .shape({random.uniform(0.2, 0.4):.1f})  // Less shape
  .delay({random.uniform(0.05, 0.15):.2f})  // Much less delay
  {''.join(effects_chain[2:])}
)
.late("[0 .01]*2")  // Reduced late effects
.size({random.uniform(1.5, 3.0):.1f})  // Smaller size for less reverb
"""
        
        return strudel_code.strip()
    
    def generate_strudel_code(self, musical_params: MusicalParameters, instrument: ChainInstrument) -> str:
        """Generate Strudel code from musical parameters - legacy method for compatibility"""
        # This method is kept for compatibility but now uses the new dynamic generation
        # Create a mock AnalyzedMetric from musical_params for the new generator
        mock_metric = AnalyzedMetric(
            chain_name=instrument.chain_name,
            timestamp=datetime.now(),
            price_change_percentage=musical_params.tempo - 120,  # Rough mapping
            gas_fee_trend=musical_params.gain * 100 - 50,  # Rough mapping
            transaction_volume_change=musical_params.complexity * 10,  # Rough mapping
            block_production_rate=musical_params.complexity * 50,  # Rough mapping
            network_activity_score=musical_params.complexity * 10,  # Rough mapping
            volatility_index=len(musical_params.effects) * 20,  # Rough mapping
            liquidity_score=50.0  # Default value
        )
        
        return self._generate_dynamic_track(mock_metric, instrument)
    
    def generate_track(self, analyzed_metric: AnalyzedMetric, instrument: ChainInstrument) -> StrudelTrack:
        """Generate a complete Strudel track from analyzed metrics using dynamic patterns"""
        
        # Generate dynamic strudel code
        strudel_code = self._generate_dynamic_track(analyzed_metric, instrument)
        
        # Create musical parameters for compatibility
        musical_params = MusicalParameters(
            tempo=int(self._map_to_range(self._normalize_value(abs(analyzed_metric.price_change_percentage), 0, 50), 60, 180)),
            base_note=f"{self.root_notes[max(0, min(int(self._map_to_range(self._normalize_value(analyzed_metric.gas_fee_trend, -50, 50) + 0.5, 0, len(self.root_notes) - 1)), len(self.root_notes) - 1))]}4",
            rhythm_pattern="dynamic",
            gain=self._map_to_range(self._normalize_value(analyzed_metric.gas_fee_trend, -50, 50) + 0.5, 0.3, 0.9),
            sound_profile=instrument.sound_profile,
            scale=f"{self.root_notes[max(0, min(int(self._map_to_range(self._normalize_value(abs(analyzed_metric.price_change_percentage), 0, 50), 0, len(self.root_notes) - 1)), len(self.root_notes) - 1))]}:{list(self.scales.keys())[max(0, min(int(self._map_to_range(self._normalize_value(abs(analyzed_metric.price_change_percentage), 0, 50), 0, len(self.scales) - 1)), len(self.scales) - 1))]}",
            complexity=int(self._map_to_range(self._normalize_value(analyzed_metric.network_activity_score, 0, 100), 1, 10)),
            effects=self._generate_effects_chain(analyzed_metric),
            instrument_type=instrument.instrument_type
        )
        
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
    
    def generate_multi_chain_track(self, analyzed_metrics: List[AnalyzedMetric], instruments: List[ChainInstrument], experimental_chain: str = None) -> StrudelTrack:
        """Generate an experimental multi-chain track with optional chain selection"""
        
        if not analyzed_metrics or not instruments:
            raise ValueError("Need at least one analyzed metric and instrument")
        
        # If experimental_chain is specified, use that chain's pattern as the base
        if experimental_chain:
            # Find the specified chain
            experimental_metric = next((m for m in analyzed_metrics if m.chain_name == experimental_chain), None)
            experimental_instrument = next((i for i in instruments if i.chain_name == experimental_chain), None)
            
            if experimental_metric and experimental_instrument:
                # Generate the experimental pattern for the selected chain
                experimental_track = self.generate_advanced_pattern(experimental_metric, experimental_instrument, "experimental")
                
                # Use this as the base and add other chains as supporting elements
                base_code = experimental_track
                
                # Add supporting elements from other chains
                supporting_elements = []
                for metric, instrument in zip(analyzed_metrics, instruments):
                    if metric.chain_name != experimental_chain:
                        # Generate simple supporting pattern
                        rhythmic = self._generate_rhythmic_pattern(metric)
                        melodic = self._generate_melodic_pattern(metric)
                        
                        supporting_element = f"""  // {metric.chain_name.upper()} - Supporting
  n("{melodic['pattern']}")
  .scale("{melodic['scale']}")
  .s("{random.choice(self.melodic_samples['lead'])}")
  .gain({random.uniform(0.2, 0.5):.2f})
  .room({random.uniform(0.3, 0.8):.1f})
  .lpf({random.randint(200, 1000)}),"""
                        
                        supporting_elements.append(supporting_element)
                
                # Combine the experimental base with supporting elements
                # Remove comma from last element
                if supporting_elements:
                    supporting_elements[-1] = supporting_elements[-1].rstrip(',')
                
                combined_code = f"""// Experimental Multi-Chain - {experimental_chain.upper()} Lead
// Generated: {datetime.now().isoformat()}
// Lead Chain: {experimental_chain}
// Supporting: {', '.join([m.chain_name for m in analyzed_metrics if m.chain_name != experimental_chain])}

{base_code}

// Supporting chains
stack(
{chr(10).join(supporting_elements)}
)"""
                
                # Calculate tempo from the experimental chain
                experimental_tempo = int(self._map_to_range(
                    self._normalize_value(abs(experimental_metric.price_change_percentage), 0, 50), 60, 180
                ))
                
                # Create musical parameters
                musical_params = MusicalParameters(
                    tempo=experimental_tempo,
                    base_note=f"{self.root_notes[random.randint(0, len(self.root_notes)-1)]}4",
                    rhythm_pattern="experimental_multi_chain",
                    gain=random.uniform(0.6, 0.9),
                    sound_profile="experimental",
                    scale=f"{self.root_notes[random.randint(0, len(self.root_notes)-1)]}:major",
                    complexity=random.randint(7, 10),
                    effects=self._generate_effects_chain(experimental_metric),
                    instrument_type="experimental"
                )
                
                track_id = f"multi_chain_experimental_{experimental_chain}_{int(datetime.now().timestamp())}"
                
                return StrudelTrack(
                    id=track_id,
                    timestamp=datetime.now(),
                    chain_name="multi_chain_experimental",
                    strudel_code_string=combined_code.strip(),
                    source_kpis=experimental_metric,
                    musical_parameters=musical_params,
                    created_at=datetime.now()
                )
        
        # Default: Generate individual tracks and combine them cleanly
        individual_tracks = []
        for metric, instrument in zip(analyzed_metrics, instruments):
            track = self.generate_track(metric, instrument)
            individual_tracks.append(track)
        
        # Calculate collaborative tempo
        avg_tempo = sum(track.musical_parameters.tempo for track in individual_tracks) / len(individual_tracks)
        
        # Use the most active chain's scale
        primary_track = max(individual_tracks, key=lambda x: x.source_kpis.network_activity_score)
        primary_scale = primary_track.musical_parameters.scale
        
        # Extract individual chain patterns
        chain_patterns = []
        for track in individual_tracks:
            # Parse the individual track code to extract the main pattern
            code_lines = track.strudel_code_string.split('\n')
            
            # Find the stack section and extract the main melody
            melody_start = None
            melody_end = None
            for j, line in enumerate(code_lines):
                if '// LEAD MELODY' in line:
                    melody_start = j
                elif melody_start and line.strip().startswith('//'):
                    melody_end = j
                    break
            
            if melody_start and melody_end:
                melody_lines = code_lines[melody_start:melody_end]
                melody_code = '\n'.join(melody_lines).strip()
                
                # Create a clean chain section
                chain_pattern = f"""  // {track.source_kpis.chain_name.upper()} - {track.musical_parameters.instrument_type.title()}
  {melody_code}
  .gain({random.uniform(0.4, 0.8):.2f})
  .room({random.uniform(0.3, 0.7):.1f}),"""
                
                chain_patterns.append(chain_pattern)
        
        # Create collaborative harmonic layer
        harmonic_pattern = self._generate_harmonic_pattern(primary_track.source_kpis)
        harmonic_code = f"""  // COLLABORATIVE HARMONIC LAYER
  n("{harmonic_pattern['chord_progression']}")
  .scale("{primary_scale}")
  .s("{random.choice(self.melodic_samples['pad'])}")
  .gain({random.uniform(0.2, 0.4):.2f})
  .room({random.uniform(0.8, 1.5):.1f})
  .shape({random.uniform(0.2, 0.4):.1f})
  .delay({random.uniform(0.05, 0.15):.2f})"""
        
        # Generate clean multi-chain code
        chain_names = [m.chain_name for m in analyzed_metrics]
        
        # Remove comma from last chain pattern
        if chain_patterns:
            chain_patterns[-1] = chain_patterns[-1].rstrip(',')
        
        combined_code = f"""// Multi-Chain Collaborative Jam
// Generated: {datetime.now().isoformat()}
// Chains: {', '.join(chain_names)}
// Each chain contributes its unique voice to the symphony

setcps({avg_tempo/60:.2f})

stack(
{chr(10).join(chain_patterns)},
  
{harmonic_code}
)
.late("[0 .01]*2")
.size({random.uniform(2.0, 4.0):.1f})"""
        
        # Create musical parameters
        musical_params = MusicalParameters(
            tempo=int(avg_tempo),
            base_note=primary_track.musical_parameters.base_note,
            rhythm_pattern="multi_chain_collaborative",
            gain=sum(track.musical_parameters.gain for track in individual_tracks) / len(individual_tracks),
            sound_profile="orchestra",
            scale=primary_scale,
            complexity=int(sum(track.musical_parameters.complexity for track in individual_tracks) / len(individual_tracks)),
            effects=primary_track.musical_parameters.effects,
            instrument_type="orchestra"
        )
        
        track_id = f"multi_chain_collaborative_{int(datetime.now().timestamp())}"
        
        return StrudelTrack(
            id=track_id,
            timestamp=datetime.now(),
            chain_name="multi_chain",
            strudel_code_string=combined_code.strip(),
            source_kpis=primary_track.source_kpis,
            musical_parameters=musical_params,
            created_at=datetime.now()
        )
    
    def generate_advanced_pattern(self, analyzed_metric: AnalyzedMetric, instrument: ChainInstrument, pattern_type: str = "experimental") -> str:
        """Generate advanced experimental patterns similar to the provided examples"""
        
        # Generate all pattern components
        rhythmic = self._generate_rhythmic_pattern(analyzed_metric)
        melodic = self._generate_melodic_pattern(analyzed_metric)
        harmonic = self._generate_harmonic_pattern(analyzed_metric)
        textural = self._generate_textural_pattern(analyzed_metric)
        
        # Calculate tempo
        price_change = abs(analyzed_metric.price_change_percentage)
        tempo = int(self._map_to_range(self._normalize_value(price_change, 0, 50), 60, 180))
        
        if pattern_type == "experimental":
            # Generate experimental pattern similar to the examples
            strudel_code = f"""// Experimental Blockchain Audio Pattern
// Generated: {datetime.now().isoformat()}
// Chain: {analyzed_metric.chain_name}
// Pattern Type: {pattern_type}

setcps({tempo/60:.2f})

stack(
  // Complex rhythmic foundation
  stack(
    s("{rhythmic['kick']}").struct("<[x*<1 2> [~@3 x]] x>"),
    s("~ [rim, sd:<2 3>]").room("<0 .2>"),
    n("[0 <1 3>]*<2!3 4>").s("hh"),
    s("rd:<1!3 2>*2").mask("<0 0 1 1>/16").gain(.5)
  ).bank('RolandTR909')
  .mask("<[0 1] 1 1 1>/16".early(.5)),
  
  // Lead melody with complex modulation
  n("{melodic['pattern']}")
  .scale("{melodic['scale']}")
  .s("{random.choice(self.melodic_samples['lead'])}")
  .clip({textural['texture']})
  .jux(rev)
  .room({random.uniform(0.5, 2.0):.1f})
  .lpf({textural['modulation']})
  .phaser({random.randint(2, 8)})
  .shape({random.uniform(0.2, 0.6):.1f}),
  
  // Bass line with rhythmic variation
  n("{harmonic['chord_progression']}")
  .scale("{melodic['scale']}")
  .s("{random.choice(self.melodic_samples['bass'])}")
  .gain({random.uniform(0.4, 0.8):.2f})
  .lpf({random.randint(200, 800)}),
  
  // Harmonic pad with texture
  n("{harmonic['chord_progression']}")
  .scale("{melodic['scale']}")
  .s("{random.choice(self.melodic_samples['pad'])}")
  .gain({random.uniform(0.2, 0.5):.2f})
  .room({random.uniform(0.5, 1.5):.1f})  // Reduced reverb
  .shape({random.uniform(0.2, 0.5):.1f})  // Less shape
  .delay({random.uniform(0.05, 0.15):.2f})  // Much less delay
  .fm(sine.range(3, 8).slow(8))
  .lpf(sine.range(500, 1000).slow(8)).lpq(5)
  .rarely(ply("2")).chunk(4, fast(2))
  .gain(perlin.range(.6, .9))
  .mask("<0 1 1 0>/16")
)
.late("[0 .01]*2")  // Reduced late effects
.size({random.uniform(2, 4):.1f})  // Smaller size for less reverb
"""
        
        elif pattern_type == "minimal":
            # Generate minimal pattern
            strudel_code = f"""// Minimal Blockchain Audio Pattern
// Generated: {datetime.now().isoformat()}

setcps({tempo/60:.2f})

stack(
  s("{rhythmic['kick']}").gain({random.uniform(0.7, 1.0):.2f}),
  n("{melodic['pattern']}")
  .scale("{melodic['scale']}")
  .s("{random.choice(self.melodic_samples['lead'])}")
  .gain({random.uniform(0.4, 0.7):.2f})
  .room({random.uniform(0.5, 1.5):.1f})
)
"""
        
        else:  # Default complex pattern
            strudel_code = self._generate_dynamic_track(analyzed_metric, instrument)
        
        return strudel_code.strip()
