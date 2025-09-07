#!/usr/bin/env python3
"""
Golem Blockchain Audio Aggregator - Single GUI with Integrated Web Browser
Everything in one file with Strudel player embedded
"""

import sys
import json
import random
import webbrowser
from datetime import datetime
from typing import List, Optional

# Import our custom modules
from strudel_generator import StrudelGenerator
from models import AnalyzedMetric, ChainInstrument

# Try to import PyQt6 with WebEngine
try:
    from PyQt6.QtWidgets import (
        QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
        QGridLayout, QTabWidget, QLabel, QPushButton, QTextEdit, 
        QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
        QMessageBox, QStatusBar, QMenuBar, QMenu, QFileDialog,
        QSplitter, QFrame, QScrollArea
    )
    from PyQt6.QtCore import Qt, QTimer, QUrl
    from PyQt6.QtGui import QFont, QPalette, QColor
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    PYQT6_AVAILABLE = True
    WEBENGINE_AVAILABLE = True
except ImportError:
    try:
        from PyQt6.QtWidgets import (
            QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
            QGridLayout, QTabWidget, QLabel, QPushButton, QTextEdit, 
            QTableWidget, QTableWidgetItem, QComboBox, QGroupBox,
            QMessageBox, QStatusBar, QMenuBar, QMenu, QFileDialog,
            QSplitter, QFrame, QScrollArea
        )
        from PyQt6.QtCore import Qt, QTimer, QUrl
        from PyQt6.QtGui import QFont, QPalette, QColor
        PYQT6_AVAILABLE = True
        WEBENGINE_AVAILABLE = False
    except ImportError:
        print("❌ PyQt6 not available. Please install with: pip install PyQt6 PyQt6-WebEngine")
        sys.exit(1)

# Try to import matplotlib
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

