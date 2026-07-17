"""
Unit tests for prepare_dataset.py

Run with:
    pytest test_prepare_dataset.py -v

Place this file in the same directory as prepare_dataset.py, or adjust the
import below to match your project layout.
"""
import pytest
from datasets import Dataset, DatasetDict

from data.prepare_dataset import (
    _normalize,
    dedup_raw,
    validate_labels,
    check_no_contamination,
)


# ---------------------------------------------------------------------------
# _normalize
# ---------------------------------------------------------------------------

class TestNormalize:
    def test_lowercases(self):
        assert _normalize("Refund Please") == _normalize("refund please")

    def test_collapses_whitespace(self):
        assert _normalize("refund   please") == _normalize("refund please")

    def test_strips_leading_trailing_whitespace(self):
        assert _normalize("  refund please  ") == "refund please"

    def test_strips_punctuation(self):
        assert _normalize("Refund please!") == _normalize("refund please")

    def test_strips_punctuation_mid_string(self):
        assert _normalize("I can't log in.") == _normalize("I cant log in")

    def test_empty_string_stays_empty(self):
        assert _normalize("") == ""

    def test_whitespace_only_becomes_empty(self):
        assert _normalize("   ") == ""

    def test_distinct_content_stays_distinct(self):
        # sanity check: normalize shouldn't collapse genuinely different tickets
        assert _normalize("Refund my last charge") != _normalize("Track my package")


# ---------------------------------------------------------------------------
# dedup_raw
# ---------------------------------------------------------------------------

class TestDedupRaw:
    def _make_raw(self, texts, labels=None):
        labels = labels or ["billing"] * len(texts)
        return Dataset.from_dict({"text": texts, "label": labels})

    def test_no_duplicates_keeps_all_rows(self):
        raw = self._make_raw(["Refund my charge", "Track my package", "Reset my password"])
        result = dedup_raw(raw)
        assert len(result) == 3

    def test_removes_exact_duplicate(self):
        raw = self._make_raw(["Refund my charge", "Refund my charge"])
        result = dedup_raw(raw)
        assert len(result) == 1

    def test_removes_near_duplicate_casing_and_punctuation(self):
        raw = self._make_raw(["Refund my charge!", "refund my charge"])
        result = dedup_raw(raw)
        assert len(result) == 1

    def test_removes_near_duplicate_whitespace(self):
        raw = self._make_raw(["Refund   my charge", "Refund my charge"])
        result = dedup_raw(raw)
        assert len(result) == 1

    def test_removes_empty_and_whitespace_only_rows(self):
        raw = self._make_raw(["Refund my charge", "", "   "])
        result = dedup_raw(raw)
        assert len(result) == 1
        assert result["text"] == ["Refund my charge"]

    def test_keeps_first_occurrence_on_duplicate(self):
        raw = self._make_raw(["Refund my charge", "REFUND MY CHARGE"])
        result = dedup_raw(raw)
        assert result["text"] == ["Refund my charge"]

    def test_preserves_other_columns_after_dedup(self):
        raw = self._make_raw(
            ["Refund my charge", "Refund my charge", "Track my package"],
            labels=["billing", "billing", "shipping"],
        )
        result = dedup_raw(raw)
        assert len(result) == 2
        assert result["label"] == ["billing", "shipping"]

    def test_all_duplicates_collapses_to_one(self):
        raw = self._make_raw(["Same ticket"] * 5)
        result = dedup_raw(raw)
        assert len(result) == 1

    def test_empty_dataset_returns_empty(self):
        raw = self._make_raw([])
        result = dedup_raw(raw)
        assert len(result) == 0


# ---------------------------------------------------------------------------
# validate_labels
# ---------------------------------------------------------------------------

