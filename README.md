# nblm-nix

A Nix-optimized Python CLI and Zsh wrapper for [NotebookLM](https://notebooklm.google.com/), built upon [notebooklm-py](https://github.com/teng-lin/notebooklm-py) (v0.3.2). This project ensures a seamless execution environment on NixOS and similar systems by wrapping Playwright and extending timeouts.

## Features

- **Sandbox Mode**: Creates a temporary notebook (`tmp_[timestamp]`) for immediate analysis. The notebook is automatically deleted upon exit to maintain environment hygiene.
- **FZF-Powered Interface**: Interactive selection for actions, notebooks, podcast formats, and audio lengths.
- **Background Generation**: Audio generation processes are offloaded to the background, allowing uninterrupted terminal usage.
- **Nix-Native Enhancements**:
    - **Playwright Integration**: Pre-configured `PLAYWRIGHT_BROWSERS_PATH` via `makeWrapper`.
    - **Extended Timeouts**: Increased RPC and generation timeouts to 1800s via `postPatch` to handle large files.

## Installation

### 1. Install via Nix Profile

To install the `nblm` command globally in your environment:

```bash
 nix profile install github:yktsnet/nblm-nix
```

### 2. Run without Installation

You can execute the tool directly using Nix Flakes:

```bash
 nix run github:yktsnet/nblm-nix
```

### 3. Zsh Alias (Optional)

Since the package already provides the `nblm` binary, you can simply use it. If you need an alias or specific function:

```zsh
 # No path configuration needed if installed via nix profile
 alias nblm='nblm'
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

- **Playwright Wrapping**: Ensures the Playwright driver correctly locates browser binaries on NixOS.
- **Source Patching**: Replaces default 30/300s timeouts with 1800s via `sed` during the build phase.
- **Dependency Management**: Automatically includes `fzf`, `gnugrep`, and `coreutils` in the runtime `PATH`.

## License

MIT License - Copyright (c) 2026 yktsnet

## Acknowledgment

Special thanks to **@teng-lin** for the original [notebooklm-py](https://github.com/teng-lin/notebooklm-py) implementation.
