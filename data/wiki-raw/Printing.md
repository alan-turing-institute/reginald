**See [this TopDesk page](https://turingcomplete.topdesk.net/tas/public/ssp/content/detail/service?unid=e0855f770c4d4f49850780d75a33b068) for info on printing at the institute.** 

## Tips

### Advice on printing via CUPS (the Common Unix Printing System, used by MacOS)

```
lpr -T "Gargleblaster" -o InputSlot=Tray3 -o XRAFinisherStapleOption=True -o XRFinishing=Staple -o XRStapleOpti
on=1Staple -o XRStapleLocation=TopLeft -o XRAnnotationOption=Standard temp/*.pdf
```

Print all pdfs in `temp`, stapling the lot, and add a small annotation saying "Gargleblaster" in the top left.

(NB: The default input tray is `Tray1` but this is A3 paper on our printers.)

### Printing A3, double sided etc.

To get additional print settings like these have a look at the instructions here:
https://github.com/alan-turing-institute/knowledgebase/wiki/How-to-Print-in-A3-on-Mac

The office also has a stationary cupboard with the usual office supplies. 

