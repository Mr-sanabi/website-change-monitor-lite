from src import main as main_module
from src.storage import load_state, save_state
from types import SimpleNamespace


def test_fetch_error_does_not_overwrite_existing_state(tmp_path, monkeypatch):
    url = "https://example.com"
    input_path = tmp_path / "urls.txt"
    input_path.write_text(url + "\n", encoding="utf-8")
    state_path = tmp_path / "nested" / "state.json"
    output_path = tmp_path / "nested" / "report.csv"
    save_state(state_path, {url: "old-good-hash"})
    fake_result = {
        "url": url,
        "status_code": None,
        "html": None,
        "error": "Connection failed",
        "error_type": "request_error"
    }
    def fake_fetch_page(url):
        return fake_result
    monkeypatch.setattr(main_module, "fetch_page", fake_fetch_page)
    fake_args = SimpleNamespace(
        input_file=str(input_path),
        output_file=str(output_path),
        state_file=str(state_path),
    )
    def fake_parse_args():
        return fake_args
    monkeypatch.setattr(main_module, "parse_args", fake_parse_args)
    main_module.main()
    saved_state = load_state(state_path)
    assert saved_state[url] == "old-good-hash"
    rows = output_path.read_text(encoding="utf-8")
    assert "request_error" in rows
