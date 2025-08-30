import React from "react";
import { RichTreeView } from "@mui/x-tree-view/RichTreeView";
import { TreeViewBaseItem } from "@mui/x-tree-view/models";

// Define the tree item type that extends MUI's base type
export interface TreeItem extends TreeViewBaseItem {
  id: string;
  label: string;
  children?: TreeItem[];
  disabled?: boolean;
}

// React component for MUI RichTreeView
export function ShinyTreeView({
  items,
  multiple,
  selected,
  expanded,
  updateShinyValue
}: {
  items: TreeItem[];
  multiple: boolean;
  selected: string[];
  expanded: string[];
  updateShinyValue: (value: string[] | string | null) => void;
}) {
  const [selectedItems, setSelectedItems] = React.useState<string[]>(selected);
  const [currentExpandedItems, setCurrentExpandedItems] = React.useState<string[]>(expanded);

  // Notify Shiny of the initial value on mount
  React.useEffect(() => {
    if (multiple) {
      // Multiple selection: return array or null if empty
      const multiValue = selected.length > 0 ? selected : null;
      updateShinyValue(multiValue);
    } else {
      // Single selection: return single string or null
      const singleValue = selected.length > 0 ? selected[0] : null;
      updateShinyValue(singleValue);
    }
  }, []); // Empty dependency array means this runs once on mount

  return React.createElement(RichTreeView, {
    items: items,
    selectedItems: selectedItems,
    expandedItems: currentExpandedItems,
    onExpandedItemsChange: (_event: any, itemIds: string[]) => {
      setCurrentExpandedItems(itemIds);
    },
    onSelectedItemsChange: (_event: any, itemIds: string | string[] | null) => {
      const normalizedIds = Array.isArray(itemIds) ? itemIds : itemIds ? [itemIds] : [];
      normalizedIds.sort();
      setSelectedItems(normalizedIds);

      // Return appropriate type based on multiple setting
      if (multiple) {
        // Multiple selection: return array (becomes tuple in Python) or null if empty
        const multiValue = normalizedIds.length > 0 ? normalizedIds : null;
        updateShinyValue(multiValue);
      } else {
        // Single selection: return single string or null
        const singleValue = normalizedIds.length > 0 ? normalizedIds[0] : null;
        updateShinyValue(singleValue);
      }
    },
    multiSelect: multiple,
    isItemDisabled: (item: any) => {
      return item.disabled === true;
    },
    sx: {
      height: "fit-content",
      width: "100%",
      border: "1px solid #e0e0e0",
      borderRadius: "4px",
      padding: "8px",
      fontFamily: "Roboto, Helvetica, Arial, sans-serif",
      backgroundColor: "white"
    }
  });
}
