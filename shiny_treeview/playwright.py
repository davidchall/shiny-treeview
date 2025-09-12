"""Playwright controllers for shiny-treeview components."""

from functools import cached_property
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from playwright.sync_api import Locator, Page
    from shiny.playwright.controller._base import UiBase

try:
    from playwright.sync_api import Locator, Page
    from playwright.sync_api import expect as playwright_expect
    from shiny.playwright.controller._base import UiBase
except ImportError as e:
    raise ImportError(
        "Playwright testing utilities require playwright. "
        "Install with: pip install playwright"
    ) from e


LABEL_CLASS = "MuiTreeItem-label"
ICON_CLASS = "MuiTreeItem-iconContainer"


class InputTreeView(UiBase):
    """Custom Playwright controller for `input_treeview`.

    This controller provides methods to interact with and test shiny-treeview
    components in Playwright-based integration tests.

    Parameters
    ----------
    page : Page
        Playwright page of the Shiny app.
    id : str
        The ID of the treeview Shiny component.

    Examples
    --------
    ```python
    from shiny_treeview.playwright import InputTreeView

    def test_treeview(page, local_app):
        page.goto(local_app.url)

        treeview = InputTreeView(page, "my_treeview")
        treeview.select("item1")
        treeview.expect_selected("item1")

        # Works with multiple selection too
        treeview.select(["item1", "item2"])
        treeview.expect_selected(["item1", "item2"])

        # Expand tree nodes (if checkbox=False, this also selects the item)
        treeview.expand("folder1")
        treeview.expect_expanded("folder1")
    ```
    """

    def __init__(self, page: Page, id: str):
        super().__init__(
            page=page,
            id=id,
            loc=page.locator(f"#{id}.shiny-treeview").get_by_role("tree"),
        )
        self._loc_disabled = self.loc.get_by_role("treeitem", disabled=True)
        self._loc_expanded = self.loc.get_by_role("treeitem", expanded=True)
        self._loc_selected = self.loc.get_by_role("treeitem", selected=True)

    @property
    def _tree_id(self) -> str | None:
        """Get the ID attribute of the tree element."""
        return self.loc.get_attribute("id")

    @cached_property
    def _has_checkboxes(self) -> bool:
        """Check if the treeview has checkbox selection enabled.

        Cached property to avoid repeated DOM queries.

        Returns
        -------
        bool
            True if the treeview has checkboxes, False otherwise.
        """
        checkboxes = self.loc.locator('input[type="checkbox"]')
        try:
            checkboxes.first.wait_for(state="attached", timeout=1000)
            return True
        except:
            return False

    def item_locator(self, id: str) -> Locator:
        """Get a locator for a specific tree item by ID.

        Parameters
        ----------
        id : str
            The ID of the tree item.

        Returns
        -------
        Locator
            A Playwright locator for the tree item.
        """
        return self.loc.locator(f'[role="treeitem"][id$="-{id}"]')

    def expect_disabled(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ) -> None:
        """Expect the disabled item(s) of the treeview.

        Parameters
        ----------
        id : str, list[str], or None
            The expected IDs of the disabled items. None means zero items should be disabled.
        timeout : float, optional
            Maximum time to wait for the expectation to be fulfilled.
        """
        self._expect_match_id(id, self._loc_disabled, timeout=timeout)

    def expect_expanded(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ) -> None:
        """Expect the expanded item(s) of the treeview.

        Parameters
        ----------
        id : str, list[str], or None
            The expected IDs of the expanded items. None means zero items should be expanded.
        timeout : float, optional
            Maximum time to wait for the expectation to be fulfilled.
        """
        self._expect_match_id(id, self._loc_expanded, timeout=timeout)

    def expect_selected(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ) -> None:
        """Expect the selected item(s) of the treeview.

        Parameters
        ----------
        id : str, list[str], or None
            The expected IDs of the selected items. None means zero items should be selected.
        timeout : float, optional
            Maximum time to wait for the expectation to be fulfilled.
        """
        self._expect_match_id(id, self._loc_selected, timeout=timeout)

    def _expect_match_id(
        self,
        id: str | list[str] | None,
        loc: Locator,
        *,
        timeout: Optional[float] = None,
    ) -> None:
        """Internal method to match expected IDs against actual IDs."""
        if id is None:
            expected_ids = []
        elif isinstance(id, str):
            expected_ids = [id]
        elif isinstance(id, list):
            expected_ids = id

        playwright_expect(loc).to_have_count(len(expected_ids), timeout=timeout)

        observed_ids = [el.get_attribute("id") for el in loc.all()]
        observed_ids = [x.removeprefix(f"{self._tree_id}-") for x in observed_ids]

        assert set(observed_ids) == set(
            expected_ids
        ), f"Expected IDs {expected_ids}, but found {observed_ids}"

    def expect_multiple(self, value: bool, *, timeout: Optional[float] = None) -> None:
        """Expect the treeview to allow multiple selections.

        Parameters
        ----------
        value : bool
            Whether the input should allow multiple selections.
        timeout : float, optional
            Maximum time to wait for the expectation to be fulfilled.
        """
        value = str(value).lower()
        self.expect.to_have_attribute("aria-multiselectable", value, timeout=timeout)

    def expect_checkbox(self, value: bool, *, timeout: Optional[float] = None) -> None:
        """Expect the treeview to have checkbox selection enabled.

        Parameters
        ----------
        value : bool
            Whether the input should have checkbox selection enabled.
        timeout : float, optional
            Maximum time to wait for the expectation to be fulfilled.
        """
        checkboxes = self.loc.locator('input[type="checkbox"]')

        if value:
            playwright_expect(checkboxes.first).to_be_attached(timeout=timeout)
        else:
            playwright_expect(checkboxes).to_have_count(0, timeout=timeout)

    def _get_selectable_element(self, id: str) -> Locator:
        """Get the appropriate selectable element for a tree item (checkbox or label).

        Parameters
        ----------
        id : str
            The ID of the tree item.

        Returns
        -------
        Locator
            A locator for either the checkbox (if present) or the tree item itself.
        """
        item = self.item_locator(id)

        if self._has_checkboxes:
            return item.locator('input[type="checkbox"]:not(ul *)')
        else:
            return item.locator(f".{LABEL_CLASS}:not(ul *)")

    def select(
        self, selected: str | list[str], *, timeout: Optional[float] = None
    ) -> None:
        """Select item(s) in the treeview.

        Parameters
        ----------
        selected : str or list[str]
            The IDs of the items to select.
        timeout : float, optional
            Maximum time to wait for the action to complete.
        """
        if isinstance(selected, str):
            selected = [selected]

        for index, id in enumerate(selected):
            modifiers = ["ControlOrMeta"] if index > 0 else None
            selectable = self._get_selectable_element(id)
            playwright_expect(selectable).to_have_count(1, timeout=timeout)
            selectable.click(modifiers=modifiers, timeout=timeout)

    def select_range(
        self, id_start: str, id_end: str, *, timeout: Optional[float] = None
    ) -> None:
        """Select a range of items in the treeview.

        Parameters
        ----------
        id_start : str
            The ID of the starting item in the range.
        id_end : str
            The ID of the ending item in the range.
        timeout : float, optional
            Maximum time to wait for the action to complete.
        """
        selectable_start = self._get_selectable_element(id_start)
        selectable_end = self._get_selectable_element(id_end)

        playwright_expect(selectable_start).to_have_count(1, timeout=timeout)
        playwright_expect(selectable_end).to_have_count(1, timeout=timeout)

        selectable_start.click(timeout=timeout)
        selectable_end.click(modifiers=["Shift"], timeout=timeout)

    def expand(
        self, items: str | list[str], *, timeout: Optional[float] = None
    ) -> None:
        """Expand or collapse tree item(s) by clicking on their expand icons.

        Parameters
        ----------
        items : str or list[str]
            The IDs of the items to expand.
        timeout : float, optional
            Maximum time to wait for the action to complete.
        """
        if isinstance(items, str):
            items = [items]

        for item_id in items:
            item = self.item_locator(item_id)
            playwright_expect(item).to_have_count(1, timeout=timeout)

            # Find the expand icon for this tree item (not its children)
            expand_icon = item.locator(f".{ICON_CLASS}:not(ul *)").first
            expand_icon.click(timeout=timeout)