class GolemBlockchainGUI(QMainWindow):
    """Single GUI with integrated web browser for Strudel"""
    
    def __init__(self):
        super().__init__()
        self.strudel_generator = StrudelGenerator()
        self.setup_status_bar()
        self.setup_menu()
        self.init_ui()
        self.load_sample_data()
    
    def init_ui(self):
        """Initialize the main UI"""
        self.setWindowTitle("🎵 Golem Blockchain Audio Aggregator")
        self.setGeometry(100, 100, 1600, 1000)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🎵 Golem-Powered Blockchain Audio Aggregator")
        header.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2E86AB; margin: 10px;")
        layout.addWidget(header)
        
        # Tab widget
        self.tab_widget = QTabWidget()
        
        # Add tabs
        self.blockchain_tab = self.create_blockchain_tab()
        self.strudel_tab = self.create_strudel_tab()
        self.orchestra_tab = self.create_orchestra_tab()
        
        self.tab_widget.addTab(self.blockchain_tab, "📊 Blockchain Data")
        self.tab_widget.addTab(self.strudel_tab, "🎵 Blockchain Symphony")
        self.tab_widget.addTab(self.orchestra_tab, "🎼 Orchestra Config")
        
        layout.addWidget(self.tab_widget)
        central_widget.setLayout(layout)
        
        # Apply dark theme
        self.apply_dark_theme()
    
    def create_blockchain_tab(self):
        """Create the blockchain data tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("📊 Blockchain Data Analytics")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Control panel
        control_panel = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_blockchain_data)
        control_panel.addWidget(self.refresh_btn)
        
        self.chain_combo = QComboBox()
        self.chain_combo.addItems(["ethereum", "optimism", "polygon", "base"])
        self.chain_combo.currentTextChanged.connect(self.update_blockchain_display)
        control_panel.addWidget(QLabel("Chain:"))
        control_panel.addWidget(self.chain_combo)
        
        control_panel.addStretch()
        layout.addLayout(control_panel)
        
        # Data display
        self.data_table = QTableWidget()
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(["Metric", "Value"])
        layout.addWidget(self.data_table)
        
        # Charts (if matplotlib is available)
        if MATPLOTLIB_AVAILABLE:
            chart_layout = QHBoxLayout()
            
            # Price chart
            self.price_fig = Figure(figsize=(6, 4))
            self.price_canvas = FigureCanvas(self.price_fig)
            chart_layout.addWidget(self.price_canvas)
            
            # Activity chart
            self.activity_fig = Figure(figsize=(6, 4))
            self.activity_canvas = FigureCanvas(self.activity_fig)
            chart_layout.addWidget(self.activity_canvas)
            
            layout.addLayout(chart_layout)
        else:
            # Fallback message
            no_charts_label = QLabel("📊 Charts disabled - matplotlib not available")
            no_charts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_charts_label.setStyleSheet("color: #888; font-style: italic; padding: 20px;")
            layout.addWidget(no_charts_label)
        
        widget.setLayout(layout)
        return widget
    
    def create_strudel_tab(self):
        """Create the Strudel player tab with integrated web browser"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🎵 Blockchain Symphony - All Chains Playing Together")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Control panel
        control_panel = QHBoxLayout()
        
        self.refresh_tracks_btn = QPushButton("🔄 Regenerate Symphony")
        self.refresh_tracks_btn.clicked.connect(self.refresh_strudel_tracks)
        control_panel.addWidget(self.refresh_tracks_btn)
        
        self.load_strudel_btn = QPushButton("🌐 Load Strudel")
        self.load_strudel_btn.clicked.connect(self.load_strudel_website)
        control_panel.addWidget(self.load_strudel_btn)
        
        self.export_btn = QPushButton("💾 Export Track")
        self.export_btn.clicked.connect(self.export_track)
        control_panel.addWidget(self.export_btn)
        
        control_panel.addStretch()
        layout.addLayout(control_panel)
        
        # Create splitter for tracks table and Strudel player
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side - Tracks table and details
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # Tracks table
        self.tracks_table = QTableWidget()
        self.tracks_table.setColumnCount(6)
        self.tracks_table.setHorizontalHeaderLabels([
            "Track ID", "Chain", "Timestamp", "Tempo", "Instrument", "Effects"
        ])
        self.tracks_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tracks_table.selectionModel().selectionChanged.connect(self.on_track_selected)
        left_layout.addWidget(self.tracks_table)
        
        # Track details
        details_group = QGroupBox("Track Details")
        details_layout = QVBoxLayout()
        
        self.track_details = QTextEdit()
        self.track_details.setMaximumHeight(150)
        self.track_details.setReadOnly(True)
        details_layout.addWidget(self.track_details)
        
        details_group.setLayout(details_layout)
        left_layout.addWidget(details_group)
        
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        
        # Right side - Integrated Strudel player
        strudel_group = QGroupBox("🎵 Integrated Strudel Player")
        strudel_layout = QVBoxLayout()
        
        # Strudel player controls
        player_controls = QHBoxLayout()
        
        self.copy_code_btn = QPushButton("📋 Copy Code")
        self.copy_code_btn.clicked.connect(self.copy_track_code)
        player_controls.addWidget(self.copy_code_btn)
        
        self.load_track_btn = QPushButton("🎵 Play Symphony")
        self.load_track_btn.clicked.connect(self.load_selected_track)
        player_controls.addWidget(self.load_track_btn)
        
        player_controls.addStretch()
        strudel_layout.addLayout(player_controls)
        
        # Pattern generation controls
        generation_controls = QHBoxLayout()
        
        # Pattern type selection
        generation_controls.addWidget(QLabel("Pattern Type:"))
        self.pattern_type_combo = QComboBox()
        self.pattern_type_combo.addItems(["basic", "experimental", "minimal"])
        self.pattern_type_combo.setCurrentText("experimental")
        generation_controls.addWidget(self.pattern_type_combo)
        
        # Generate new pattern button
        self.generate_pattern_btn = QPushButton("🎼 Generate New Pattern")
        self.generate_pattern_btn.clicked.connect(self.generate_new_pattern)
        generation_controls.addWidget(self.generate_pattern_btn)
        
        # Multi-chain pattern button
        self.multi_chain_btn = QPushButton("🔗 Multi-Chain Pattern")
        self.multi_chain_btn.clicked.connect(self.generate_multi_chain_pattern)
        generation_controls.addWidget(self.multi_chain_btn)
        
        generation_controls.addStretch()
        strudel_layout.addLayout(generation_controls)
        
        # Integrated web browser for Strudel
        if WEBENGINE_AVAILABLE:
            self.strudel_webview = QWebEngineView()
            self.strudel_webview.setMinimumHeight(400)
            strudel_layout.addWidget(self.strudel_webview)
            
            # Load Strudel website
            self.load_strudel_website()
        else:
            # Fallback - external browser message
            fallback_label = QLabel("""
            <b>⚠️ WebEngine not available</b><br><br>
            PyQt6-WebEngine is required for integrated Strudel player.<br>
            Install with: <code>pip install PyQt6-WebEngine</code><br><br>
            <b>Alternative:</b> Use external browser for Strudel
            """)
            fallback_label.setStyleSheet("""
                QLabel {
                    background-color: #333;
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 4px;
                    margin: 10px;
                }
            """)
            fallback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            strudel_layout.addWidget(fallback_label)
        
        # Code display area
        self.strudel_code_display = QTextEdit()
        self.strudel_code_display.setReadOnly(True)
        self.strudel_code_display.setFont(QFont("Courier New", 10))
        self.strudel_code_display.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #444;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        self.strudel_code_display.setPlaceholderText("Select a track to see its Strudel code here...")
        self.strudel_code_display.setMaximumHeight(150)
        
        strudel_layout.addWidget(self.strudel_code_display)
        
        strudel_group.setLayout(strudel_layout)
        splitter.addWidget(strudel_group)
        
        # Set splitter proportions (40% tracks, 60% player)
        splitter.setSizes([400, 800])
        
        layout.addWidget(splitter)
        widget.setLayout(layout)
        return widget
    
    def create_orchestra_tab(self):
        """Create the orchestra configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Header
        header = QLabel("🎼 Orchestra Configuration")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Control panel
        control_panel = QHBoxLayout()
        
        self.refresh_orchestra_btn = QPushButton("🔄 Refresh")
        self.refresh_orchestra_btn.clicked.connect(self.refresh_orchestra)
        control_panel.addWidget(self.refresh_orchestra_btn)
        
        self.add_chain_btn = QPushButton("➕ Add Chain")
        self.add_chain_btn.clicked.connect(self.add_chain)
        control_panel.addWidget(self.add_chain_btn)
        
        control_panel.addStretch()
        layout.addLayout(control_panel)
        
        # Orchestra table
        self.orchestra_table = QTableWidget()
        self.orchestra_table.setColumnCount(4)
        self.orchestra_table.setHorizontalHeaderLabels([
            "Chain Name", "Instrument Type", "RPC URL", "Sound Profile"
        ])
        layout.addWidget(self.orchestra_table)
        
        widget.setLayout(layout)
        return widget
    
    def setup_status_bar(self):
        """Setup the status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Golem Blockchain Audio Aggregator")
    
    def setup_menu(self):
        """Setup the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        export_action = file_menu.addAction("Export Data")
        export_action.triggered.connect(self.export_data)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction("Exit")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu("Help")
        
        about_action = help_menu.addAction("About")
        about_action.triggered.connect(self.show_about)
    
    def apply_dark_theme(self):
        """Apply a dark theme to the application"""
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(0, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.ColorRole.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.ColorRole.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.ColorRole.HighlightedText, QColor(0, 0, 0))
        
        self.setPalette(dark_palette)
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        self.blockchain_data = {
            "ethereum": {
                "price": 4272.26,
                "volume": 5000000000,
                "gas_fee": 0.0,
                "transactions": 85,
                "blocks": 19500000,
                "volatility": 3.07
            },
            "optimism": {
                "price": 2.85,
                "volume": 800000000,
                "gas_fee": 0.001,
                "transactions": 120,
                "blocks": 12000000,
                "volatility": 4.2
            },
            "polygon": {
                "price": 0.8,
                "volume": 500000000,
                "gas_fee": 30.0,
                "transactions": 5000,
                "blocks": 50000000,
                "volatility": 6.94
            },
            "base": {
                "price": 0.0003,
                "volume": 300000000,
                "gas_fee": 0.002,
                "transactions": 200,
                "blocks": 8000000,
                "volatility": 5.8
            }
        }
        
        # Create AnalyzedMetric objects for the dynamic generator
        self.analyzed_metrics = {
            "ethereum": AnalyzedMetric(
                chain_name="ethereum",
                timestamp=datetime.now(),
                price_change_percentage=15.5,
                gas_fee_trend=25.3,
                transaction_volume_change=40.2,
                block_production_rate=150.0,
                network_activity_score=75.8,
                volatility_index=65.2,
                liquidity_score=80.1
            ),
            "optimism": AnalyzedMetric(
                chain_name="optimism",
                timestamp=datetime.now(),
                price_change_percentage=22.3,
                gas_fee_trend=45.1,
                transaction_volume_change=65.7,
                block_production_rate=180.0,
                network_activity_score=82.4,
                volatility_index=58.9,
                liquidity_score=75.3
            ),
            "polygon": AnalyzedMetric(
                chain_name="polygon",
                timestamp=datetime.now(),
                price_change_percentage=30.1,
                gas_fee_trend=55.8,
                transaction_volume_change=80.3,
                block_production_rate=250.0,
                network_activity_score=88.7,
                volatility_index=70.5,
                liquidity_score=85.4
            ),
            "base": AnalyzedMetric(
                chain_name="base",
                timestamp=datetime.now(),
                price_change_percentage=18.7,
                gas_fee_trend=35.2,
                transaction_volume_change=55.9,
                block_production_rate=200.0,
                network_activity_score=78.1,
                volatility_index=62.3,
                liquidity_score=82.7
            )
        }
        
        # Create ChainInstrument objects
        self.chain_instruments = {
            "ethereum": ChainInstrument(
                chain_name="ethereum",
                instrument_type="synthesizer",
                rpc_node_url="https://mainnet.infura.io/v3/your-key",
                sound_profile="gm_synth_lead",
                created_at=datetime.now()
            ),
            "optimism": ChainInstrument(
                chain_name="optimism",
                instrument_type="lead",
                rpc_node_url="https://optimism-mainnet.infura.io/v3/your-key",
                sound_profile="gm_lead_6_voice",
                created_at=datetime.now()
            ),
            "polygon": ChainInstrument(
                chain_name="polygon",
                instrument_type="drum",
                rpc_node_url="https://polygon-rpc.com",
                sound_profile="RolandTR909",
                created_at=datetime.now()
            ),
            "base": ChainInstrument(
                chain_name="base",
                instrument_type="bass",
                rpc_node_url="https://mainnet.base.org",
                sound_profile="gm_acoustic_bass",
                created_at=datetime.now()
            )
        }
        
        # Generate initial tracks using the dynamic generator
        self.strudel_tracks = []
        
        # Generate a track for each chain
        for chain_name in ["ethereum", "optimism", "polygon", "base"]:
            metric = self.analyzed_metrics[chain_name]
            instrument = self.chain_instruments[chain_name]
            
            # Generate basic track
            track = self.strudel_generator.generate_track(metric, instrument)
            self.strudel_tracks.append({
                "id": f"{chain_name}_dynamic",
                "chain": chain_name,
                "timestamp": track.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": track.musical_parameters.tempo,
                "instrument": track.musical_parameters.instrument_type,
                "effects": ", ".join(track.musical_parameters.effects) if track.musical_parameters.effects else "none",
                "code": track.strudel_code_string,
                "track_obj": track
            })
        
        # Generate multi-chain track
        multi_track = self.strudel_generator.generate_multi_chain_track(
            list(self.analyzed_metrics.values()),
            list(self.chain_instruments.values())
        )
        self.strudel_tracks.append({
            "id": "multi_chain_dynamic",
            "chain": "multi",
            "timestamp": multi_track.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "tempo": multi_track.musical_parameters.tempo,
            "instrument": "orchestra",
            "effects": ", ".join(multi_track.musical_parameters.effects) if multi_track.musical_parameters.effects else "none",
            "code": multi_track.strudel_code_string,
            "track_obj": multi_track
        })
        
        self.orchestra_data = [
            {
                "chain": "ethereum",
                "instrument": "synthesizer",
                "rpc_url": "https://mainnet.infura.io/v3/your-key",
                "sound_profile": "gm_synth_lead"
            },
            {
                "chain": "optimism",
                "instrument": "lead",
                "rpc_url": "https://optimism-mainnet.infura.io/v3/your-key",
                "sound_profile": "gm_lead_6_voice"
            },
            {
                "chain": "polygon",
                "instrument": "drum",
                "rpc_url": "https://polygon-rpc.com",
                "sound_profile": "RolandTR909"
            },
            {
                "chain": "base",
                "instrument": "bass",
                "rpc_url": "https://mainnet.base.org",
                "sound_profile": "gm_acoustic_bass"
            }
        ]
        
        # Save data to JSON file
        self.save_data_to_json()
        
        self.update_all_displays()
    
    def save_data_to_json(self):
        """Save all blockchain data and tracks to JSON file"""
        try:
            data_to_save = {
                "blockchain_data": self.blockchain_data,
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
                    for chain, metric in self.analyzed_metrics.items()
                },
                "chain_instruments": {
                    chain: {
                        "chain_name": instrument.chain_name,
                        "instrument_type": instrument.instrument_type,
                        "rpc_node_url": instrument.rpc_node_url,
                        "sound_profile": instrument.sound_profile,
                        "created_at": instrument.created_at.isoformat()
                    }
                    for chain, instrument in self.chain_instruments.items()
                },
                "strudel_tracks": [
                    {
                        "id": track["id"],
                        "chain": track["chain"],
                        "timestamp": track["timestamp"],
                        "tempo": track["tempo"],
                        "instrument": track["instrument"],
                        "effects": track["effects"],
                        "code": track["code"]
                    }
                    for track in self.strudel_tracks
                ],
                "generated_at": datetime.now().isoformat()
            }
            
            with open("blockchain_audio_data.json", "w") as f:
                json.dump(data_to_save, f, indent=2)
                
            print("✅ Data saved to blockchain_audio_data.json")
            
        except Exception as e:
            print(f"❌ Error saving data to JSON: {e}")
    
    def generate_new_pattern(self):
        """Generate a new pattern using the dynamic generator"""
        current_chain = self.chain_combo.currentText()
        pattern_type = self.pattern_type_combo.currentText()
        
        if current_chain not in self.analyzed_metrics:
            QMessageBox.warning(self, "Warning", "Please select a valid chain first.")
            return
        
        try:
            metric = self.analyzed_metrics[current_chain]
            instrument = self.chain_instruments[current_chain]
            
            # Generate pattern based on type
            if pattern_type == "basic":
                track = self.strudel_generator.generate_track(metric, instrument)
                code = track.strudel_code_string
            else:
                code = self.strudel_generator.generate_advanced_pattern(metric, instrument, pattern_type)
            
            # Create new track entry
            new_track = {
                "id": f"{current_chain}_{pattern_type}_{int(datetime.now().timestamp())}",
                "chain": current_chain,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": 120,  # Will be updated from generated pattern
                "instrument": instrument.instrument_type,
                "effects": pattern_type,
                "code": code
            }
            
            # Add to tracks list
            self.strudel_tracks.append(new_track)
            
            # Update display
            self.update_strudel_tracks()
            
            # Select the new track
            self.tracks_table.selectRow(len(self.strudel_tracks) - 1)
            self.load_track_code(new_track)
            
            self.status_bar.showMessage(f"Generated new {pattern_type} pattern for {current_chain}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate pattern: {str(e)}")
    
    def generate_multi_chain_pattern(self):
        """Generate a multi-chain jam session using the same dynamic interpolation as single-chain"""
        try:
            pattern_type = self.pattern_type_combo.currentText()
            
            # Get all chain data
            ethereum_metric = self.analyzed_metrics["ethereum"]
            optimism_metric = self.analyzed_metrics["optimism"]
            polygon_metric = self.analyzed_metrics["polygon"]
            base_metric = self.analyzed_metrics["base"]
            
            ethereum_instrument = self.chain_instruments["ethereum"]
            optimism_instrument = self.chain_instruments["optimism"]
            polygon_instrument = self.chain_instruments["polygon"]
            base_instrument = self.chain_instruments["base"]
            
            # Calculate collaborative tempo based on all chains using the same interpolation
            eth_tempo = int(self.strudel_generator._map_to_range(
                self.strudel_generator._normalize_value(abs(ethereum_metric.price_change_percentage), 0, 50), 60, 180
            ))
            opt_tempo = int(self.strudel_generator._map_to_range(
                self.strudel_generator._normalize_value(abs(optimism_metric.price_change_percentage), 0, 50), 60, 180
            ))
            poly_tempo = int(self.strudel_generator._map_to_range(
                self.strudel_generator._normalize_value(abs(polygon_metric.price_change_percentage), 0, 50), 60, 180
            ))
            base_tempo = int(self.strudel_generator._map_to_range(
                self.strudel_generator._normalize_value(abs(base_metric.price_change_percentage), 0, 50), 60, 180
            ))
            
            avg_tempo = int((eth_tempo + opt_tempo + poly_tempo + base_tempo) / 4)
            
            # Generate dynamic patterns for each chain using the same interpolation methods
            eth_rhythmic = self.strudel_generator._generate_rhythmic_pattern(ethereum_metric)
            eth_melodic = self.strudel_generator._generate_melodic_pattern(ethereum_metric)
            eth_harmonic = self.strudel_generator._generate_harmonic_pattern(ethereum_metric)
            eth_textural = self.strudel_generator._generate_textural_pattern(ethereum_metric)
            eth_effects = self.strudel_generator._generate_effects_chain(ethereum_metric)
            
            opt_rhythmic = self.strudel_generator._generate_rhythmic_pattern(optimism_metric)
            opt_melodic = self.strudel_generator._generate_melodic_pattern(optimism_metric)
            opt_harmonic = self.strudel_generator._generate_harmonic_pattern(optimism_metric)
            opt_textural = self.strudel_generator._generate_textural_pattern(optimism_metric)
            opt_effects = self.strudel_generator._generate_effects_chain(optimism_metric)
            
            poly_rhythmic = self.strudel_generator._generate_rhythmic_pattern(polygon_metric)
            poly_melodic = self.strudel_generator._generate_melodic_pattern(polygon_metric)
            poly_harmonic = self.strudel_generator._generate_harmonic_pattern(polygon_metric)
            poly_textural = self.strudel_generator._generate_textural_pattern(polygon_metric)
            poly_effects = self.strudel_generator._generate_effects_chain(polygon_metric)
            
            base_rhythmic = self.strudel_generator._generate_rhythmic_pattern(base_metric)
            base_melodic = self.strudel_generator._generate_melodic_pattern(base_metric)
            base_harmonic = self.strudel_generator._generate_harmonic_pattern(base_metric)
            base_textural = self.strudel_generator._generate_textural_pattern(base_metric)
            base_effects = self.strudel_generator._generate_effects_chain(base_metric)
            
            # Create a truly collaborative jam session with dynamic interpolation
            if pattern_type == "experimental":
                combined_code = f"""// Multi-Chain Dynamic Jam Session - {pattern_type.title()}
