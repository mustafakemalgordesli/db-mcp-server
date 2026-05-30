import pytest
from sqlalchemy import text
from db_mcp_server.provider import DatabaseProvider, DatabaseManager

def test_database_provider_sqlite():
    provider = DatabaseProvider("sqlite", "sqlite:///:memory:")
    
    with provider.connect() as conn:
        conn.execute(text("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)"))
        conn.execute(text("INSERT INTO test (id, name) VALUES (1, 'Alice')"))
        conn.execute(text("INSERT INTO test (id, name) VALUES (2, 'Bob')"))
        conn.commit()

    tables_query = provider.get_tables_query()
    with provider.connect() as conn:
        result = conn.execute(text(tables_query)).fetchall()
        assert len(result) == 1
        assert result[0][0] == "test"

    count_query = provider.get_count_query("test")
    with provider.connect() as conn:
        count = conn.execute(text(count_query)).scalar()
        assert count == 2

def test_database_manager():
    config = {
        "db1": {"provider": "sqlite", "connection_string": "sqlite:///:memory:"},
        "db2": {"provider": "sqlite", "connection_string": "sqlite:///:memory:"}
    }
    
    manager = DatabaseManager(config)
    providers = manager.get_all_providers()
    
    assert len(providers) == 2
    assert "db1" in providers
    assert "db2" in providers
    assert manager.get_provider("db1").provider == "sqlite"

def test_unsupported_provider():
    with pytest.raises(ValueError):
        DatabaseProvider("unsupported_db", "...")
