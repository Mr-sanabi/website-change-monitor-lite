from src.storage import load_state, save_state

state = {
    "https://example.com": "abc123",
    "https://example.org": "def456",
}

def test_storage(tmp_path):
    state_path = tmp_path / "nested" / "state.json"
    save_state(state_path, state)
    assert state_path.exists()
    loaded = load_state(state_path)
    assert loaded == state
    temporary_path = state_path.with_suffix(state_path.suffix + ".tmp")
    assert not temporary_path.exists()