// Generated: {datetime.now().isoformat()}
// Ethereum: Lead | Optimism: Harmony | Polygon: Percussion | Base: Bass

setcps({avg_tempo/60:.2f})

stack(
  // 🥁 COLLABORATIVE RHYTHM SECTION
  // Each chain contributes unique rhythmic elements
  s("{eth_rhythmic['kick']}").gain({random.uniform(0.7, 1.0):.2f}).room(0.2),
  s("{opt_rhythmic['snare']}").gain({random.uniform(0.5, 0.8):.2f}).room(0.3),
  s("{poly_rhythmic['hihat']}").gain({random.uniform(0.3, 0.6):.2f}).room(0.1),
  s("{base_rhythmic['kick']}").gain({random.uniform(0.4, 0.7):.2f}).room(0.2),
  
  // 🎹 ETHEREUM - Lead Melody (Dynamic interpolation)
  n("{eth_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_lead_6_voice")
  .clip({eth_textural['texture']})
  .jux(rev)
  .room({random.uniform(0.5, 2.0):.1f})
  .lpf({eth_textural['modulation']})
  .gain({random.uniform(0.6, 0.9):.2f})
  {''.join(eth_effects[:3])},
  
  // 🎼 OPTIMISM - Harmony Layer (Dynamic interpolation)
  n("{opt_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")  // Use shared scale
  .s("gm_lead_3_calliope")
  .clip({opt_textural['texture']})
  .room({random.uniform(0.4, 1.5):.1f})
  .lpf({opt_textural['modulation']})
  .gain({random.uniform(0.4, 0.7):.2f})
  {''.join(opt_effects[:2])},
  
  // 🎸 BASE - Bass Foundation (Dynamic interpolation)
  n("{base_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")  // Use shared scale
  .s("gm_acoustic_bass")
  .gain({random.uniform(0.5, 0.8):.2f})
  .lpf({random.randint(200, 600)})
  .room({random.uniform(0.3, 0.8):.1f})
  {''.join(base_effects[:2])},
  
  // 🎛️ POLYGON - Percussion & Texture (Dynamic interpolation)
  n("{poly_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")  // Use shared scale
  .s("gm_synth_pad_2_warm")
  .gain({random.uniform(0.2, 0.5):.2f})
  .room({random.uniform(0.6, 1.2):.1f})
  .shape({random.uniform(0.2, 0.5):.1f})
  .delay({random.uniform(0.05, 0.15):.2f})
  .lpf({poly_textural['modulation']})
  {''.join(poly_effects[:2])},
  
  // 🎼 COLLABORATIVE HARMONIC LAYER
  // All chains contribute to the harmony with dynamic interpolation
  n("{eth_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_synth_strings_2")
  .gain({random.uniform(0.1, 0.3):.2f})
  .room({random.uniform(0.8, 1.5):.1f})
  .shape({random.uniform(0.2, 0.4):.1f})
  .delay({random.uniform(0.03, 0.08):.2f})
  
  // 🎵 INTERACTIVE ELEMENTS - Chains respond to each other
  .mask("<0 1 1 0>/8")  // Ethereum leads
  .mask("<1 0 0 1>/8")  // Optimism responds
  .mask("<0 0 1 1>/8")  // Polygon adds texture
  .mask("<1 1 0 0>/8")  // Base provides foundation
)
.late("[0 .01]*2")
.size({random.uniform(2.0, 4.0):.1f})
"""
            
            elif pattern_type == "minimal":
                combined_code = f"""// Multi-Chain Minimal Jam - {pattern_type.title()}
