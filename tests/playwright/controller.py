"""Playwright controllers for shiny-treeview testing."""

from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import expect as playwright_expect
from shiny.playwright.controller._base import UiBase


class InputTreeView(UiBase):
    """Custom Playwright controller for the treeview input component."""

    def __init__(self, page: Page, id: str):
        super().__init__(
            page=page,
            id=id,
            loc=page.locator(f"#{id}.shiny-treeview").get_by_role("tree"),
        )
        self.loc_disabled = self.loc.get_by_role("treeitem", disabled=True)
        self.loc_expanded = self.loc.get_by_role("treeitem", expanded=True)
        self.loc_selected = self.loc.get_by_role("treeitem", selected=True)

    @property
    def tree_id(self) -> str | None:
        return self.loc.get_attribute("id")

    def item_locator(self, id: str) -> Locator:
        return self.loc.locator(f'[role="treeitem"][id$="-{id}"]')

    def expect_disabled(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ):
        """Expect the disabled item(s) of the treeview to be an exact match."""
        self._expect_match_id(id, self.loc_disabled, timeout=timeout)

    def expect_expanded(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ):
        """Expect the expanded item(s) of the treeview to be an exact match."""
        self._expect_match_id(id, self.loc_expanded, timeout=timeout)

    def expect_selected(
        self, id: str | list[str] | None, *, timeout: Optional[float] = None
    ):
        """Expect the selected item(s) of the treeview to be an exact match."""
        self._expect_match_id(id, self.loc_selected, timeout=timeout)

    def _expect_match_id(
        self,
        id: str | list[str] | None,
        loc: Locator,
        *,
        timeout: Optional[float] = None,
    ):
        if id is None:
            expected_ids = []
        elif isinstance(id, str):
            expected_ids = [id]
        elif isinstance(id, list):
            expected_ids = id

        playwright_expect(loc).to_have_count(len(expected_ids), timeout=timeout)

        observed_ids = [el.get_attribute("id") for el in loc.all()]
        observed_ids = [x.removeprefix(f"{self.tree_id}-") for x in observed_ids]

        assert set(observed_ids) == set(
            expected_ids
        ), f"Expected IDs {expected_ids}, but found {observed_ids}"

    def expect_multiple(self, multiple: bool, *, timeout: Optional[float] = None):
        """
        Expect the treeview to allow multiple selections.

        Parameters
        ----------
        multiple
            Whether the input allows multiple selections.
        timeout
            Maximum time to wait for the expectation to be fulfilled.
        """
        value = str(multiple).lower()
        self.expect.to_have_attribute("aria-multiselectable", value, timeout=timeout)

    def select_single(self, id: str, *, timeout: Optional[float] = None):
        """
        Select a single item in the treeview by its ID.

        Parameters
        ----------
        id
            The ID of the item to select.
        timeout
            Maximum time to wait for the action to complete.
        """
        item = self.item_locator(id)
        playwright_expect(item).to_have_count(1, timeout=timeout)
        item.click(timeout=timeout)

    def select_multiple(self, ids: list[str], *, timeout: Optional[float] = None):
        """
        Select multiple items in the treeview by their IDs.

        Parameters
        ----------
        ids
            The IDs of the items to select.
        timeout
            Maximum time to wait for the action to complete.
        """
        for index, id in enumerate(ids):
            modifiers = ["ControlOrMeta"] if index > 0 else None
            item = self.item_locator(id)
            playwright_expect(item).to_have_count(1, timeout=timeout)
            item.click(modifiers=modifiers, timeout=timeout)

    def select_range(
        self, id_start: str, id_end: str, *, timeout: Optional[float] = None
    ):
        """
        Select a range of items in the treeview from id_start to id_end.

        Parameters
        ----------
        id_start
            The ID of the starting item in the range.
        id_end
            The ID of the ending item in the range.
        timeout
            Maximum time to wait for the action to complete.
        """
        item_start = self.item_locator(id_start)
        item_end = self.item_locator(id_end)

        playwright_expect(item_start).to_have_count(1, timeout=timeout)
        playwright_expect(item_end).to_have_count(1, timeout=timeout)

        item_start.click(timeout=timeout)
        item_end.click(modifiers=["Shift"], timeout=timeout)
