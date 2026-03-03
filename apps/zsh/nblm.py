#!/usr/bin/env python3
import os
import subprocess
import time
import tempfile
import shlex
import sys
import shutil


def check_dependencies():
    for cmd in ["fzf", "notebooklm"]:
        if not shutil.which(cmd):
            sys.exit(1)


def run_cmd(cmd, capture=False):
    if capture:
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        return result.stdout.strip()
    subprocess.run(cmd, shell=True)


def run_fzf(cmd_pipeline):
    with tempfile.NamedTemporaryFile(delete=False) as tf:
        tf_path = tf.name
    full_cmd = f"{cmd_pipeline} > {shlex.quote(tf_path)}"
    subprocess.run(full_cmd, shell=True)
    result = ""
    if os.path.exists(tf_path):
        with open(tf_path, "r") as f:
            result = f.read().strip()
        os.remove(tf_path)
    return result


def select_fzf(options, prompt):
    options_str = "\n".join(options)
    cmd = f"echo {shlex.quote(options_str)} | fzf --height 70% --reverse --prompt={shlex.quote(prompt)}"
    return run_fzf(cmd)


def select_nb(prompt):
    cmd = f"notebooklm list | fzf --ansi --height 70% --reverse --prompt={shlex.quote(prompt)} | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -n 1"
    return run_fzf(cmd)


def bg_podcast(nb_id, fmt, length, out_file):
    script = f"notebooklm use {shlex.quote(nb_id)} && notebooklm generate audio --format {shlex.quote(fmt)} --length {shlex.quote(length)} --wait && notebooklm download audio {shlex.quote(out_file)} --latest"
    subprocess.Popen(
        script, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def chat_loop(nb_id, is_saved):
    current_is_saved = is_saved
    while True:
        user_q = input(
            "Question (Input 'src': add, 'p': podcast, 's': save/rename, 'c': exit): "
        )
        if user_q == "c":
            if not current_is_saved:
                run_cmd(f"notebooklm use {shlex.quote(nb_id)}")
                run_cmd("notebooklm delete -y")
            break
        elif user_q == "s":
            new_title = input("Enter new title (leave empty to keep current): ")
            if new_title:
                run_cmd(f"notebooklm rename {shlex.quote(new_title)}")
            current_is_saved = True
        elif user_q == "src":
            src_input = input("URL or file path: ")
            if src_input:
                expanded = os.path.expanduser(src_input)
                run_cmd(f"notebooklm source add {shlex.quote(expanded)}")
        elif user_q == "p":
            fmt = select_fzf(["deep-dive", "brief", "critique", "debate"], "Format: ")
            if not fmt:
                continue
            length = select_fzf(["short", "default", "long"], "Length: ")
            if not length:
                continue
            ts = time.strftime("%Y%m%d_%H%M%S")
            download_dir = os.environ.get(
                "XDG_DOWNLOAD_DIR", os.path.expanduser("~/Downloads")
            )
            os.makedirs(download_dir, exist_ok=True)
            out_file = os.path.join(download_dir, f"notebooklm_{nb_id}_{ts}.mp4")
            bg_podcast(nb_id, fmt, length, out_file)
        elif user_q:
            run_cmd(f"notebooklm ask {shlex.quote(user_q)}")


def main():
    check_dependencies()
    action_raw = select_fzf(
        ["1: Sandbox (New)", "2: Existing Notebook", "3: Delete Notebook"],
        "Select Action: ",
    )
    if not action_raw:
        return
    action = action_raw.split(":")[0]
    if action == "1":
        ts = time.strftime("%s")
        nb_id = run_cmd(
            f"notebooklm create {shlex.quote('tmp_' + ts)} | grep -oE '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}' | head -n 1",
            capture=True,
        )
        if nb_id:
            run_cmd(f"notebooklm use {shlex.quote(nb_id)}")
            while True:
                src_input = input(
                    "Enter URL or path ('a': start analysis, 'c': abort): "
                )
                if src_input == "a":
                    break
                elif src_input == "c":
                    run_cmd("notebooklm delete -y")
                    return
                elif src_input:
                    run_cmd(
                        f"notebooklm source add {shlex.quote(os.path.expanduser(src_input))}"
                    )
            run_cmd(
                "notebooklm ask 'Please summarize all provided sources and extract the most important insights.'"
            )
            chat_loop(nb_id, is_saved=False)
    elif action == "2":
        nb_id = select_nb("Select Notebook: ")
        if nb_id:
            run_cmd(f"notebooklm use {shlex.quote(nb_id)}")
            chat_loop(nb_id, is_saved=True)
    elif action == "3":
        nb_id = select_nb("DELETE Notebook: ")
        if nb_id and input("Are you sure? (y/n): ").lower() == "y":
            run_cmd(f"notebooklm use {shlex.quote(nb_id)}")
            run_cmd("notebooklm delete -y")


if __name__ == "__main__":
    main()
