from chimera.library.parser import NumberedListOutputParser


class TestNumberedListOutputParser:
    """Test cases for NumberedListOutputParser."""

    def test_parser_initialization(self):
        """Test that parser can be initialized."""
        parser = NumberedListOutputParser()
        assert parser is not None

    def test_parser_type_property(self):
        """Test that parser has correct type property."""
        parser = NumberedListOutputParser()
        assert parser._type == "numbered_list"

    def test_parse_simple_numbered_list(self):
        """Test parsing a simple numbered list."""
        parser = NumberedListOutputParser()
        text = "1. First item\n2. Second item\n3. Third item"

        result = parser.parse(text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_numbered_list_with_parenthesis(self):
        """Test parsing a numbered list with parenthesis format."""
        parser = NumberedListOutputParser()
        text = "1) First item\n2) Second item\n3) Third item"

        result = parser.parse(text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_mixed_formats(self):
        """Test parsing a list with mixed formats."""
        parser = NumberedListOutputParser()
        text = "1. First item\n2) Second item\n3. Third item"

        result = parser.parse(text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_empty_string(self):
        """Test parsing an empty string."""
        parser = NumberedListOutputParser()
        text = ""

        result = parser.parse(text)

        assert result == []

    def test_parse_whitespace_only(self):
        """Test parsing whitespace only string."""
        parser = NumberedListOutputParser()
        text = "   \n   \n   "

        result = parser.parse(text)

        assert result == []

    def test_parse_list_with_extra_whitespace(self):
        """Test parsing a list with extra whitespace."""
        parser = NumberedListOutputParser()
        text = "  1.   First item  \n  2.   Second item  "

        result = parser.parse(text)

        assert result == ["First item", "Second item"]

    def test_parse_single_item(self):
        """Test parsing a single item list."""
        parser = NumberedListOutputParser()
        text = "1. Only item"

        result = parser.parse(text)

        assert result == ["Only item"]

    def test_parse_list_with_empty_lines(self):
        """Test parsing a list with empty lines."""
        parser = NumberedListOutputParser()
        text = "1. First item\n\n2. Second item\n\n3. Third item"

        result = parser.parse(text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_list_with_large_numbers(self):
        """Test parsing a list with large numbers."""
        parser = NumberedListOutputParser()
        text = "10. Tenth item\n11. Eleventh item\n100. Hundredth item"

        result = parser.parse(text)

        assert result == ["Tenth item", "Eleventh item", "Hundredth item"]

    def test_parse_list_with_special_characters(self):
        """Test parsing a list with special characters in items."""
        parser = NumberedListOutputParser()
        text = "1. Item with @#$%\n2. Item with spaces  and  tabs\n3. Item with: colons"

        result = parser.parse(text)

        assert "Item with @#$%" in result
        assert "Item with spaces  and  tabs" in result
        assert "Item with: colons" in result

    def test_parse_list_without_numbers(self):
        """Test parsing text without numbered items."""
        parser = NumberedListOutputParser()
        text = "This is just regular text\nWithout any numbering"

        result = parser.parse(text)

        # Text without numbers should still be captured (just stripped)
        assert "This is just regular text" in result
        assert "Without any numbering" in result

    def test_parse_list_with_inconsistent_spacing(self):
        """Test parsing a list with inconsistent spacing."""
        parser = NumberedListOutputParser()
        text = "1.First item\n2.  Second item\n  3.  Third item"

        result = parser.parse(text)

        assert result == ["First item", "Second item", "Third item"]

    def test_parse_inherits_from_base_output_parser(self):
        """Test that NumberedListOutputParser inherits from BaseOutputParser."""
        from langchain_core.output_parsers import BaseOutputParser

        parser = NumberedListOutputParser()
        assert isinstance(parser, BaseOutputParser)
