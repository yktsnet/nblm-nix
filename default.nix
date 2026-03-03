{ pkgs ? import <nixpkgs> { } }:

let
  notebooklm-py = pkgs.python3Packages.buildPythonApplication rec {
    pname = "notebooklm-py";
    version = "0.3.2";
    pyproject = true;

    src = pkgs.fetchFromGitHub {
      owner = "teng-lin";
      repo = "notebooklm-py";
      rev = "v0.3.2";
      hash = "sha256-TXaJbOfWklqDSrtWbZq1vaIMr+sCknfuSLYnfpI4QkU=";
    };

    postPatch = ''
      find src -type f -name "*.py" -exec sed -E -i 's/\btimeout[[:space:]]*=[[:space:]]*[0-9]+/timeout=1800/g' {} +
    '';
    build-system = with pkgs.python3Packages; [ hatchling hatch-fancy-pypi-readme ];
    dependencies = with pkgs.python3Packages; [ httpx click rich playwright ];
    doCheck = false;
  };

  notebooklm = pkgs.symlinkJoin {
    name = "notebooklm";
    paths = [ notebooklm-py ];
    buildInputs = [ pkgs.makeWrapper ];
    postBuild = ''
      wrapProgram $out/bin/notebooklm --set PLAYWRIGHT_BROWSERS_PATH ${pkgs.playwright-driver.browsers}
    '';
  };

  nblm-script = pkgs.stdenv.mkDerivation {
    name = "nblm-script";
    src = ./apps/zsh;
    installPhase = ''
      mkdir -p $out/bin
      cp nblm.py $out/bin/nblm
      chmod +x $out/bin/nblm
    '';
  };

in
pkgs.symlinkJoin {
  name = "nblm-env";
  paths = [ notebooklm nblm-script ];
  buildInputs = [ pkgs.makeWrapper ];
  postBuild = ''
    wrapProgram $out/bin/nblm \
      --prefix PATH : ${pkgs.lib.makeBinPath [ notebooklm pkgs.fzf pkgs.gnugrep pkgs.coreutils ]}
  '';
}