// Generated: {datetime.now().isoformat()}
// Clean collaboration with dynamic interpolation

setcps({avg_tempo/60:.2f})

stack(
  // 🥁 MINIMAL RHYTHM
  s("{eth_rhythmic['kick']}").gain({random.uniform(0.8, 1.0):.2f}),
  s("{opt_rhythmic['snare']}").gain({random.uniform(0.4, 0.6):.2f}),
  
  // 🎹 ETHEREUM - Lead
  n("{eth_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_lead_3_calliope")
  .gain({random.uniform(0.5, 0.7):.2f})
  .room({random.uniform(0.4, 0.8):.1f}),
  
  // 🎼 OPTIMISM - Harmony
  n("{opt_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_lead_6_voice")
  .gain({random.uniform(0.3, 0.5):.2f})
  .room({random.uniform(0.3, 0.6):.1f}),
  
  // 🎸 BASE - Bass
  n("{base_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_acoustic_bass")
  .gain({random.uniform(0.4, 0.6):.2f})
  .lpf({random.randint(250, 400)}),
  
  // 🎛️ POLYGON - Pad
  n("{poly_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_synth_pad_2_warm")
  .gain({random.uniform(0.2, 0.4):.2f})
  .room({random.uniform(0.5, 0.9):.1f})
)
"""
            
            else:  # basic
                combined_code = f"""// Multi-Chain Basic Jam - {pattern_type.title()}
