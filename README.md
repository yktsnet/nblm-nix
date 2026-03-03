# nblm-nix

A Nix-integrated Python CLI and Zsh wrapper for [NotebookLM](https://notebooklm.google.com/), built upon [notebooklm-py](https://github.com/teng-lin/notebooklm-py).

## Features

- **Sandbox Mode**: Quickly create a temporary notebook for analysis. The notebook is automatically deleted upon exit to keep your environment clean.
- **FZF-Powered Interface**: Interactive selection for notebooks, podcast formats (`deep-dive`, `critique`, etc.), and audio lengths.
- **Background Generation**: Audio generation runs in the background, allowing you to continue working in your terminal.
- **Nix-Optimized**: 
    - Pre-configured Playwright environment.
    - Extended timeouts (up to 1800s) via Nix `postPatch` to handle large source files reliably.

## Installation & Setup

### 1. Nix Package
This repository provides a `default.nix` which defines the `notebooklm` package with all necessary Python dependencies and Playwright browser paths.

### 2. Zsh Integration
To use the `nblm` command as a Zsh function, add the following to your Zsh configuration (e.g., `home-manager` or `.zshrc`):

```zsh
function nblm() {
  # Replace the path with your actual script location
  python3 /path/to/nblm-nix/apps/zsh/nblm.py
}

```

## Usage

Simply run the command in your terminal:

```bash
nblm
```
1. **Select Action**: Choose between Sandbox (New), Existing Notebook, or Delete.
2. **Sandbox Mode**: Input URLs or file paths. Type `a` to start the analysis/summary, or `c` to abort and cleanup.
3. **Chat/Podcast**: Once inside a notebook, use `src` to add sources, `p` to generate a podcast in the background, or `s` to save/rename the temporary notebook.

## Key Technical Enhancements

Compared to the upstream `notebooklm-py`, this Nix-native version includes:

- **Playwright Wrapping**: Uses `makeWrapper` to set `PLAYWRIGHT_BROWSERS_PATH`, ensuring the CLI works out-of-the-box on NixOS.
- **Timeout Patches**: Automatically modifies the source code during the Nix build phase to extend RPC and generation timeouts from 30/300 seconds to 1800 seconds.

## Acknowledgment

Special thanks to **@teng-lin** for the original [notebooklm-py](https://github.com/teng-lin/notebooklm-py) implementation. This project serves as a Nix-specific enhancement and workflow wrapper.
