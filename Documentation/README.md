## Build
`pdflatex -synctex=1 -interaction=nonstopmode %.tex|bibtex "Protocols"|makeglossaries %|pdflatex -synctex=1 -interaction=nonstopmode %.tex|pdflatex -synctex=1 -interaction=nonstopmode %.tex`