// Generated: {datetime.now().isoformat()}
// Simple collaboration with dynamic interpolation

setcps({avg_tempo/60:.2f})

stack(
  // 🥁 BASIC RHYTHM
  s("{eth_rhythmic['kick']}").gain({random.uniform(0.7, 0.9):.2f}),
  s("{opt_rhythmic['snare']}").gain({random.uniform(0.5, 0.7):.2f}),
  s("{poly_rhythmic['hihat']}").gain({random.uniform(0.3, 0.5):.2f}),
  
  // 🎹 ETHEREUM - Lead
  n("{eth_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_lead_6_voice")
  .gain({random.uniform(0.6, 0.8):.2f})
  .room({random.uniform(0.5, 1.0):.1f}),
  
  // 🎼 OPTIMISM - Harmony
  n("{opt_melodic['pattern']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_lead_3_calliope")
  .gain({random.uniform(0.4, 0.6):.2f})
  .room({random.uniform(0.4, 0.8):.1f}),
  
  // 🎸 BASE - Bass
  n("{base_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_acoustic_bass")
  .gain({random.uniform(0.5, 0.7):.2f})
  .lpf({random.randint(300, 500)}),
  
  // 🎛️ POLYGON - Pad
  n("{poly_harmonic['chord_progression']}")
  .scale("{eth_melodic['scale']}")
  .s("gm_synth_pad_2_warm")
  .gain({random.uniform(0.3, 0.5):.2f})
  .room({random.uniform(0.6, 1.0):.1f})
  .shape({random.uniform(0.2, 0.4):.1f})
)
"""
            
            # Create new track entry
            new_track = {
                "id": f"multi_chain_dynamic_{pattern_type}_{int(datetime.now().timestamp())}",
                "chain": "multi_dynamic",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": avg_tempo,
                "instrument": "orchestra",
                "effects": f"{pattern_type} dynamic jam",
                "code": combined_code.strip(),
                "track_obj": None
            }
            
            # Add to tracks list
            self.strudel_tracks.append(new_track)
            
            # Update display and save data
            self.update_strudel_tracks()
            self.save_data_to_json()
            
            # Select the new track
            self.tracks_table.selectRow(len(self.strudel_tracks) - 1)
            self.load_track_code(new_track)
            
            self.status_bar.showMessage(f"Generated multi-chain dynamic jam - {pattern_type} (tempo: {avg_tempo} BPM)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate multi-chain jam: {str(e)}")
    
    def generate_blockchain_symphony(self):
        """Generate a symphony that combines all blockchain data into one musical composition (legacy method)"""
        ethereum_data = self.blockchain_data["ethereum"]
        bitcoin_data = self.blockchain_data["bitcoin"]
        polygon_data = self.blockchain_data["polygon"]
        
        # Calculate musical parameters based on blockchain data
        ethereum_tempo = max(60, min(180, int(ethereum_data["volatility"] * 20)))
        bitcoin_tempo = max(60, min(180, int(bitcoin_data["volatility"] * 20)))
        polygon_tempo = max(60, min(180, int(polygon_data["volatility"] * 20)))
        
        # Price-based note patterns
        eth_notes = self.price_to_notes(ethereum_data["price"], "ethereum")
        btc_notes = self.price_to_notes(bitcoin_data["price"], "bitcoin")
        poly_notes = self.price_to_notes(polygon_data["price"], "polygon")
        
        # Volume-based rhythm patterns
        eth_rhythm = self.volume_to_rhythm(ethereum_data["volume"])
        btc_rhythm = self.volume_to_rhythm(bitcoin_data["volume"])
        poly_rhythm = self.volume_to_rhythm(polygon_data["volume"])
        
        # Gas fee-based effects
        eth_effects = self.gas_to_effects(ethereum_data["gas_fee"])
        btc_effects = self.gas_to_effects(bitcoin_data["gas_fee"])
        poly_effects = self.gas_to_effects(polygon_data["gas_fee"])
        
        symphony_code = f"""
