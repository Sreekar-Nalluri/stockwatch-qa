"""
Page object loader for dynamically loading page helper classes.

This module provides utilities to load and manage page object classes
from the pages folder. Each page helper file should contain a class
with locators and action methods.

Usage:
    from src.pages_loader import PageLoader

    # Load a specific page class
    dashboard_page = PageLoader.get_page('dashboard_page.DashboardPage')

    # Load all page classes
    pages = PageLoader.load_all_pages()
"""

import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, List, Type


class PageLoader:
    """Loader for page object classes from the pages folder."""

    _pages_cache: Dict[str, Any] = {}
    _pages_dir = None

    @classmethod
    def _get_pages_dir(cls) -> Path:
        """Get the pages directory path."""
        if cls._pages_dir is None:
            # Pages folder is at src/pages
            cls._pages_dir = Path(__file__).parent / "pages"
            if not cls._pages_dir.exists():
                raise FileNotFoundError(f"Pages directory not found at: {cls._pages_dir}")
        return cls._pages_dir

    @classmethod
    def get_page(cls, page_path: str) -> Type:
        """
        Get a page class by module path.

        Args:
            page_path: Dot-separated path to the page class
                      (e.g., 'dashboard_page.DashboardPage', 'login.LoginPage')

        Returns:
            The page class

        Raises:
            ImportError: If the module cannot be imported
            AttributeError: If the class cannot be found in the module
        """
        # Check cache first
        if page_path in cls._pages_cache:
            return cls._pages_cache[page_path]

        try:
            # Split path into module and class name
            parts = page_path.rsplit('.', 1)
            if len(parts) != 2:
                raise ValueError(f"Invalid page path format: {page_path}. Use 'module.ClassName'")

            module_name, class_name = parts

            # Import the module from pages folder
            full_module_name = f"src.pages.{module_name}"
            module = importlib.import_module(full_module_name)

            # Get the class from the module
            page_class = getattr(module, class_name)

            # Cache it
            cls._pages_cache[page_path] = page_class

            print(f"✓ Loaded page class: {page_path}")
            return page_class

        except ImportError as e:
            raise ImportError(f"Cannot import page module: {module_name}. Error: {e}")
        except AttributeError as e:
            raise AttributeError(f"Cannot find class '{class_name}' in module '{module_name}'. Error: {e}")

    @classmethod
    def load_all_pages(cls) -> Dict[str, Type]:
        """
        Discover and load all page classes from the pages folder.

        Returns:
            Dictionary mapping page class names to their classes
        """
        pages_dict = {}
        pages_dir = cls._get_pages_dir()

        # Iterate through all Python files in pages folder
        for py_file in pages_dir.glob("**/*.py"):
            # Skip __init__.py and private files
            if py_file.name.startswith("_"):
                continue

            try:
                # Get relative module path
                relative_path = py_file.relative_to(pages_dir)
                module_name = str(relative_path).replace("\\", "/").replace("/", ".").replace(".py", "")

                # Import module
                full_module_name = f"src.pages.{module_name}"
                module = importlib.import_module(full_module_name)

                # Find all classes in the module that look like page objects
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Skip imported classes from other modules
                    if obj.__module__ == full_module_name and not name.startswith("_"):
                        pages_dict[name] = obj
                        print(f"✓ Discovered page class: {name}")

            except Exception as e:
                print(f"⚠ Error loading module {py_file}: {e}")
                continue

        return pages_dict

    @classmethod
    def clear_cache(cls):
        """Clear the pages cache."""
        cls._pages_cache.clear()
        print("✓ Pages cache cleared")


# Convenience functions for common usage patterns
def get_page(page_path: str) -> Type:
    """
    Convenience function to get a page class.

    Args:
        page_path: Dot-separated path to the page class

    Returns:
        The page class
    """
    return PageLoader.get_page(page_path)


def load_all_pages() -> Dict[str, Type]:
    """
    Convenience function to load all page classes.

    Returns:
        Dictionary of page classes
    """
    return PageLoader.load_all_pages()

