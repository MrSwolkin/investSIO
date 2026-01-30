"""
Tests for Category model.
"""
import pytest

from categories.models import Category


class TestCategoryModel:
    """Tests for Category model."""

    def test_create_category(self, db):
        """Test creating a category."""
        category = Category.objects.create(
            title="FII",
            description="Fundos Imobiliarios",
        )
        assert category.pk is not None
        assert category.title == "FII"
        assert category.description == "Fundos Imobiliarios"

    def test_category_str(self, db):
        """Test category string representation."""
        category = Category.objects.create(title="Acao")
        assert str(category) == "Acao"

    def test_category_without_description(self, db):
        """Test category can be created without description."""
        category = Category.objects.create(title="ETF")
        assert category.pk is not None
        assert category.description is None

    def test_category_ordering(self, db):
        """Test categories are ordered by title."""
        Category.objects.create(title="Stock")
        Category.objects.create(title="Acao")
        Category.objects.create(title="FII")
        categories = list(Category.objects.all())
        assert categories[0].title == "Acao"
        assert categories[1].title == "FII"
        assert categories[2].title == "Stock"