// 🎵 BLOCKCHAIN SYMPHONY - Generated from Real Data
// Ethereum: ${ethereum_data["price"]:,.2f} | Bitcoin: ${bitcoin_data["price"]:,.2f} | Polygon: ${polygon_data["price"]:,.2f}

samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

// Main symphony - all blockchains playing together
stack(
  // 🟦 ETHEREUM LAYER - Lead (High frequency, complex patterns)
  n("{eth_notes}")
    .sound("piano")
    .gain(0.4)
    .{eth_effects}
    .lpf(1200)
    .hpf(200),
    
  // 🟨 BITCOIN LAYER - Bass/Foundation (Low frequency, steady rhythm)
  n("{btc_notes}")
    .sound("bd")
    .gain(0.6)
    .{btc_effects}
    .lpf(800)
    .gain(0.7),
    
  // 🟣 POLYGON LAYER - Percussion/Texture (Mid frequency, fast patterns)
  n("{poly_notes}")
    .sound("hh")
    .gain(0.5)
    .{poly_effects}
    .hpf(400)
    .lpf(2000),
    
  // 🥁 RHYTHM SECTION - Based on transaction volumes
  s("{eth_rhythm}").gain(0.3),
  s("{btc_rhythm}").gain(0.4),
  s("{poly_rhythm}").gain(0.2),
  
  // 🎼 HARMONIC LAYER - Price correlations
  n("c3 e3 g3 bb3 d4 f4 a4")
    .sound("piano")
    .gain(0.2)
    .lpf(600)
    .room(0.3)
    .size(0.5),
    
  // 🌊 AMBIENT LAYER - Network activity
  n("~ c2 ~ e2 ~ g2 ~ bb2")
    .sound("piano")
    .gain(0.15)
    .lpf(400)
    .room(0.8)
    .size(0.9)
    .delay(0.3)
    .delayfeedback(0.2)
)

