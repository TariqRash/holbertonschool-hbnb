# ER Diagram Export Instructions

To export the ER diagram as an image (required for Task 10):

## Method 1: Using Mermaid Live Editor (Recommended)

1. Visit [Mermaid Live Editor](https://mermaid.live/)
2. Copy the entire Mermaid diagram code from `er_diagram.md`
3. Paste it into the editor
4. Click on the "Actions" dropdown menu
5. Select "PNG" or "SVG" to download the image
6. Save the image as `er_diagram.png` or `er_diagram.svg` in the `docs/` folder

## Method 2: Using VS Code Extension

1. Install the "Markdown Preview Mermaid Support" extension in VS Code
2. Open `er_diagram.md`
3. Click the preview button (or press Cmd+Shift+V on Mac, Ctrl+Shift+V on Windows)
4. Right-click on the diagram and select "Save Image As..."
5. Save as `er_diagram.png` in the `docs/` folder

## Method 3: Using Command Line (Node.js required)

```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Navigate to docs folder
cd part3/docs

# Export diagram
mmdc -i er_diagram.md -o er_diagram.png
```

## Expected Result

After export, you should have a file named `er_diagram.png` or `er_diagram.svg` in the `docs/` folder that visualizes the database relationships.
