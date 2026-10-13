# Minesweeper Reversing

final project for intro to reversing (JCT). patching the old winmine.exe in 4 stages, no source code, just IDA / OllyDbg / CFF Explorer.
full write up with all the research is in Minesweeper Write-Up.pdf

## the challenges

Stage A - Mine Revealer
patch the game so when it starts all the mines are already flagged. everything else (clock, win condition, gameplay) stays the same. also had to answer where the board is in memory and what every bit of a cell means

Stage B - Quick Victory
find where the board size and the mine count are decided, then patch it so theres only one mine on the board (already flagged from A) so you win in like a second. not allowed to touch the clock

Stage C - Let the World Know Who You Are
add a MessageBox that pops up when the game opens, the game only starts after you press OK. had to find empty space in the exe for the code + strings and repoint the entry point at it

Stage D - Talk to the Outside World
make the game send a message to a HTTP server running locally on 127.0.0.1:80. the game doesnt import anything networking so this one was the hard one (LoadLibraryA + GetProcAddress -> URLDownloadToFileA)

## files

WINMINE.EXE - the original
winmine_stageA.exe - mines flagged
winmine_stageB.exe - A + one mine
winmine_stageC.exe - B + message box
winmine_stageD.exe - C + http beacon
server.py - small local listener for stage D

## how to run

stages A-C just run the exe (windows)

for stage D start the server first, then the exe:

```
python server.py
```

port 80 might need an admin terminal. if not you can do `python server.py 8080` but the exe has 80 hardcoded so it wont reach it.
press OK on the box and the server prints the message, it also gets saved to beacon_log.txt. the game also drops a report.tmp next to it, thats just the response, ignore it
