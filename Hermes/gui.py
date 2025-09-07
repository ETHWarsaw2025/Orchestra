#!/usr/bin/env python3
"""
Golem Blockchain Audio Aggregator - Single GUI with Integrated Web Browser
Everything in one file with Strudel player embedded
"""

import sys
import json
import random
import webbrowser
import subprocess
from datetime import datetime
from typing import List, Optional

# Import our custom modules
from strudel_generator import StrudelGenerator
from models import AnalyzedMetric, ChainInstrument, StrudelTrack
from golem_storage import GolemStorage
import asyncio

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
        self.golem_storage = GolemStorage()
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
        
        # Real data status indicator
        self.real_data_status = QLabel("📊 Sample Data Mode - Click 'Fetch Real Data' for live blockchain data")
        self.real_data_status.setStyleSheet("color: #888; font-style: italic; padding: 5px;")
        self.real_data_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.real_data_status)
        
        # Control panel
        control_panel = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Refresh Data")
        self.refresh_btn.clicked.connect(self.refresh_blockchain_data)
        control_panel.addWidget(self.refresh_btn)
        
        self.fetch_real_data_btn = QPushButton("🌐 Fetch Real Blockchain Data")
        self.fetch_real_data_btn.clicked.connect(self.fetch_real_blockchain_data)
        control_panel.addWidget(self.fetch_real_data_btn)
        
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
        
        self.load_real_data_btn = QPushButton("📊 Load Real Data Tracks")
        self.load_real_data_btn.clicked.connect(self.load_real_blockchain_data)
        control_panel.addWidget(self.load_real_data_btn)
        
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
        
        self.push_to_golem_btn = QPushButton("🚀 Push to Golem")
        self.push_to_golem_btn.clicked.connect(self.push_to_golem)
        self.push_to_golem_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        player_controls.addWidget(self.push_to_golem_btn)
        
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
        
        # Experimental chain selection
        generation_controls.addWidget(QLabel("Experimental Chain:"))
        self.experimental_chain_combo = QComboBox()
        self.experimental_chain_combo.addItems(["none", "ethereum", "optimism", "polygon", "base"])
        self.experimental_chain_combo.setCurrentText("none")
        generation_controls.addWidget(self.experimental_chain_combo)
        
        # Experimental multi-chain button
        self.experimental_multi_btn = QPushButton("🎨 Experimental Multi-Chain")
        self.experimental_multi_btn.clicked.connect(self.generate_experimental_multi_chain)
        generation_controls.addWidget(self.experimental_multi_btn)
        
        generation_controls.addStretch()
        strudel_layout.addLayout(generation_controls)
        
        # Individual chain pattern generation controls
        individual_controls = QHBoxLayout()
        individual_controls.addWidget(QLabel("Individual Chain Patterns:"))
        
        # Individual chain buttons
        self.ethereum_btn = QPushButton("🔷 Ethereum")
        self.ethereum_btn.clicked.connect(lambda: self.generate_individual_chain_pattern("ethereum"))
        individual_controls.addWidget(self.ethereum_btn)
        
        self.optimism_btn = QPushButton("🟠 Optimism")
        self.optimism_btn.clicked.connect(lambda: self.generate_individual_chain_pattern("optimism"))
        individual_controls.addWidget(self.optimism_btn)
        
        self.polygon_btn = QPushButton("🟣 Polygon")
        self.polygon_btn.clicked.connect(lambda: self.generate_individual_chain_pattern("polygon"))
        individual_controls.addWidget(self.polygon_btn)
        
        self.base_btn = QPushButton("🔵 Base")
        self.base_btn.clicked.connect(lambda: self.generate_individual_chain_pattern("base"))
        individual_controls.addWidget(self.base_btn)
        
        individual_controls.addStretch()
        strudel_layout.addLayout(individual_controls)
        
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
        """Generate a clean multi-chain pattern using individual chain generation"""
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
            
            # Use the clean multi-chain generation method
            multi_track = self.strudel_generator.generate_multi_chain_track(
                [ethereum_metric, optimism_metric, polygon_metric, base_metric],
                [ethereum_instrument, optimism_instrument, polygon_instrument, base_instrument]
            )
            
            # Create new track entry
            new_track = {
                "id": f"multi_chain_clean_{pattern_type}_{int(datetime.now().timestamp())}",
                "chain": "multi_clean",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": multi_track.musical_parameters.tempo,
                "instrument": "orchestra",
                "effects": f"{pattern_type} collaborative jam",
                "code": multi_track.strudel_code_string,
                "track_obj": multi_track
            }
            
            # Add to tracks list
            self.strudel_tracks.append(new_track)
            
            # Update display and save data
            self.update_strudel_tracks()
            self.save_data_to_json()
            
            # Select the new track
            self.tracks_table.selectRow(len(self.strudel_tracks) - 1)
            self.load_track_code(new_track)
            
            self.status_bar.showMessage(f"Generated clean multi-chain collaborative jam - {pattern_type} (tempo: {multi_track.musical_parameters.tempo} BPM)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate multi-chain jam: {str(e)}")
    
    def generate_experimental_multi_chain(self):
        """Generate experimental multi-chain with selected chain as lead"""
        try:
            experimental_chain = self.experimental_chain_combo.currentText()
            
            if experimental_chain == "none":
                QMessageBox.warning(self, "Warning", "Please select a chain for experimental generation.")
                return
            
            # Get all chain data
            ethereum_metric = self.analyzed_metrics["ethereum"]
            optimism_metric = self.analyzed_metrics["optimism"]
            polygon_metric = self.analyzed_metrics["polygon"]
            base_metric = self.analyzed_metrics["base"]
            
            ethereum_instrument = self.chain_instruments["ethereum"]
            optimism_instrument = self.chain_instruments["optimism"]
            polygon_instrument = self.chain_instruments["polygon"]
            base_instrument = self.chain_instruments["base"]
            
            # Generate experimental multi-chain with selected chain as lead
            multi_track = self.strudel_generator.generate_multi_chain_track(
                [ethereum_metric, optimism_metric, polygon_metric, base_metric],
                [ethereum_instrument, optimism_instrument, polygon_instrument, base_instrument],
                experimental_chain=experimental_chain
            )
            
            # Create new track entry
            new_track = {
                "id": f"multi_chain_experimental_{experimental_chain}_{int(datetime.now().timestamp())}",
                "chain": f"multi_experimental_{experimental_chain}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": multi_track.musical_parameters.tempo,
                "instrument": "experimental",
                "effects": f"experimental {experimental_chain} lead",
                "code": multi_track.strudel_code_string,
                "track_obj": multi_track
            }
            
            # Add to tracks list
            self.strudel_tracks.append(new_track)
            
            # Update display and save data
            self.update_strudel_tracks()
            self.save_data_to_json()
            
            # Select the new track
            self.tracks_table.selectRow(len(self.strudel_tracks) - 1)
            self.load_track_code(new_track)
            
            self.status_bar.showMessage(f"Generated experimental multi-chain with {experimental_chain} as lead (tempo: {multi_track.musical_parameters.tempo} BPM)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate experimental multi-chain: {str(e)}")
    
    def generate_individual_chain_pattern(self, chain_name):
        """Generate a pattern for a specific individual chain"""
        try:
            if chain_name not in self.analyzed_metrics:
                QMessageBox.warning(self, "Warning", f"Chain '{chain_name}' not found in analyzed metrics.")
                return
            
            if chain_name not in self.chain_instruments:
                QMessageBox.warning(self, "Warning", f"Chain '{chain_name}' not found in chain instruments.")
                return
            
            pattern_type = self.pattern_type_combo.currentText()
            
            # Get chain data
            metric = self.analyzed_metrics[chain_name]
            instrument = self.chain_instruments[chain_name]
            
            # Generate pattern based on type
            if pattern_type == "basic":
                track = self.strudel_generator.generate_track(metric, instrument)
                code = track.strudel_code_string
                tempo = track.musical_parameters.tempo
                effects = ", ".join(track.musical_parameters.effects) if track.musical_parameters.effects else "none"
            else:
                code = self.strudel_generator.generate_advanced_pattern(metric, instrument, pattern_type)
                # Extract tempo from the generated code
                tempo = 120  # Default tempo
                if "setcps(" in code:
                    try:
                        cps_line = [line for line in code.split('\n') if 'setcps(' in line][0]
                        cps_value = float(cps_line.split('setcps(')[1].split(')')[0])
                        tempo = int(cps_value * 60)  # Convert CPS to BPM
                    except:
                        tempo = 120
                effects = pattern_type
            
            # Create new track entry
            new_track = {
                "id": f"{chain_name}_{pattern_type}_{int(datetime.now().timestamp())}",
                "chain": chain_name,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tempo": tempo,
                "instrument": instrument.instrument_type,
                "effects": effects,
                "code": code
            }
            
            # Add to tracks list
            self.strudel_tracks.append(new_track)
            
            # Update display and save data
            self.update_strudel_tracks()
            self.save_data_to_json()
            
            # Select the new track
            self.tracks_table.selectRow(len(self.strudel_tracks) - 1)
            self.load_track_code(new_track)
            
            self.status_bar.showMessage(f"Generated {pattern_type} pattern for {chain_name} (tempo: {tempo} BPM)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate individual chain pattern for {chain_name}: {str(e)}")
    
    def push_to_golem(self):
        """Push selected track to Golem DB"""
        current_row = self.tracks_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a track to push to Golem.")
            return
        
        track_data = self.strudel_tracks[current_row]
        
        # Check if track has a track_obj (StrudelTrack object)
        if 'track_obj' in track_data and track_data['track_obj']:
            track_obj = track_data['track_obj']
        else:
            # Create a StrudelTrack object from the track data
            try:
                # Get the corresponding metric and instrument
                chain_name = track_data['chain']
                if chain_name in self.analyzed_metrics and chain_name in self.chain_instruments:
                    metric = self.analyzed_metrics[chain_name]
                    instrument = self.chain_instruments[chain_name]
                    
                    # Create a basic StrudelTrack object
                    from models import MusicalParameters
                    musical_params = MusicalParameters(
                        tempo=track_data['tempo'],
                        base_note="C4",
                        rhythm_pattern="dynamic",
                        gain=0.7,
                        sound_profile=instrument.sound_profile,
                        scale="C:major",
                        complexity=5,
                        effects=[],
                        instrument_type=instrument.instrument_type
                    )
                    
                    track_obj = StrudelTrack(
                        id=track_data['id'],
                        timestamp=datetime.now(),
                        chain_name=chain_name,
                        strudel_code_string=track_data['code'],
                        source_kpis=metric,
                        musical_parameters=musical_params,
                        created_at=datetime.now()
                    )
                else:
                    QMessageBox.warning(self, "Warning", f"Could not find metric or instrument data for chain: {chain_name}")
                    return
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to create StrudelTrack object: {str(e)}")
                return
        
        # Show confirmation dialog
        reply = QMessageBox.question(
            self, "Push to Golem", 
            f"Push track '{track_data['id']}' to Golem DB?\n\n"
            f"Chain: {track_data['chain']}\n"
            f"Tempo: {track_data['tempo']} BPM\n"
            f"Instrument: {track_data['instrument']}\n\n"
            f"This will store the track on the Golem network.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # Disable button during operation
            self.push_to_golem_btn.setEnabled(False)
            self.push_to_golem_btn.setText("🔄 Pushing...")
            self.status_bar.showMessage("Pushing track to Golem DB...")
            
            # Run the async operation
            try:
                # Create a new event loop for this operation
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                # Run the push operation
                success = loop.run_until_complete(self._push_track_to_golem(track_obj))
                
                if success:
                    QMessageBox.information(
                        self, "Success", 
                        f"Track '{track_data['id']}' successfully pushed to Golem DB!\n\n"
                        f"The track is now stored on the Golem network and can be "
                        f"retrieved by other users."
                    )
                    self.status_bar.showMessage(f"✅ Track '{track_data['id']}' pushed to Golem successfully")
                else:
                    QMessageBox.critical(
                        self, "Error", 
                        f"Failed to push track to Golem DB.\n\n"
                        f"Please check your Golem connection and try again."
                    )
                    self.status_bar.showMessage("❌ Failed to push track to Golem")
                
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", 
                    f"An error occurred while pushing to Golem:\n\n{str(e)}"
                )
                self.status_bar.showMessage("❌ Error pushing to Golem")
            finally:
                # Re-enable button
                self.push_to_golem_btn.setEnabled(True)
                self.push_to_golem_btn.setText("🚀 Push to Golem")
                loop.close()
    
    async def _push_track_to_golem(self, track: StrudelTrack) -> bool:
        """Async method to push track to Golem DB"""
        try:
            # Connect to Golem
            if not await self.golem_storage.connect():
                return False
            
            # Store the track
            success = await self.golem_storage.store_strudel_track(track)
            
            # Disconnect
            await self.golem_storage.disconnect()
            
            return success
            
        except Exception as e:
            print(f"Error in _push_track_to_golem: {e}")
            return False
    
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
    
    def fetch_real_blockchain_data(self):
        """Fetch real blockchain data from the last 10 blocks"""
        try:
            self.status_bar.showMessage("🌐 Fetching real blockchain data from last 10 blocks...")
            
            # Run the blockchain data fetcher
            result = subprocess.run(
                ["python", "blockchain_data_fetcher.py"],
                cwd=".",
                capture_output=True,
                text=True,
                timeout=120  # 2 minute timeout
            )
            
            if result.returncode == 0:
                # Load the generated real data
                self.load_real_blockchain_data()
                self.status_bar.showMessage("✅ Real blockchain data fetched successfully!")
                
                # Show success message
                QMessageBox.information(
                    self, "Success", 
                    "Real blockchain data fetched successfully!\n\n"
                    "Generated audio tracks from:\n"
                    "• Optimism (10 blocks)\n"
                    "• Polygon (10 blocks)\n" 
                    "• Base (10 blocks)\n\n"
                    "Check the Strudel tab to see the generated tracks!"
                )
            else:
                # Show error message
                error_msg = result.stderr if result.stderr else "Unknown error occurred"
                QMessageBox.critical(
                    self, "Error", 
                    f"Failed to fetch real blockchain data:\n\n{error_msg}"
                )
                self.status_bar.showMessage("❌ Failed to fetch real blockchain data")
                
        except subprocess.TimeoutExpired:
            QMessageBox.critical(
                self, "Timeout", 
                "Request timed out. The blockchain data fetch took too long."
            )
            self.status_bar.showMessage("❌ Request timed out")
        except Exception as e:
            QMessageBox.critical(
                self, "Error", 
                f"An error occurred while fetching real blockchain data:\n\n{str(e)}"
            )
            self.status_bar.showMessage("❌ Error fetching real blockchain data")
    
    def load_real_blockchain_data(self):
        """Load real blockchain data from the generated JSON file"""
        try:
            with open("real_blockchain_audio_data.json", "r") as f:
                real_data = json.load(f)
            
            # Update analyzed metrics with real data
            for chain, metrics in real_data["analyzed_metrics"].items():
                if chain in self.analyzed_metrics:
                    # Update existing metrics with real data
                    self.analyzed_metrics[chain] = AnalyzedMetric(
                        chain_name=metrics["chain_name"],
                        timestamp=datetime.fromisoformat(metrics["timestamp"]),
                        price_change_percentage=metrics["price_change_percentage"],
                        gas_fee_trend=metrics["gas_fee_trend"],
                        transaction_volume_change=metrics["transaction_volume_change"],
                        block_production_rate=metrics["block_production_rate"],
                        network_activity_score=metrics["network_activity_score"],
                        volatility_index=metrics["volatility_index"],
                        liquidity_score=metrics["liquidity_score"]
                    )
            
            # Add real data tracks to strudel_tracks
            for track in real_data["strudel_tracks"]:
                # Check if track already exists
                existing_track = next(
                    (t for t in self.strudel_tracks if t["id"] == track["id"]), 
                    None
                )
                if not existing_track:
                    self.strudel_tracks.append(track)
            
            # Update displays
            self.update_all_displays()
            
            # Update status indicator
            self.real_data_status.setText("✅ Real Data Mode - Live blockchain data from last 10 blocks")
            self.real_data_status.setStyleSheet("color: #4CAF50; font-weight: bold; padding: 5px;")
            
            print(f"✅ Loaded real blockchain data: {len(real_data['strudel_tracks'])} tracks")
            
        except FileNotFoundError:
            print("❌ real_blockchain_audio_data.json not found")
        except Exception as e:
            print(f"❌ Error loading real blockchain data: {e}")
    
    def update_blockchain_display(self):
        """Update blockchain data display"""
        chain = self.chain_combo.currentText()
        
        if chain not in self.blockchain_data:
            return
        
        data = self.blockchain_data[chain]
        
        # Check if we have real data for this chain
        has_real_data = chain in self.analyzed_metrics and self.analyzed_metrics[chain].network_activity_score != 50.0
        
        if has_real_data:
            # Show real blockchain data
            real_metrics = self.analyzed_metrics[chain]
            metrics = [
                ("Chain Name", f"{chain.title()} (Real Data)"),
                ("Activity Score", f"{real_metrics.network_activity_score:.1f}"),
                ("Volatility Index", f"{real_metrics.volatility_index:.1f}"),
                ("Liquidity Score", f"{real_metrics.liquidity_score:.1f}"),
                ("TX Volume Change", f"{real_metrics.transaction_volume_change:.1f}%"),
                ("Gas Fee Trend", f"{real_metrics.gas_fee_trend:.1f}%"),
                ("Block Production Rate", f"{real_metrics.block_production_rate:.1f} blocks/min"),
                ("Price Change", f"{real_metrics.price_change_percentage:.1f}%"),
                ("Data Source", "Last 10 blocks"),
                ("Timestamp", real_metrics.timestamp.strftime("%Y-%m-%d %H:%M:%S"))
            ]
        else:
            # Show sample data
            metrics = [
                ("Chain Name", f"{chain.title()} (Sample Data)"),
                ("Price", f"${data['price']:,.2f}"),
                ("Volume", f"${data['volume']:,.0f}"),
                ("Gas Fee", f"{data['gas_fee']:.2f} Gwei"),
                ("Transactions", str(data['transactions'])),
                ("Block Number", str(data['blocks'])),
                ("Volatility", f"{data['volatility']:.2f}%"),
                ("Data Source", "Sample data"),
                ("Note", "Click 'Fetch Real Data' for live data")
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
