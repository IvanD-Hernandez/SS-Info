#!/bin/zsh

python3 DatabaseUI.py -s 1 -v blackBolt "Levinthus Phoenix" "Phoenix" "3 Stars" "Soul Searching"    
python3 DatabaseUI.py -s 2 -v "Ghosts on Campus" "Has anyone noticed the strange activity in the plaza"
python3 DatabaseUI.py -s 3
python3 DatabaseUI.py -s 4
python3 DatabaseUI.py -s 5 -f student_name -v "Levinthus Phoenix"
python3 DatabaseUI.py -s 6 -f event_name -v "Ghosts on Campus"
python3 DatabaseUI.py -s 7 -f username student_name -v PhoenixPrince "Levinthus Phoenix"
python3 DatabaseUI.py -s 8 -f event_description event_name -v "HEEEELLLLPP GHOSTS ARE ATTACKING ME" "Ghosts on Campus"
python3 DatabaseUI.py -s 9 -f student_name -v "Levinthus Phoenix"
python3 DatabaseUI.py -s 10 -f event_name -v "Ghosts on Campus"