class TestValidateLabels:
    def _make_dataset(self, train_labels, val_labels):
        train = Dataset.from_dict({"text": ["x"] * len(train_labels), "label": train_labels})
        val = Dataset.from_dict({"text": ["x"] * len(val_labels), "label": val_labels})
        return DatasetDict({"train": train, "validation": val})

    def test_passes_with_all_known_labels(self):
        ds = self._make_dataset(["billing", "technical"], ["account", "shipping"])
        # should not raise
        validate_labels(ds)

    def test_raises_on_unknown_label_in_train(self):
        ds = self._make_dataset(["billing", "not_a_real_label"], ["account"])
        with pytest.raises(ValueError, match="not_a_real_label"):
            validate_labels(ds)

    def test_raises_on_unknown_label_in_validation_only(self):
        ds = self._make_dataset(["billing"], ["mystery_category"])
        with pytest.raises(ValueError, match="mystery_category"):
            validate_labels(ds)

    def test_error_message_lists_all_unknown_labels(self):
        ds = self._make_dataset(["foo", "bar"], ["billing"])
        with pytest.raises(ValueError) as exc_info:
            validate_labels(ds)
        assert "foo" in str(exc_info.value)
        assert "bar" in str(exc_info.value)

    def test_passes_with_single_split_dict(self):
        ds = DatasetDict({"train": Dataset.from_dict({"text": ["x"], "label": ["general"]})})
        validate_labels(ds)


# ---------------------------------------------------------------------------
# check_no_contamination
# ---------------------------------------------------------------------------

class TestCheckNoContamination:
    def _make_dataset(self, train_texts, val_texts):
        train = Dataset.from_dict({"text": train_texts, "label": ["billing"] * len(train_texts)})
        val = Dataset.from_dict({"text": val_texts, "label": ["billing"] * len(val_texts)})
        return DatasetDict({"train": train, "validation": val})

    def test_passes_with_no_overlap(self):
        ds = self._make_dataset(
            train_texts=["Refund my charge", "Track my package"],
            val_texts=["Reset my password", "App keeps crashing"],
        )
        # should not raise
        check_no_contamination(ds)

    def test_raises_on_exact_overlap(self):
        ds = self._make_dataset(
            train_texts=["Refund my charge"],
            val_texts=["Refund my charge"],
        )
        with pytest.raises(ValueError, match="Contamination detected"):
            check_no_contamination(ds)

    def test_raises_on_near_duplicate_overlap_case_and_punctuation(self):
        # This is the scenario the contamination check exists to catch:
        # a near-duplicate that slipped past dedup due to casing/punctuation
        ds = self._make_dataset(
            train_texts=["Refund my charge!"],
            val_texts=["refund my charge"],
        )
        with pytest.raises(ValueError, match="Contamination detected"):
            check_no_contamination(ds)

    def test_raises_with_correct_overlap_count(self):
        ds = self._make_dataset(
            train_texts=["Refund my charge", "Track my package"],
            val_texts=["Refund my charge", "Reset my password"],
        )
        with pytest.raises(ValueError, match="1 examples"):
            check_no_contamination(ds)

    def test_passes_with_empty_splits(self):
        ds = self._make_dataset(train_texts=[], val_texts=[])
        check_no_contamination(ds)


# ---------------------------------------------------------------------------
# Integration: dedup_raw feeding into check_no_contamination should never fail
# ---------------------------------------------------------------------------

class TestDedupPreventsContamination:
    def test_dedup_then_split_then_check_passes(self):
        """End-to-end sanity check: the exact pattern used in main() —
        dedup before split, contamination check after — should never raise
        for data that dedup_raw has already cleaned."""
        texts = [
            "Refund my charge",
            "Refund my charge",       # exact dup
            "REFUND MY CHARGE!",      # near dup
            "Track my package",
            "Reset my password",
            "App keeps crashing",
        ]
        labels = ["billing", "billing", "billing", "shipping", "account", "technical"]
        raw = Dataset.from_dict({"text": texts, "label": labels})

        deduped = dedup_raw(raw)
        split = deduped.train_test_split(test_size=0.5, seed=42)
        ds = DatasetDict({"train": split["train"], "validation": split["test"]})

        validate_labels(ds)
        # should not raise
        check_no_contamination(ds)