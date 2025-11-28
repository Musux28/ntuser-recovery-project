Scalpel, a file carving utility, was used on the evidence image file to attempt to recover the evidence images and files deleted by MREVIL.

Scalpel comes with default file headers and footers to be used in the configuration file. We edited the file to search only for jpg and pdf files. The following headers and footers were used formatted in hex followed by the exact text in the conf file:
REVERSE signifies that scalpel will search from the footer to the header. This is in case the hex data for the header appears as data inside the file. This prevents the files from being truncated early during carving.

JPG:
FF D8 FF E0        FF D9
\xff\xd8\xff\xe0        \xff\xd9      REVERSE

PDF:
25 50 44 46         45 4F 46 0A
\x25\x50\x44\x46        \x45\x4f\x46\x0a      REVERSE

The audit.txt file provided with the output from Scalpel provided a list of all the jpg and pdf files carved. As well as the commands used. 

The pdf documents were unable to be successfully recovered. However, the jpg image downloaded and exported by MREVIL was recovered as 00000925.jpg.
(Many default images and icons used by Windows are in the jpg format and are carved as well, this is why so many jpg files are carved from the image.)
Despite MREVIL deleting the files and emptying the recycling bin, casuing the pointers in the master file table to be deleted, the raw data was not overwritten allowing the extraction of the image.
