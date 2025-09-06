# 🎵 Golem-Powered Blockchain Audio Aggregator

A revolutionary project that transforms blockchain data into live musical symphonies using Golem DB and Strudel. This project was created for **ETHWarsaw2025** and showcases the intersection of decentralized technology, data visualization, and musical composition.

## 🎼 What is the Blockchain Symphony?

The Blockchain Symphony is a real-time musical composition where:
- **Ethereum, Bitcoin, and Polygon** data creates musical layers
- **Price movements** become musical notes and melodies
- **Trading volume** drives rhythm patterns
- **Gas fees** add audio effects (reverb, delay, room)
- **Network volatility** influences musical tempo
- **All chains play together** in perfect harmony

## ✨ Features

### 🎵 **Musical Layers**
- **🟦 Ethereum Layer** - Lead piano (high frequency, complex patterns)
- **🟨 Bitcoin Layer** - Bass foundation (low frequency, steady rhythm)
- **🟣 Polygon Layer** - Percussion texture (mid frequency, fast patterns)
- **🥁 Rhythm Section** - Volume-based drum patterns
- **🎼 Harmonic Layer** - Price correlation chords
- **🌊 Ambient Layer** - Network activity atmosphere

### 📊 **Real-time Data Visualization**
- Interactive blockchain metrics dashboard
- Live price charts and network activity graphs
- Multi-chain data comparison (Ethereum, Bitcoin, Polygon)
- Volatility analysis and trend visualization

### 🎮 **Integrated Strudel Player**
- Embedded web browser for live music playback
- Real-time symphony generation from blockchain data
- Export functionality for saving musical compositions
- Copy-to-clipboard for external Strudel usage

### 🗄️ **Golem DB Integration**
- Decentralized storage of blockchain data
- Persistent musical compositions on the Golem network
- Distributed computing for data analysis
- Blockchain-instrument mapping storage

## 🚀 Quick Start

### 1. **Clone the Repository**
```bash
git clone https://github.com/ETHWarsaw2025/Orchestra.git
cd Orchestra
```

### 2. **Set up Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. **Install Dependencies**
```bash
pip install -r Hermes/requirements.txt
```

### 4. **Run the Blockchain Symphony**
```bash
cd Hermes
python gui.py
```

## 🎵 How It Works

### **Data-to-Music Mapping**
- **Price → Notes**: Each blockchain's price determines musical notes and octaves
- **Volume → Rhythm**: Trading volume creates rhythm patterns
- **Gas Fees → Effects**: Network congestion adds reverb, delay, and room effects
- **Volatility → Tempo**: Price volatility influences musical tempo

### **Musical Generation Process**
1. **Fetch Real-time Data** - Collect blockchain metrics from RPC nodes
2. **Analyze Patterns** - Calculate volatility, trends, and correlations
3. **Generate Symphony** - Convert data into Strudel musical code
4. **Play Together** - All chains contribute to one unified composition
5. **Store on Golem** - Save compositions to decentralized storage

## 📁 Project Structure

```
Orchestra/
├── Hermes/
│   ├── gui.py                    # 🎵 Main symphony GUI
│   ├── main.py                   # System orchestrator
│   ├── models.py                 # Data models
│   ├── blockchain_client.py      # Blockchain data fetching
│   ├── data_analyzer.py          # Data analysis
│   ├── golem_storage.py          # Golem DB integration
│   ├── orchestrator.py           # System orchestration
│   ├── strudel_generator.py      # Audio track generation
│   └── requirements.txt          # Dependencies
└── README.md                     # This file
```

## 🛠️ Dependencies

### **Core Requirements**
- `golem-base-sdk` - Golem DB integration
- `web3` - Ethereum blockchain interaction
- `PyQt6` + `PyQt6-WebEngine` - GUI and embedded browser
- `matplotlib` - Data visualization
- `pandas` + `numpy` - Data analysis
- `aiohttp` - Async HTTP requests

### **Installation**
```bash
pip install -r Hermes/requirements.txt
```

## 🎼 Usage

### **Launch the Symphony**
```bash
cd Hermes
python gui.py
```

### **Interact with the GUI**
1. **📊 Blockchain Data Tab** - View real-time metrics and charts
2. **🎵 Blockchain Symphony Tab** - Play the generated symphony
3. **🎼 Orchestra Config Tab** - Configure chain-instrument mappings

### **Generate New Symphony**
- Click "🔄 Regenerate Symphony" to create new composition from current data
- Click "🎵 Play Symphony" to load in Strudel player
- Click "📋 Copy Code" to copy musical code to clipboard

## 🌐 External Integration

### **Strudel Integration**
- **Website**: https://strudel.tidalcycles.org/
- **Samples**: https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json
- **Documentation**: https://strudel.tidalcycles.org/learn/

### **Golem Network**
- **Website**: https://golem.network/
- **Documentation**: https://docs.golem.network/
- **RPC Endpoint**: https://ethwarsaw.holesky.golemdb.io/rpc

## 🎵 Sample Symphony Code

```javascript
// Generated Strudel track for blockchain symphony
samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
  // 🟦 ETHEREUM LAYER - Lead piano
  n("c4 e4 g4")
    .sound("piano")
    .gain(0.4)
    .room(0.8)
    .size(0.9)
    .delay(0.2),
    
  // 🟨 BITCOIN LAYER - Bass foundation
  n("c2 e2 g2")
    .sound("bd")
    .gain(0.6)
    .lpf(800),
    
  // 🟣 POLYGON LAYER - Percussion
  n("c5 e5 g5")
    .sound("hh")
    .gain(0.5)
    .hpf(400),
    
  // Rhythm patterns based on volume
  s("bd sd bd sd, hh*8").gain(0.3)
)
```

## 🤝 Contributing

This project was created for **ETHWarsaw2025**. Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🎵 Acknowledgments

- **Golem Network** - Decentralized computing platform
- **Strudel** - Live coding environment for musical patterns
- **TidalCycles** - Algorithmic pattern library
- **ETHWarsaw2025** - Ethereum community event

---

**🎵 The blockchain symphony plays on... Each chain contributes its unique voice to the digital orchestra! 🎵⛓️🎼**