import React from "react";
import { createRoot } from "react-dom/client";
import { makeInputBinding } from "@posit-dev/shiny-bindings-core";
import { ShinyTreeView, TreeItem } from "./treeview";

makeInputBinding({
  name: "shiny-treeview",
  setup: (el: HTMLElement, updateValue: (value: unknown) => void) => {
    // Find the configuration script element
    const configScript = el.querySelector(`script[data-for="${el.id}"]`);

    if (!configScript) {
      console.error(`No configuration script found for treeview ${el.id}`);
      return;
    }

    // Helper function to safely parse and validate arrays of strings
    const parseStringArray = (value: unknown, fallback: string[] = []): string[] => {
      if (Array.isArray(value)) {
        return value.filter(item => typeof item === 'string');
      }
      return fallback;
    };

    // Helper function to validate TreeItem structure
    const validateTreeItems = (items: unknown): TreeItem[] => {
      if (!Array.isArray(items)) {
        return [];
      }

      const validateItem = (item: any): TreeItem | null => {
        if (!item || typeof item !== 'object') return null;
        if (typeof item.id !== 'string' || typeof item.label !== 'string') return null;

        const validatedItem: TreeItem = {
          id: item.id,
          label: item.label,
        };

        if (typeof item.disabled === 'boolean') {
          validatedItem.disabled = item.disabled;
        }

        if (Array.isArray(item.children)) {
          const validChildren = item.children
            .map(validateItem)
            .filter((child: TreeItem | null): child is TreeItem => child !== null);
          if (validChildren.length > 0) {
            validatedItem.children = validChildren;
          }
        }

        return validatedItem;
      };

      return items
        .map(validateItem)
        .filter((item: TreeItem | null): item is TreeItem => item !== null);
    };

    let config: {
      items: TreeItem[];
      multiple: boolean;
      selected: string[];
      expanded: string[];
    };

    try {
      const rawConfig = JSON.parse(configScript.textContent || '{}');

      // Safely extract and validate each property
      config = {
        items: validateTreeItems(rawConfig?.items ?? []),
        multiple: Boolean(rawConfig?.multiple),
        selected: parseStringArray(rawConfig?.selected ?? []),
        expanded: parseStringArray(rawConfig?.expanded ?? []),
      };

      // Log warning if items array is empty after validation
      if (Array.isArray(rawConfig?.items) && rawConfig.items.length > 0 && config.items.length === 0) {
        console.warn('All tree items failed validation - check item structure (id and label are required)');
      }
    } catch (e) {
      console.error('Failed to parse treeview configuration:', e);
      // Provide fallback configuration instead of complete failure
      config = {
        items: [],
        multiple: false,
        selected: [],
        expanded: [],
      };
    }

    const { items, multiple, selected, expanded } = config;

    // Create React root and render component
    createRoot(el).render(React.createElement(ShinyTreeView, {
      items,
      multiple,
      selected,
      expanded,
      updateShinyValue: updateValue
    }));
  }
});
