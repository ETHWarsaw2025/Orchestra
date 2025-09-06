# Golem DB Practice

A simple practice project for working with Golem DB - the decentralized storage and computing platform.

## What is Golem DB?

Golem DB is a decentralized platform where you can:
1. **Store data** - Upload your data to the Golem network
2. **Retrieve data** - Query and download stored data
3. **Process data** - Use distributed computing for analysis

## Key Concept

**Golem DB doesn't have data by default** - you must store your data first before you can retrieve and analyze it.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with your Golem DB credentials:
   ```env
   PRIVATE_KEY=your_private_key_here
   RPC_URL=https://ethwarsaw.holesky.golemdb.io/rpc
   WS_URL=wss://ethwarsaw.holesky.golemdb.io/rpc/ws
   ```

3. **Run the Golem DB client:**
   ```bash
   python golem_db_client.py
   ```

## Files

- `golem_db_client.py` - Core Golem DB client functionality
- `crud.py` - Original blockchain analysis (kept for reference)
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (create this)

## Usage

The `GolemDBClient` class provides basic operations:

```python
from golem_db_client import GolemDBClient

# Create client
client = GolemDBClient()

# Connect
await client.connect()

# Store data
await client.store_entity("my_key", "my_value", {"type": "demo"})

# Retrieve data
entities = await client.retrieve_entities()

# Disconnect
await client.disconnect()
```

## Important Notes

- Golem DB requires you to store data before you can retrieve it
- This is a two-step process: Store → Retrieve → Analyze
- The platform provides decentralized storage and computing
- Data persists on the Golem network for future use

## Getting Help

- Check the Golem documentation for advanced features
- Ensure your account has sufficient balance for operations
- Verify your network connection and credentials