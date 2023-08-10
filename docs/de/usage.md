[Projekt-Homepage](https://peter88213.github.io/novelyst_templates) > Gebrauchsanleitung

--- 

Ein [novelyst](https://peter88213.github.io/novelyst/)-Plugin for managing Markdown "Erzählstruktur-Vorlagen". 

---

# Installation

Wenn [novelyst](https://peter88213.github.io/novelyst/) installiert ist, installiert das Setup-Skript automatisch das*novelyst_templates*-Plugin im *novelyst* Plugin-Verzeichnis.

Das Plugin hängt einen **Erzählstruktur-Vorlagen**-Eintrag an das *novelyst* **Extras**-Menü, und einen **Template plugin Online Hilfe**-Eintrag an das **Hilfe**-Menü an. 

---

# Command reference

You can open the submenu with **Extras > Erzählstruktur-Vorlagen**.

---

## Laden

This loads the narrative structure from a Markdown template file. 

---

## Speichern

This saves the narrative structure to a Markdown template file. 

---

## Ordner öffnen

This opens the templates folder with the OS file manager, so you can manage and edit the templates. 

---

# Conventions

In *novelyst*, you can define a narrative structure with "Planung" Teils, Kapitels, and scenes. See [Bögen](https://peter88213.github.io/novelyst/help/arcs). *novelyst_templates* faciliates the reuse of narrative structures.

## Markdown file structure

The *Erzählstruktur-Vorlage* Markdown file defines such a structure with headings and ordinary text.

---

### First level heading

The first level heading begins with `#`, followed by a space and a title. 

Two titles are allowed:
- `nv` for the "Planung" chapters in the *Narrative* tree, signifying e.g. acts.
- `pl` for the "Planung" parts, chapters, and scenes in the *Planung* tree, signifying story arcs and arc points.

---

### Second level heading

The second level heading begins with `##`, followed by a space and a part title. 

- One second level heading is required for creating the "Bögen" part in the *Planung* tree.

---

### Third level heading

The third level heading begins with `###`, followed by a space and a chapter title. 

- In the *Narrative* tree, a chapter signifying a story phase such as an act is created. 
- In the *Planung* tree, a chapter is created. If the heading contains a hyphen (`-`), the chapter defines an arc. Then the arc name will be the part of the chapter title that comes before the hyphen.

---

### Fourth level heading

The fourth level heading begins with `####`, followed by a space and a scene title. 

- Under a chapter in the *Planung* tree, a scene signifying an arc point is created.

---

### Ordinary text

Any text under a heading is used as a description for the element generated from the heading.

---

### Example

```
# nv

### ACT 1

Setup

### ACT 2

Confrontation

### ACT 3

Resolution

# pl

## Bögen

### A-Storyline

Anwendening a three-act structure.

#### Inciting Incident

#### Plot Point 1

#### Midpoint

#### Plot Point 2

#### Climax

```

This file generates the following structure:

![Screenshot](Screenshots/structure01.png)

---

# Lizenz

Dies ist quelloffene Software, und das *novelyst_templates*-Plugin steht unter der GPLv3-Lizenz. Für mehr Details besuchen Sie die[Website der GNU General Public License](https://www.gnu.org/licenses/gpl-3.0.de.html), oder schauen Sie sich die [LICENSE](https://github.com/peter88213/novelyst_templates/blob/main/LICENSE)-Datei an.
