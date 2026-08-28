from scripts.seed import load_transactions


def test_seed_preserves_all_rows_and_unique_ids():
    rows, balance = load_transactions()
    ids = [row["id"] for row in rows]
    assert len(rows) == 10_000
    assert len(set(ids)) == 10_000
    assert balance > 0
    assert any(identifier.endswith("-02") for identifier in ids)

