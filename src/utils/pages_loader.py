import importlib
import inspect
from pathlib import Path
from typing import Any, Dict, Type


class PageLoader:
    """
    Dynamic loader that instantiates all page objects and makes them available
    as attributes based on their module names.

    Example:
        pages = PageLoader(page)
        await pages.example.get_title()             # ExamplePage instance
    """

    _class_cache: Dict[str, Type] = {}

    def __init__(self, page: Any):
        """
        Initialize PageLoader and autoload all page objects.

        Args:
            page: Playwright async page object
        """
        self.page = page
        self._page_instances: Dict[str, Any] = {}

        # Autoload all page classes
        self._load_pages()

    @staticmethod
    def _get_pages_dir() -> Path:
        """Get the pages directory path."""
        pages_dir = Path(__file__).parent.parent / "pages"
        if not pages_dir.exists():
            raise FileNotFoundError(f"Pages directory not found at: {pages_dir}")
        return pages_dir

    @classmethod
    def _load_page_classes(cls) -> Dict[str, Type]:
        """
        Discover and load all page classes from the pages folder.

        Returns:
            Dictionary mapping page names to their classes
        """
        if cls._class_cache:
            return cls._class_cache

        pages_dict = {}
        pages_dir = cls._get_pages_dir()

        # Iterate through all Python files in pages folder
        for py_file in pages_dir.glob("*.py"):
            # Skip __init__.py and private files
            if py_file.name.startswith("_"):
                continue

            # Only load *_page.py files
            if not py_file.name.endswith("_page.py"):
                continue

            try:
                # Get module name (e.g., "dashboard_page" from "dashboard_page.py")
                module_name = py_file.stem

                # Import module
                full_module_name = f"src.pages.{module_name}"
                module = importlib.import_module(full_module_name)

                # Find all classes in the module that are page objects
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    # Skip imported classes from other modules
                    if obj.__module__ == full_module_name and not name.startswith("_"):
                        pages_dict[name] = obj
                        print(f"[OK] Loaded page class: {name}")

            except Exception as e:
                print(f"[WARN] Error loading {py_file.name}: {e}")
                continue

        cls._class_cache = pages_dict
        return pages_dict

    def _load_pages(self):
        """Load all page classes and create instances as attributes."""
        page_classes = self._load_page_classes()

        for class_name, page_class in page_classes.items():
            # Convert class name to snake_case attribute name
            # e.g., "DashboardPage" -> "dashboard"
            attr_name = self._class_name_to_attr(class_name)

            # Create instance and attach as attribute
            try:
                instance = page_class(self.page)
                setattr(self, attr_name, instance)
                print(f"[OK] Initialized page: {attr_name} ({class_name})")
            except Exception as e:
                print(f"[WARN] Failed to initialize {class_name}: {e}")

    @staticmethod
    def _class_name_to_attr(class_name: str) -> str:
        """
        Convert class name to snake_case attribute name.

        Examples:
            "DashboardPage" -> "dashboard"
            "ExamplePage" -> "example"
            "LoginFormPage" -> "login_form"

        Args:
            class_name: The class name

        Returns:
            Snake case attribute name (without "_page" suffix)
        """
        # Remove "Page" suffix if present
        if class_name.endswith("Page"):
            class_name = class_name[:-4]

        # Convert CamelCase to snake_case
        result = []
        for i, char in enumerate(class_name):
            if char.isupper() and i > 0:
                result.append("_")
            result.append(char.lower())

        return "".join(result)

    def __getattr__(self, name: str):
        """
        Provide access to page instances as attributes.

        Args:
            name: Attribute name

        Returns:
            The page instance

        Raises:
            AttributeError: If the page doesn't exist
        """
        if name.startswith("_"):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        # Check if we have this page instance
        for page_name, page_instance in self.__dict__.items():
            if not page_name.startswith("_") and page_name != "page":
                if page_name == name:
                    return page_instance

        raise AttributeError(f"Page '{name}' not found. Available pages: {self._get_available_pages()}")

    def _get_available_pages(self) -> list:
        """Get list of available page names."""
        return [name for name in self.__dict__.keys() if not name.startswith("_") and name != "page"]

    @classmethod
    def clear_cache(cls):
        """Clear the pages cache."""
        cls._class_cache.clear()
        print("[OK] Pages cache cleared")
