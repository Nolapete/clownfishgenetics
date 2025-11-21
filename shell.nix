{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  # Add your project-specific dependencies here
  buildInputs = with pkgs; [
    python3
    # ... other packages
  ];

  shellHook = ''
    export DJANGO_ENV="development"
    # Additional shell commands can go here
  '';
}
