# novelyst_templates

The [novelyst](https://peter88213.github.io/novelyst/) Python program helps authors organize novels.

*novelyst_templates* is a plugin for managing Markdown "Story Templates".

![Screenshot](Screenshots/screen01.png)

## Features

In *novelyst*, you can define a story structure with "Todo" scenes. *novelyst_templates* faciliates the reuse of story structures.

- Load the story structure model from a Markdown template file. Each stage is converted into a "Todo" scene with a "stage" tag:
    - When loading a template into an empty project, a whole story framework is created.
    - When loading a template into a project that has already chapters, a list of stages is created in a "Todo" chapter.
- Save the story structure to a Markdown template file. 


## Requirements

- [novelyst](https://peter88213.github.io/novelyst/) version 4.45+

## Download and install

[Download the latest release (version 0.99.0)](https://github.com/peter88213/novelyst_templates/raw/main/dist/novelyst_templates_v0.99.0.zip)

- Extract the "novelyst_templates_v0.99.0" folder from the downloaded zipfile "novelyst_templates_v0.99.0.zip".
- Move into this new folder and launch **setup.pyw**. This installs the plugin for the local user.

---

[Changelog](changelog)

## Usage

See the [instructions for use](usage)

## License

This is Open Source software, and the *novelyst_templates* plugin is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst_templates/blob/main/LICENSE) file.
