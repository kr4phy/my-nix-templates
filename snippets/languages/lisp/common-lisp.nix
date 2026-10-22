{ pkgs }

with pkgs; [
  # Common Lisp Implementations
  sbcl
  sbclPackages.coalton
  
  # clisp
  # ccl
  # ecl

  rlwrap

  # Utilities
  asdf
  # quicklisp
  # roswell

  # Editor
  emacs
]