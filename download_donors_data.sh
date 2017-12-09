#!/usr/bin/sh

#(USAID) US-GOV-1
./geocoder.sh  --command=download --publisher=US-GOV-1 --countries=ALL -l=100
#African Development Bank 46002
./geocoder.sh --command=download --publisher=46002 --countries=ALL -l=20
#rem  UN Women  XM-DAC-411124
./geocoder.sh --command=download  --publisher=XM-DAC-411124 --countries=ALL -l=100
# UK - Department for International Development (DFID)  GB-GOV-1
./geocoder.sh geocoder  -cdownload -p=oGB-GOV-1 -cALL
