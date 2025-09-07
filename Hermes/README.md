# 🎵 Golem-Powered Blockchain Audio Aggregator

A system that aggregates blockchain data using Golem, analyzes it, and generates musical patterns in the Strudel language based on the analyzed data.

## 🎯 Overview

This project creates a complete pipeline that:
1. **Stores Orchestra Table** on Golem (blockchain → instrument mappings)
2. **Retrieves Blockchain Data** from various networks
3. **Stores Blockchain Data** on Golem for historical analysis
4. **Analyzes Data** to calculate KPIs (price changes, gas trends, etc.)
5. **Generates Strudel Audio Tracks** based on blockchain activity
6. **Stores Strudel Tracks** on Golem for sharing and playback

## 🏗️ Architecture

```
Orchestra Table (Golem) → Blockchain Data Retrieval → Blockchain Data Storage (Golem) 
→ Data Analysis → Strudel Audio Track Generation → Strudel Audio Table (Golem)
```

## 📁 Project Structure

```
Hermes/
├── main.py                 # Main entry point
├── orchestrator.py         # Main pipeline orchestrator
├── models.py               # Data models and types
├── golem_storage.py        # Golem DB storage operations
├── blockchain_client.py    # Blockchain data retrieval
├── data_analyzer.py        # KPI calculation and analysis
├── strudel_generator.py    # Strudel audio pattern generation
├── gui.py                  # PyQt6 GUI interface (user-friendly frontend)
├── requirements.txt        # Python dependencies
├── env_example.txt         # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Environment

Copy the environment template and configure:

```bash
cp env_example.txt .env
```

Edit `.env` with your Golem DB credentials and API keys.

### 3. Run the Pipeline

**Command Line Interface:**
```bash
python main.py
```

**GUI Interface (User-Friendly):**
```bash
python gui.py
```

## 🎮 GUI Interface (Optional)

The GUI provides a user-friendly interface to the core pipeline:

### **Blockchain Data Tab**
- View real-time blockchain metrics and KPIs
- Visualize data analysis results
- Monitor network activity across chains

### **Blockchain Symphony Tab**
- Generate individual chain patterns (Ethereum, Optimism, Polygon, Base)
- Create multi-chain symphonies
- Play patterns in embedded Strudel player
- Manage and organize generated tracks

### **Push to Golem**
- Store generated patterns on Golem network
- Share compositions globally
- Access decentralized storage

*Note: The GUI is a frontend interface. All core functionality is available via command line.*

## 🔧 Configuration

### Environment Variables

- `PRIVATE_KEY`: Your Golem DB private key
- `RPC_URL`: Golem DB RPC endpoint
- `WS_URL`: Golem DB WebSocket endpoint
- `INFURA_PROJECT_ID`: Infura API key (optional)
- `ALCHEMY_API_KEY`: Alchemy API key (optional)
- `COINGECKO_API_KEY`: CoinGecko API key (optional)

### Orchestra Table

The system comes pre-configured with these blockchain-instrument mappings:

- **Ethereum** → Guitar (Moog sound profile)
- **Bitcoin** → Drum (BD sound profile)  
- **Polygon** → Bass (GM Synth Bass sound profile)
- **Optimism** → Lead (Sawtooth sound profile)
- **Base** → Lead (Calliope sound profile)

## 🎵 Generated Strudel Code

The system generates dynamic Strudel patterns based on blockchain KPIs:

### Price Changes → Tempo
- Positive price change = faster tempo
- Negative price change = slower tempo

### Gas Fee Trends → Gain & Effects
- Rising gas fees = higher gain, distortion effects
- Falling gas fees = lower gain, reverb effects

### Transaction Volume → Rhythm Complexity
- High volume = complex rhythmic patterns
- Low volume = simple, sparse patterns

### Block Production Rate → Scale
- High block rate = major scales
- Low block rate = minor scales

## 📊 Data Flow

### 1. Orchestra Table Storage
- **Step 1**: Store blockchain-instrument mappings on Golem DB
- **Purpose**: Defines sound profiles, RPC endpoints, and chain configurations
- **Implementation**: `_step_1_store_orchestra_table()` in orchestrator.py

### 2. Blockchain Data Retrieval  
- **Step 2**: Fetch real-time data from multiple blockchains
- **Data Collected**: Price, volume, gas fees, transaction counts, block production rates
- **Implementation**: `_step_2_retrieve_blockchain_data()` using blockchain_client.py

### 3. Blockchain Data Storage
- **Step 3**: Store historical blockchain metrics on Golem
- **Purpose**: Enable trend analysis and KPI calculation
- **Implementation**: `_step_3_store_blockchain_data()` in orchestrator.py

### 4. Data Analysis
- **Step 4**: Calculate KPIs from blockchain metrics
- **KPIs**: Price change %, gas fee trends, network activity scores, volatility indices
- **Implementation**: `_step_4_analyze_data()` using data_analyzer.py

### 5. Strudel Track Generation
- **Step 5**: Generate musical patterns from analyzed KPIs
- **Output**: Dynamic Strudel code with rhythmic, melodic, and harmonic layers
- **Implementation**: `_step_5_generate_strudel_tracks()` using strudel_generator.py

### 6. Strudel Track Storage
- **Step 6**: Store generated tracks on Golem for sharing
- **Purpose**: Enable global access and historical playback
- **Implementation**: `_step_6_store_strudel_tracks()` in orchestrator.py

## 🎼 Example Generated Strudel Code

```javascript
// Dynamic Blockchain Audio Pattern
// Generated: 2025-09-07T10:40:16.141959
// Chain: ethereum
// Activity: 75.5
// Volatility: 3.2

