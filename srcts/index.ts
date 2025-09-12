import React from "react";
import { createRoot, Root } from "react-dom/client";
import { ShinyTreeView, ShinyTreeItem } from "./treeview";

if (window.Shiny) {
  class ShinyTreeViewBinding extends window.Shiny.InputBinding {
    private boundElementValues = new WeakMap<HTMLElement, any>();
    private boundElementRoots = new WeakMap<HTMLElement, Root>();

    override find(scope: HTMLElement) {
      return $(scope).find('.shiny-treeview');
    }

    override getValue(el: HTMLElement) {
      if (this.boundElementValues.has(el)) {
        return this.boundElementValues.get(el);
      }
      return null;
    }

    override subscribe(el: HTMLElement, callback: (value: boolean) => void): void {
      if (this.boundElementRoots.has(el)) {
        return;
      }

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

      // Helper function to validate ShinyTreeItem structure
      const validateTreeItems = (items: unknown): ShinyTreeItem[] => {
        if (!Array.isArray(items)) {
          return [];
        }

        const validateItem = (item: any): ShinyTreeItem | null => {
          if (!item || typeof item !== 'object') return null;
          if (typeof item.id !== 'string' || typeof item.label !== 'string') return null;

          const validatedItem: ShinyTreeItem = {
            id: item.id,
            label: item.label,
          };

          if (typeof item.disabled === 'boolean') {
            validatedItem.disabled = item.disabled;
          }

          if (typeof item.caption === 'string') {
            validatedItem.caption = item.caption;
          }

          if (Array.isArray(item.children)) {
            const validChildren = item.children
              .map(validateItem)
              .filter((child: ShinyTreeItem | null): child is ShinyTreeItem => child !== null);
            if (validChildren.length > 0) {
              validatedItem.children = validChildren;
            }
          }

          return validatedItem;
        };

        return items
          .map(validateItem)
          .filter((item: ShinyTreeItem | null): item is ShinyTreeItem => item !== null);
      };

      let config: {
        items: ShinyTreeItem[];
        selected: string[];
        expanded: string[];
        multiple: boolean;
        checkbox: boolean;
      };

      try {
        const rawConfig = JSON.parse(configScript.textContent || '{}');

        // Safely extract and validate each property
        config = {
          items: validateTreeItems(rawConfig?.items ?? []),
          selected: parseStringArray(rawConfig?.selected ?? []),
          expanded: parseStringArray(rawConfig?.expanded ?? []),
          multiple: Boolean(rawConfig?.multiple),
          checkbox: Boolean(rawConfig?.checkbox),
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
          selected: [],
          expanded: [],
          multiple: false,
          checkbox: false,
        };
      }

      const { items, selected, expanded, multiple, checkbox } = config;

      // Function to update the Shiny value
      const updateValue = (value: unknown, allowDeferred?: boolean) => {
        this.boundElementValues.set(el, value);
        callback(allowDeferred || false);
      };

      // Create React root and render component
      const root = createRoot(el);
      this.boundElementRoots.set(el, root);

      root.render(React.createElement(ShinyTreeView, {
        items,
        selected,
        expanded,
        multiple,
        checkbox,
        updateShinyValue: updateValue
      }));
    }

    override unsubscribe(el: HTMLElement): void {
      // Clean up React root to prevent memory leaks
      const root = this.boundElementRoots.get(el);
      if (root) {
        root.unmount();
        this.boundElementRoots.delete(el);
      }

      // Clean up value storage
      this.boundElementValues.delete(el);
    }
  }

  window.Shiny.inputBindings.register(new ShinyTreeViewBinding(), 'shiny-treeview-binding');
}
