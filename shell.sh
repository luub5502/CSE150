#!/bin/bash
# prints even numbered lines of every file in directory
# https://unix.stackexchange.com/questions/26723/print-odd-numbered-lines-print-even-numbered-lines#:~:text=That%27s%20easy%3A%20sed%20-n%202~2p%20filename%20will%20print,sed%20-n%201~2p%20filename%20will%20print%20odd-numbered%20lines.
count=0
for file in *; do
    if [ -f "$file" ]; then
        while read line
        do
            evenNum=$(($count%2))
            if [ $evenNum -ne 0 ]
            then
                echo "$file: $line"
            fi
            ((count++))
            done < "$file"
    fi
done
