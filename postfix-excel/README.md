# Postfix Cell Evaluator

A spreadsheet can be a powerful but easy to use tool for repetitive tabulation. In partic- ular, cells of a spreadsheet can contain formulas which consisting of mathematical op- erations and references to other cells. The goal of this problem is to write a program to evaluate the cells of a spreadsheet.

For example, the spreadsheet:

  |  A |  B
--|---|--
 1 | 1  |  2 3 +
 2 | 2 A1 *  | B1 A2 /


would evaluate to:

 |  A |  B
--|---|--
1 | 1  |  5
2 | 2 | 2.5

For this problem, you may assume that every cell of a matrix contains a mathematical
expression in postorder notation (meaning the operator follows the operands) which can
be comprised of the following:
 1. The binary operators {+, -, *, /}
 2. Numbers: these can be either integers or decimal numbers, and may be signed.
 3. References to other cells: these will be of the form ColumnRow, where Column is a capital letter, and Row is a positive integer

## Input and Output
Your program should take two command line parameters, `input_file` and `output_file`. The `input_file` will be a plaintext representation of a single spreadsheet, in which each line corresponds to a single row containing the comma delimited values of each cell in that row. Furthermore, if the spreadsheet can be successfully evaluated, your program should write the evaluated spreadsheet to `output_file` using a similar format. If there are any errors during evaluation, your program should print a descrip- tive error message instead of writing an output file. It is safe to assume that any input file will contain no more than 500,000 cells.
