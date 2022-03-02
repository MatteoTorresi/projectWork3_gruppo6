# projectWork3_gruppo6
Design, Develop and Test an Alexa application that is able to:

- Given the region name,month and year calculate the overall number of doses
  delivered
- Given the month and year calculate the region that received the highest/lowest
  number of doses
- Given a region calculate the average value of delivered doses over the entire dataset

Develop back-end with AWS lambda

Check the following data:
https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/consegne-vaccini-latest.json

Analysis and resolution:
The project we worked on asked us to analyze a series of data regarding the distribution of vaccine doses against Covid-19 from the beginning of production up to the last few months, in the various Italian regions.

The task has been divided into three main requests:

in the first task we were asked to input the name of the region in which to carry out the operations, the month and year we wanted to take into consideration for the calculation of the doses sent in total
the second task required to establish which region had received the maximum and minimum number of doses, given the month and the year in which to carry out the checks
the third task asked us to make the average of all the doses delivered in a given region, taken as input
First we analyzed the structure of the json file from which we would then have to extract the information on vaccines and their distribution.
The structure of the file is a complex dictionary, containing a list of information for each day and country.
Each element of the list is divided into several elements:

we have the index of the element within the list,
the supplier for those vaccine doses,
the number of doses delivered on that date and the date of delivery,
the ISTAT code of the region that received the doses,
the name of the region.
The json file contains about 6 thousand elements, which increaseas the time to carry out operations, so we have adopted strategies to try to optimize the calculation times of each instruction as much as possible.
