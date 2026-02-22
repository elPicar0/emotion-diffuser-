"""
Tests for mediator_engine prompt/mode infrastructure.
Verifies that every relationship mode has proper configuration.
"""

import pytest
from mediator_engine.prompts import (
    TONE_RULES,
    MODE_GUIDANCE,
    REWRITE_EXAMPLES,
    APOLOGY_EXAMPLES,
    SUGGESTED_TRIGGERS,
    REWRITE_SYSTEM_PROMPT,
    APOLOGY_SYSTEM_PROMPT,
    GOTTMAN_RULES,
)
from mediator_engine.rewrite import (
    _get_tone_requirement,
    _get_mode_guidance,
    _get_rewrite_example,
    _get_apology_example,
)

ALL_MODES = ["parent", "sibling", "partner", "friend", "professional", "neutral"]


class TestToneRules:
    """Every mode must have a tone rule entry."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_tone_rule_exists(self, mode):
        assert mode in TONE_RULES
        assert isinstance(TONE_RULES[mode], str)
        assert len(TONE_RULES[mode]) > 5

    def test_unknown_mode_falls_back(self):
        assert _get_tone_requirement("alien") == TONE_RULES["neutral"]


class TestModeGuidance:
    """Every mode must have LLM guidance."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_guidance_exists(self, mode):
        assert mode in MODE_GUIDANCE
        assert len(MODE_GUIDANCE[mode]) > 20

    def test_partner_includes_gottman(self):
        assert "Gottman" in MODE_GUIDANCE["partner"]
        assert "CRITICISM" in MODE_GUIDANCE["partner"]

    def test_unknown_mode_falls_back(self):
        assert _get_mode_guidance("alien") == MODE_GUIDANCE["neutral"]


class TestRewriteExamples:
    """Every mode must have a bad→good rewrite example."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_example_exists(self, mode):
        ex = REWRITE_EXAMPLES[mode]
        assert "bad" in ex and "good" in ex
        assert len(ex["bad"]) > 5
        assert len(ex["good"]) > 5

    def test_unknown_mode_falls_back(self):
        ex = _get_rewrite_example("alien")
        assert ex == REWRITE_EXAMPLES["neutral"]


class TestApologyExamples:
    """Every mode must have a situation→apology example."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_example_exists(self, mode):
        ex = APOLOGY_EXAMPLES[mode]
        assert "situation" in ex and "apology" in ex

    def test_unknown_mode_falls_back(self):
        ex = _get_apology_example("alien")
        assert ex == APOLOGY_EXAMPLES["neutral"]


class TestSuggestedTriggers:
    """Every mode must have trigger strategies."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_triggers_exist(self, mode):
        assert mode in SUGGESTED_TRIGGERS
        triggers = SUGGESTED_TRIGGERS[mode]
        assert len(triggers) >= 2
        for t in triggers:
            assert "strategy" in t
            assert "suggestion" in t
            assert "psychology" in t


class TestPromptFormatting:
    """Prompts must format without errors for every mode."""

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_rewrite_prompt_formats(self, mode):
        ex = REWRITE_EXAMPLES[mode]
        result = REWRITE_SYSTEM_PROMPT.format(
            tone_requirement=TONE_RULES[mode],
            mode_guidance=MODE_GUIDANCE[mode],
            example_bad=ex["bad"],
            example_good=ex["good"],
        )
        assert TONE_RULES[mode] in result
        assert ex["bad"] in result

    @pytest.mark.parametrize("mode", ALL_MODES)
    def test_apology_prompt_formats(self, mode):
        ex = APOLOGY_EXAMPLES[mode]
        result = APOLOGY_SYSTEM_PROMPT.format(
            tone_requirement=TONE_RULES[mode],
            mode_guidance=MODE_GUIDANCE[mode],
            example_situation=ex["situation"],
            example_apology=ex["apology"],
        )
        assert TONE_RULES[mode] in result
        assert ex["situation"] in result