// 🎵 The blockchain symphony plays on...
// Each chain contributes its unique voice to the digital orchestra
"""
        return symphony_code.strip()
    
    def price_to_notes(self, price, chain):
        """Convert price to musical notes"""
        if chain == "ethereum":
            # Ethereum: C major scale, price determines octave and pattern
            base_notes = ["c", "d", "e", "f", "g", "a", "b"]
            octave = 3 + (int(price) % 1000) // 200
            pattern_length = 3 + (int(price) % 10)
            notes = []
            for i in range(pattern_length):
                note = base_notes[i % len(base_notes)]
                notes.append(f"{note}{octave}")
            return " ".join(notes)
        
        elif chain == "bitcoin":
            # Bitcoin: Pentatonic scale, more stable
            base_notes = ["c", "d", "e", "g", "a"]
            octave = 2 + (int(price) % 10000) // 2000
            pattern_length = 2 + (int(price) % 5)
            notes = []
            for i in range(pattern_length):
                note = base_notes[i % len(base_notes)]
                notes.append(f"{note}{octave}")
            return " ".join(notes)
        
        else:  # polygon
            # Polygon: Chromatic scale, more experimental
            base_notes = ["c", "c#", "d", "d#", "e", "f", "f#", "g", "g#", "a", "a#", "b"]
            octave = 4 + (int(price * 100) % 100) // 20
            pattern_length = 4 + (int(price * 100) % 8)
            notes = []
            for i in range(pattern_length):
                note = base_notes[i % len(base_notes)]
                notes.append(f"{note}{octave}")
            return " ".join(notes)
    
    def volume_to_rhythm(self, volume):
        """Convert volume to rhythm pattern"""
        if volume > 5000000000:  # High volume
            return "bd sd bd sd, hh*8"
        elif volume > 1000000000:  # Medium volume
            return "bd sd, hh*4"
        else:  # Low volume
            return "bd, hh*2"
    
    def gas_to_effects(self, gas_fee):
        """Convert gas fee to audio effects"""
        if gas_fee > 50:
            return "room(0.8).size(0.9).delay(0.2).delayfeedback(0.3)"
        elif gas_fee > 20:
            return "room(0.4).size(0.6).delay(0.1)"
        else:
            return "room(0.2).size(0.3)"
    
    def update_all_displays(self):
        """Update all display widgets"""
        self.update_blockchain_display()
        self.update_strudel_tracks()
        self.update_orchestra_display()
    
    def refresh_blockchain_data(self):
        """Refresh blockchain data"""
        self.status_bar.showMessage("Refreshing blockchain data...")
        QTimer.singleShot(1000, lambda: self.status_bar.showMessage("Blockchain data refreshed"))
        self.update_blockchain_display()
    
    def update_blockchain_display(self):
        """Update blockchain data display"""
        chain = self.chain_combo.currentText()
        
        if chain not in self.blockchain_data:
            return
        
        data = self.blockchain_data[chain]
        
        # Update table
        metrics = [
            ("Chain Name", chain.title()),
            ("Price", f"${data['price']:,.2f}"),
            ("Volume", f"${data['volume']:,.0f}"),
            ("Gas Fee", f"{data['gas_fee']:.2f} Gwei"),
            ("Transactions", str(data['transactions'])),
            ("Block Number", str(data['blocks'])),
            ("Volatility", f"{data['volatility']:.2f}%")
        ]
        
        self.data_table.setRowCount(len(metrics))
        for i, (metric, value) in enumerate(metrics):
            self.data_table.setItem(i, 0, QTableWidgetItem(metric))
            self.data_table.setItem(i, 1, QTableWidgetItem(str(value)))
        
        # Update charts if matplotlib is available
        if MATPLOTLIB_AVAILABLE:
            self.update_charts(chain)
    
    def update_charts(self, chain):
        """Update the charts"""
        data = self.blockchain_data[chain]
        
        # Price chart
        self.price_fig.clear()
        ax1 = self.price_fig.add_subplot(111)
        
        # Simulate price data over time
        import numpy as np
        days = np.arange(7)
        base_price = data['price']
        prices = base_price + np.random.normal(0, base_price * 0.05, 7)
        
        ax1.plot(days, prices, 'b-', linewidth=2, marker='o')
        ax1.set_title(f"{chain.title()} Price Over Time")
        ax1.set_ylabel("Price (USD)")
        ax1.grid(True, alpha=0.3)
        
        self.price_canvas.draw()
        
        # Activity chart
        self.activity_fig.clear()
        ax2 = self.activity_fig.add_subplot(111)
        
        # Simulate activity data
        tx_counts = [data['transactions'] + np.random.randint(-10, 10) for _ in range(7)]
        gas_fees = [data['gas_fee'] + np.random.uniform(-5, 5) for _ in range(7)]
        
        ax2_twin = ax2.twinx()
        
        line1 = ax2.plot(days, tx_counts, 'g-', label='Transactions', linewidth=2, marker='s')
        line2 = ax2_twin.plot(days, gas_fees, 'r-', label='Gas Fee (Gwei)', linewidth=2, marker='^')
        
        ax2.set_title(f"{chain.title()} Network Activity")
        ax2.set_ylabel("Transaction Count", color='g')
        ax2_twin.set_ylabel("Gas Fee (Gwei)", color='r')
        ax2.grid(True, alpha=0.3)
        
        # Combine legends
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax2.legend(lines, labels, loc='upper left')
        
        self.activity_canvas.draw()
    
    def refresh_strudel_tracks(self):
        """Refresh Strudel tracks and regenerate symphony"""
        self.status_bar.showMessage("Refreshing blockchain symphony...")
        # Regenerate the symphony with current data
        self.strudel_tracks[0]["code"] = self.generate_blockchain_symphony()
        QTimer.singleShot(1000, lambda: self.status_bar.showMessage("Blockchain symphony refreshed"))
        self.update_strudel_tracks()
    
    def update_strudel_tracks(self):
        """Update Strudel tracks display"""
        self.tracks_table.setRowCount(len(self.strudel_tracks))
        
        for i, track in enumerate(self.strudel_tracks):
            self.tracks_table.setItem(i, 0, QTableWidgetItem(track['id']))
            self.tracks_table.setItem(i, 1, QTableWidgetItem(track['chain']))
            self.tracks_table.setItem(i, 2, QTableWidgetItem(track['timestamp']))
            self.tracks_table.setItem(i, 3, QTableWidgetItem(f"{track['tempo']} BPM"))
            self.tracks_table.setItem(i, 4, QTableWidgetItem(track['instrument']))
            self.tracks_table.setItem(i, 5, QTableWidgetItem(track['effects']))
    
    def on_track_selected(self):
        """Handle track selection"""
        current_row = self.tracks_table.currentRow()
        if current_row >= 0 and current_row < len(self.strudel_tracks):
            track = self.strudel_tracks[current_row]
            self.display_track_details(track)
            self.load_track_code(track)
    
    def display_track_details(self, track):
        """Display detailed track information"""
        details = f"""
