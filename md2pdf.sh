#!/bin/bash
for infile in $@; do
  [ -e "$infile" ] || continue
  ext="${infile##*.}"
  base=$(basename "$infile" "$ext")
  outfile="$base""pdf"
  #echo  infile "$infile"
  #echo outfile "$outfile"
  if [ ! -f "$outfile" ]
  then
    pandoc --pdf-engine=xelatex --template my-template.tex \
    --variable mainfont="D2Coding"  default.yaml \
    "$infile" -o "$outfile"
    echo "CONVERTED:  $outfile"
  else
    echo "skipped:    $outfile"
  fi
done
  
