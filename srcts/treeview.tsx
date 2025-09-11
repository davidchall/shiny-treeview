import React from "react";
import { RichTreeView } from "@mui/x-tree-view/RichTreeView";
import { TreeItem, TreeItemProps } from "@mui/x-tree-view/TreeItem";
import { TreeViewBaseItem } from "@mui/x-tree-view/models";
import { useTreeItemModel } from "@mui/x-tree-view/hooks";
import { Typography } from "@mui/material";

// Define the tree item type that extends MUI's base type
export interface ShinyTreeItem extends TreeViewBaseItem {
  id: string;
  label: string;
  caption?: string;
  children?: ShinyTreeItem[];
  disabled?: boolean;
}

// Custom label component for items with captions
interface CustomLabelProps {
  children: string;
  className: string;
  caption: string;
}

function CustomLabel({ children, className, caption }: CustomLabelProps) {
  return (
    <div className={className}>
      <Typography>{children}</Typography>
      {caption && (
        <Typography variant="caption" color="text.secondary">
          {caption}
        </Typography>
      )}
    </div>
  );
}

// Custom TreeItem component that supports captions
const CustomTreeItem = React.forwardRef(function CustomTreeItem(
  props: TreeItemProps,
  ref: React.Ref<HTMLLIElement>,
) {
  const item = useTreeItemModel<ShinyTreeItem>(props.itemId)!;

  return (
    <TreeItem
      {...props}
      ref={ref}
      slots={{
        label: CustomLabel,
      }}
      slotProps={{
        label: { caption: item?.caption || '' } as CustomLabelProps,
      }}
    />
  );
});

// React component for MUI RichTreeView
export function ShinyTreeView({
  items,
  selected,
  expanded,
  multiple,
  checkbox,
  updateShinyValue
}: {
  items: ShinyTreeItem[];
  selected: string[];
  expanded: string[];
  multiple: boolean;
  checkbox: boolean;
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

  return (
    <RichTreeView
      items={items}
      selectedItems={selectedItems}
      expandedItems={currentExpandedItems}
      multiSelect={multiple}
      checkboxSelection={checkbox}
      slots={{
        item: CustomTreeItem,
      }}
      onExpandedItemsChange={(_event: any, itemIds: string[]) => {
        setCurrentExpandedItems(itemIds);
      }}
      onSelectedItemsChange={(_event: any, itemIds: string | string[] | null) => {
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
      }}
      isItemDisabled={(item: any) => {
        return item.disabled === true;
      }}
      sx={{
        height: "fit-content",
        width: "100%",
        border: "1px solid #e0e0e0",
        borderRadius: "4px",
        padding: "8px",
        fontFamily: "Roboto, Helvetica, Arial, sans-serif",
        backgroundColor: "white"
      }}
    />
  );
}
