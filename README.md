Constraint-satisfaction sudoku solver using Python. Keeps track of possible candidates for each cell and dynamically prunes these sets on placement of a value in current row, column, box. Has a minimum remaining value heuristic in situations where backtracking is required.

Type in terminal - python sudoku.py - then follow the instructions printed for you.

Some sample input for you so that you don't have to get a sudoku board.

Easy (no backtracking, mainly naked singles): 680000400504000203029534061000103000160089030005276048046000007207815600901000380

Medium (one backtrack, lots of hidden singles): 000160902109502806326789154060850000010070000007920000092018500038095021651207089

Hard (multiple backtracks): 400000300028009000000000002000001007170000900050020080000050000300700100701308050
