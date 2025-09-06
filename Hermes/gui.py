#!/usr/bin/env python3
"""
Golem Blockchain Audio Aggregator - Single GUI with Integrated Web Browser
Everything in one file with Strudel player embedded
"""

import sys
import json
import webbrowser
from datetime import datetime
from typing import List, Optional

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
        self.tab_widget.addTab(self.strudel_tab, "🎵 Strudel Player")
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
        self.chain_combo.addItems(["ethereum", "bitcoin", "polygon"])
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
        header = QLabel("🎵 Strudel Audio Player")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Control panel
        control_panel = QHBoxLayout()
        
        self.refresh_tracks_btn = QPushButton("🔄 Refresh Tracks")
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
        
        self.load_track_btn = QPushButton("🎵 Load Track")
        self.load_track_btn.clicked.connect(self.load_selected_track)
        player_controls.addWidget(self.load_track_btn)
        
        player_controls.addStretch()
        strudel_layout.addLayout(player_controls)
        
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
            "bitcoin": {
                "price": 45000.0,
                "volume": 10000000000,
                "gas_fee": 50.0,
                "transactions": 2000,
                "blocks": 800000,
                "volatility": 5.05
            },
            "polygon": {
                "price": 0.8,
                "volume": 500000000,
                "gas_fee": 30.0,
                "transactions": 5000,
                "blocks": 50000000,
                "volatility": 6.94
            }
        }
        
        self.strudel_tracks = [
            {
                "id": "ethereum_1757194957",
                "chain": "ethereum",
                "timestamp": "2024-01-01 12:00:00",
                "tempo": 120,
                "instrument": "guitar",
                "effects": "hpf",
                "code": """
// Generated Strudel track for ethereum
samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    s("bd sd bd lt").gain(0.5),
    s("hh*16").gain(0.3),
    n("c3 e3 g3").sound("piano").gain(0.4)
)
"""
            },
            {
                "id": "bitcoin_1757194957",
                "chain": "bitcoin",
                "timestamp": "2024-01-01 12:00:00",
                "tempo": 120,
                "instrument": "drum",
                "effects": "",
                "code": """
// Generated Strudel track for bitcoin
samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    s("bd sd bd lt").gain(0.6),
    s("hh*8").gain(0.4),
    n("g3 bb3 d4").sound("bd").gain(0.5)
)
"""
            },
            {
                "id": "polygon_1757194957",
                "chain": "polygon",
                "timestamp": "2024-01-01 12:00:00",
                "tempo": 140,
                "instrument": "bass",
                "effects": "lpf",
                "code": """
// Generated Strudel track for polygon
samples('https://raw.githubusercontent.com/tidalcycles/Dirt-Samples/master/strudel.json')

stack(
    s("bd sd bd lt").gain(0.7),
    s("hh*12").gain(0.5),
    n("f2 a2 c3").sound("gm_synth_bass_1").gain(0.6)
)
"""
            }
        ]
        
        self.orchestra_data = [
            {
                "chain": "ethereum",
                "instrument": "guitar",
                "rpc_url": "https://lb.drpc.org/sepolia/AplHGB2v9khYpYVNxc5za0FxucDEi1sR8IqgqhnKxixj",
                "sound_profile": "moog"
            },
            {
                "chain": "bitcoin",
                "instrument": "drum",
                "rpc_url": "https://blockstream.info/api/",
                "sound_profile": "bd"
            },
            {
                "chain": "polygon",
                "instrument": "bass",
                "rpc_url": "https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
                "sound_profile": "gm_synth_bass_1"
            }
        ]
        
        self.update_all_displays()
    
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
        """Refresh Strudel tracks"""
        self.status_bar.showMessage("Refreshing Strudel tracks...")
        QTimer.singleShot(1000, lambda: self.status_bar.showMessage("Strudel tracks refreshed"))
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