Track ID: {track['id']}
Chain: {track['chain']}
Timestamp: {track['timestamp']}

Musical Parameters:
- Tempo: {track['tempo']} BPM
- Instrument: {track['instrument']}
- Effects: {track['effects'] if track['effects'] else 'None'}
"""
        self.track_details.setPlainText(details)
    
    def load_track_code(self, track):
        """Load track code into the Strudel display"""
        self.strudel_code_display.setPlainText(track['code'].strip())
    
    def load_strudel_website(self):
        """Load Strudel website in the integrated browser"""
        if WEBENGINE_AVAILABLE:
            self.strudel_webview.load(QUrl("https://strudel.tidalcycles.org/"))
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Strudel website loaded in integrated browser")
        else:
            webbrowser.open("https://strudel.tidalcycles.org/")
            if hasattr(self, 'status_bar'):
                self.status_bar.showMessage("Strudel website opened in external browser")
    
    def load_selected_track(self):
        """Load selected track into Strudel"""
        current_row = self.tracks_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a track to load.")
            return
        
        track = self.strudel_tracks[current_row]
        
        if WEBENGINE_AVAILABLE:
            # Load Strudel website first
            self.load_strudel_website()
            
            # Show message with instructions
            QMessageBox.information(
                self, "Load Track in Strudel", 
                f"Track '{track['id']}' ready!\n\n"
                f"1. Copy the code from the display below\n"
                f"2. Paste it into the Strudel editor\n"
                f"3. Press Ctrl+Enter to play the track"
            )
        else:
            # Fallback to external browser
            webbrowser.open("https://strudel.tidalcycles.org/")
            QMessageBox.information(
                self, "Load Track in Strudel", 
                f"Track '{track['id']}' ready!\n\n"
                f"Strudel website opened in external browser.\n"
                f"Copy the code and paste it into Strudel."
            )
    
    def copy_track_code(self):
        """Copy the selected track code to clipboard"""
        current_row = self.tracks_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a track to copy.")
            return
        
        track = self.strudel_tracks[current_row]
        code = track['code'].strip()
        
        # Copy to clipboard
        clipboard = QApplication.clipboard()
        clipboard.setText(code)
        
        QMessageBox.information(self, "Success", "Track code copied to clipboard!")
    
    def export_track(self):
        """Export selected track to file"""
        current_row = self.tracks_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a track to export.")
            return
        
        track = self.strudel_tracks[current_row]
        
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Strudel Track", 
            f"{track['id']}.js", "JavaScript files (*.js);;All files (*.*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(track['code'])
                QMessageBox.information(self, "Success", f"Track exported to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export track: {e}")
    
    def refresh_orchestra(self):
        """Refresh orchestra data"""
        self.status_bar.showMessage("Refreshing orchestra data...")
        QTimer.singleShot(1000, lambda: self.status_bar.showMessage("Orchestra data refreshed"))
        self.update_orchestra_display()
    
    def update_orchestra_display(self):
        """Update orchestra display"""
        self.orchestra_table.setRowCount(len(self.orchestra_data))
        
        for i, entry in enumerate(self.orchestra_data):
            self.orchestra_table.setItem(i, 0, QTableWidgetItem(entry['chain']))
            self.orchestra_table.setItem(i, 1, QTableWidgetItem(entry['instrument']))
            self.orchestra_table.setItem(i, 2, QTableWidgetItem(entry['rpc_url']))
            self.orchestra_table.setItem(i, 3, QTableWidgetItem(entry['sound_profile']))
    
    def add_chain(self):
        """Add new chain to orchestra (placeholder)"""
        QMessageBox.information(
            self, "Add Chain", 
            "This feature will allow you to add new blockchain-instrument mappings."
        )
    
    def export_data(self):
        """Export all data to files"""
        QMessageBox.information(
            self, "Export Data", 
            "This feature will export all blockchain data and Strudel tracks to files."
        )
    
    def show_about(self):
        """Show about dialog"""
        webengine_status = "✅ Available" if WEBENGINE_AVAILABLE else "❌ Not Available"
        matplotlib_status = "✅ Available" if MATPLOTLIB_AVAILABLE else "❌ Not Available"
        
        QMessageBox.about(
            self, "About",
            f"""Golem Blockchain Audio Aggregator

A comprehensive GUI for interacting with blockchain data and Strudel tracks.

Built with PyQt6 and Python.

Features:
• Real-time blockchain data visualization
• Integrated Strudel player (WebEngine: {webengine_status})
• Interactive charts and analytics (matplotlib: {matplotlib_status})
• Orchestra configuration
• Track export and management

Note: This is a demo version with sample data."""
        )

def main():
    """Main function to run the GUI application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Golem Blockchain Audio Aggregator")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    window = GolemBlockchainGUI()
    window.show()
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