setcps(1.20)

stack(
  // RHYTHMIC LAYER
  s("bd ~ bd").gain(0.77),
  s("~ sd ~ sd").gain(0.74),
  s("hh*2").gain(0.43),
  
  // LEAD MELODY
  n("<60 62 64 65>")
  .scale("B:major")
  .s("piano")
  .clip(sine.range(0.1, 0.9).slow(8))
  .jux(rev)
  .room(0.7)
  .lpf(sine.range(200, 20000).slow(4))
  .room(0.5).size(0.3).flanger(7),
  
  // BASS LINE
  n("0 2 3 5")
  .scale("B:major")
  .s("bass")
  .gain(0.44)
  .lpf(304)
  .size(0.3),
  
  // HARMONIC PAD
  n("0 2 3 5")
  .scale("B:major")
  .s("piano")
  .gain(0.29)
  .room(0.5)  // Reduced reverb
  .shape(0.3)  // Less shape
  .delay(0.14)  // Much less delay
  .flanger(7)
)
.late("[0 .01]*2")  // Reduced late effects
.size(2.9)  // Smaller size for less reverb
```

## 🔍 Monitoring and Analysis

The system provides detailed analysis of:

- **Price Changes**: 24-hour price change percentages (`calculate_price_change_percentage`)
- **Gas Fee Trends**: Gas fee movement patterns (`calculate_gas_fee_trend`)
- **Transaction Volume**: Volume change analysis (`calculate_transaction_volume_change`)
- **Block Production Rate**: Block generation speed (`calculate_block_production_rate`)
- **Network Activity**: Composite activity scores (`calculate_network_activity_score`)
- **Volatility**: Price volatility indices (`calculate_volatility_index`)
- **Liquidity**: Volume per transaction ratios (`calculate_liquidity_score`)

## 🎯 Key Features

- **Decentralized Storage**: All data stored on Golem network
- **Real-time Analysis**: Live blockchain data processing
- **Dynamic Music Generation**: KPIs directly influence musical output
- **Multi-chain Support**: Analyze multiple blockchains simultaneously
- **Historical Tracking**: Store and analyze historical patterns
- **Extensible Architecture**: Easy to add new blockchains and instruments
- **GUI Interface**: User-friendly PyQt6 frontend for easy interaction

## 🛠️ Development

### Adding New Blockchains

1. Add entry to `orchestra_table` in `orchestrator.py`
2. Implement blockchain client methods in `blockchain_client.py`
3. Update price APIs in `blockchain_client.py`

### Adding New Instruments

1. Update `sound_profile` in orchestra table
2. Add sound samples to Strudel generator
3. Modify musical parameter calculations

### Customizing KPI Calculations

1. Modify methods in `data_analyzer.py`
2. Update musical parameter mappings in `strudel_generator.py`
3. Adjust Strudel code templates

## 📈 Output

The system generates:
- **Individual tracks** for each blockchain (via `generate_track()`)
- **Multi-chain tracks** combining all blockchains (via `generate_multi_chain_track()`)
- **Advanced patterns** with experimental structures (via `generate_advanced_pattern()`)
- **Historical analysis** of blockchain trends (via `DataAnalyzer`)
- **Musical patterns** that reflect network activity (via `StrudelGenerator`)
- **Stored data** on Golem for future analysis (via `GolemStorage`)

## 🎉 Getting Started

1. **Clone and setup** the project
2. **Configure** your Golem DB credentials
3. **Run** the pipeline: `python main.py` (or `python gui.py` for GUI)
4. **Listen** to the generated Strudel tracks
5. **Analyze** the blockchain data insights

The system will automatically:
- Connect to Golem DB
- Fetch blockchain data
- Analyze trends and patterns
- Generate musical tracks
- Store everything for future use

**Ready to turn blockchain data into music!** 🎵⛓️