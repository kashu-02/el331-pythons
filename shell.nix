{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python3
    python311Packages.nltk
  ];

  shellHook = ''

  '';
}