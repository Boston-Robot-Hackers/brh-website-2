# Prompt For Generating A Literate Program From Existing Python Code

Use the following prompt when you want an AI assistant to turn an existing Python program into the same kind of literate-program document we created here.

---

I want you to turn an existing Python program into a true literate-program style Markdown document.

The source file already exists in the workspace. Read the actual file first and base everything on the real code, not on guesses.

## Goal

Produce a Markdown file that explains the Python program in a detailed, interleaved style where commentary appears immediately before the code it explains.

I do not want a generic summary followed by a giant code dump. I want a real literate-program presentation.

## Required Output

Create a Markdown document that includes all of the following:

1. A short title and purpose section.
2. A Mermaid diagram of the program or pipeline.
3. A walkthrough section where explanation is interleaved with short code blocks.
4. A source line range label above every code block.
5. Clickable links to the real source file wherever relevant.

## Style Requirements

Follow this style very closely:

1. Break the explanation into small sections.
2. Before each code snippet, write a short paragraph explaining why the next few lines exist.
3. For non-obvious function calls, parameters, flags, and transformations, explain them in prose just before the line or small code block that uses them.
4. If a line is important, explain what would break or become confusing if it were removed or changed.
5. Prefer several small code blocks over a few large ones.
6. Keep the prose technical and practical, not academic or overly wordy.
7. Preserve the exact code from the file in the code blocks.
8. Include external links when helpful, especially for framework-specific behavior or non-obvious API semantics.
9. Use a vertical Mermaid layout if it fits better on the page.
10. Make the Markdown pleasant to read in VS Code preview.

## Interleaving Rules

This part is important.

Do not do this:

- Large prose section
- Large code block
- Large prose section
- Entire full source code

Instead do this:

- Brief explanation paragraph
- Small code block
- Brief explanation paragraph
- Small code block
- Brief explanation paragraph
- Small code block

I want the commentary to sit directly above the code it explains, even if that means the document is chopped into many small parts.

## Source Range Labels

Above every code block, add a line like this:

Source range: [path/to/file.py lines 120-134](absolute/path/to/file.py#L120-L134)

Requirements for source range labels:

1. Every code block gets one.
2. The range must match the real source lines.
3. The path must be clickable in the workspace.

## Mermaid Diagram Requirements

Create a Mermaid diagram that captures the program structure or processing pipeline.

Requirements:

1. Prefer `flowchart TD` unless horizontal layout is clearly better.
2. Keep labels simple enough to render in VS Code Mermaid preview.
3. Use quoted labels and `<br/>` line breaks if needed for compatibility.
4. Avoid syntax that commonly breaks VS Code Mermaid preview.

## What To Explain

When reading the Python file, look for these kinds of details and explain them right before the corresponding code:

1. Why a particular library call is needed.
2. Why a parameter has that specific value.
3. Data layout changes such as CHW to HWC, BGR vs RGB, FP16 vs uint8, normalized coordinates vs pixel coordinates.
4. Threading, callbacks, queues, polling, synchronization, or buffering behavior.
5. Host/device boundaries if hardware or accelerators are involved.
6. Why a specific API choice was made instead of another plausible option.
7. Which line acts as the actual filter, gate, threshold, or state transition.
8. Any part that is easy to misread when looking at raw code alone.

## Code Comments In The Source File

If appropriate, also improve the Python file itself with inline comments, but do so carefully.

Rules:

1. Add comments only where they genuinely help.
2. Prefer short, precise comments.
3. Do not rewrite the whole file with comment noise.
4. Preserve behavior.
5. Do not reformat unrelated code.

## Document Structure To Use

Use this rough structure:

1. Title
2. Purpose
3. Pipeline Diagram
4. Walkthrough
5. Full Source Code

Inside the Walkthrough section, organize the explanation by logical stages of the program rather than by raw function order when that improves comprehension.

## Important Constraints

1. Use the real file contents from the workspace.
2. Do not invent lines that are not present.
3. Do not paraphrase code inside code blocks.
4. Make line ranges accurate.
5. Make sure Mermaid syntax actually works in Markdown preview.
6. If a function call is subtle, explain it in a small paragraph before the snippet.
7. Include the entire source code in the final document, not just excerpts.

## Tone

Use the tone of a strong engineering code walkthrough:

1. Concrete
2. Technical
3. Clear
4. Slightly detailed
5. Focused on how the program actually works

## Deliverable

Create the Markdown file in the workspace and ensure it is readable as a standalone explanation of the program.

If the file already exists, update it rather than duplicating it.

---

Suggested one-line opener to use with the prompt above:

"Turn [path/to/program.py](path/to/program.py) into a literate-program Markdown walkthrough with interleaved commentary, accurate source line ranges above every code block, a Mermaid pipeline diagram."