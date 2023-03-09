[Project homepage](https://peter88213.github.io/novelyst_templates)

--- 

A [novelyst](https://peter88213.github.io/novelyst/) plugin for managing Markdown "Story Templates". 

---

# Installation

If [novelyst](https://peter88213.github.io/novelyst/) is installed, the setup script auto-installs the *novelyst_templates* plugin in the *novelyst* plugin directory.

The plugin adds a **Story Templates** entry to the *novelyst* **Tools** menu, and a **Template plugin Online Help** entry to the **Help** menu. 

---

# Command reference

You can open the submenu with **Tools > Story Templates**.

---

## Load

This loads the narrative structure from a Marktown template file. 

---

## Save

This saves the narrative structure to a Marktown template file. 

---

# Conventions

In *novelyst*, you can define a narrative structure with "Todo" Parts, Chapters, and scenes. See [Arcs](https://peter88213.github.io/novelyst/help/arcs). *novelyst_templates* faciliates the reuse of narrative structures.

## Markdown file structure

The *Story Template* Markdown file defines such a structure with headings and ordinary text.

---

### First level heading

The first level heading begins with `#`, followed by a blank and a title. 

Two titles are allowed:
- `nv` for the "Todo" chapters in the *Narrative* tree, signifying e.g. acts.
- `pl` for the "Todo" parts, chapters, and scenes in the *Planning* tree, signifying story arcs and arc points.

---

### Second level heading

The second level heading begins with `##`, followed by a blank and a part title. 

- One second level heading is required for creating the "Arcs" part in the *Planning* tree.

---

### Third level heading

The third level heading begins with `###`, followed by a blank and a chapter title. 

- In the *Narrative* tree, a chapter signifying a story phase such as an act is created. 
- In the *Planning* tree, a chapter signifying an arc is created. The arc name will be the first character of the chapter title.

---

### Fourth level heading

The fourth level heading begins with one `####`, followed by a blank and a scene title. 

- Under a chapter in the *Planning* tree, a scene signifying an arc point is created.

---

### Ordinary text

Any text under a heading is used as a description for the element generated from the heading.

---

### Example

```
# nv

### ACT 1

### ACT 2

### ACT 3

# pl

## Arcs

### A - Storyline

Applying a beat sheet as described in "Save The Cat!
Writes A Novel" by Jessica Brody.

#### Opening Image

A "so far" snapshot of your hero and his world.

#### Theme Stated

A statement from a character (usually not the hero) that
gives a hint of what the hero's story arc is about (that is,
what the hero must learn/discover before the end of the book). 

#### Setup

#### Catalyst

An igniting incident (or life-changing event) that catapults
the hero into a new world, or causes him to rethink. A blow
that should be strong enough to prevent the hero's return to
the setup's status quo.

#### Debate

The reaction, a sequence in which the hero debates what to do
next. It is usually presented as a question (like "should I go?").
The purpose is to show hesitation to change.

#### Break into 2

#### B Story

#### Fun and Games

#### Midpoint

#### Bad Guys close in

#### All is lost

#### Dark night of the soul

#### Break into 3

#### Finale

#### Final Image

```

This file generates the following structure:

![Screenshot](Screenshots/structure01.png)

---

# License

This is Open Source software, and the *novelyst_templates* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_templates/blob/main/LICENSE) file.
