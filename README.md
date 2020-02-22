# maharashtra_parser

### Requirements:
- tesseract needs to be installed and to be accessible from the terminal.
- The number recognition relies on an only-numbers model that can be found here: https://github.com/Shreeshrii/tessdata_shreetest/blob/master/digits_comma.traineddata Copy that into rootdir/tessdata (where you should also find other models like eng.traineddata)




### About the parser
The parser reads both the values and the corresponding labels from the Maharashtra Electricity Dashboard: https://mahasldc.in/wp-content/reports/sldc/mvrreport3.jpg

The labels can be used to validate results and to detect potential changes in the underlying picture.

To reduce complexity the parser is provided with a list of the locations. Like shown below, the recognition boils down to simple single-line problems.  

![alt text](https://github.com/GitMatze/maharashtra_parser/blob/master/2020-02-22T17%2000.png)

