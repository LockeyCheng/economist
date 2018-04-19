#!/usr/bin/bash

basePath='./articles/pdffiles/'
for file in `ls $basePath`;
        do
                if [ -f "$basePath/$file" ]; then
                    pdf2txt.py -o "./articles/txtfiles/${file}.txt" "$basePath/$file"
                fi
        done
