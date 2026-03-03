# nblm-nix

A Nix-optimized Python CLI and Zsh wrapper for [NotebookLM](https://notebooklm.google.com/), built upon [notebooklm-py](https://github.com/teng-lin/notebooklm-py) (v0.3.2). This project ensures a seamless execution environment on NixOS and similar systems.

## Features

- **Sandbox Mode**: Creates a temporary notebook (`tmp_[timestamp]`) for immediate analysis. The notebook is automatically deleted upon exit to maintain environment hygiene.
- **FZF-Powered Interface**: Interactive selection for actions, notebooks, podcast formats (`deep-dive`, `brief`, `critique`, `debate`), and audio lengths.
- **Background Generation**: Audio/Podcast generation processes are offloaded to the background, allowing uninterrupted terminal usage.
- **Nix-Native Enhancements**:
    - **Playwright Integration**: Pre-configured `PLAYWRIGHT_BROWSERS_PATH` via `makeWrapper` for out-of-the-box browser functionality.
    - **Extended Timeouts**: Automatic `postPatch` during build to increase RPC and generation timeouts to 1800s, accommodating large source files.

## Technical Specifications

- **Version**: 0.3.2
- **Language**: Python 3
- **Dependencies**: `httpx`, `click`, `rich`, `playwright`, `fzf`, `gnugrep`, `coreutils`

## Installation

### 1. Build via Nix

```bash
 nix build .#default
```

### 2. Zsh Integration

Add the following function to your Zsh configuration to utilize the `nblm` wrapper:

```zsh
 function nblm() {
   # Executes the wrapped nblm-env
   nblm
 }
```

## Usage

Run the command in your terminal:

```bash
 nblm
```

1. **Select Action**: Choose from Sandbox (New), Existing Notebook, or Delete Notebook.
2. **Sandbox Flow**: Input URLs or file paths. Enter `a` to start the automated analysis/summary or `c` to abort and cleanup.
3. **Chat/Podcast**: Within a notebook session, use `src` to add sources, `p` to trigger background podcast generation, or `s` to save/rename the temporary notebook.

## Technical Improvements

- **Playwright Wrapping**: Utilizes Nix `makeWrapper` to ensure the Playwright driver correctly locates its hermetic browser binaries.
- **Source Patching**: Modifies the upstream source during the build phase to replace default 30/300s timeouts with 1800s via `sed`.
- **Non-Interactive Cleanup**: Uses the `-y` flag for `notebooklm delete` commands to ensure streamlined exit logic.

## License

MIT License - Copyright (c) 2026 yktsnet

## Acknowledgment

Special thanks to **@teng-lin** for the original [notebooklm-py](https://github.com/teng-lin/notebooklm-py) implementation.
