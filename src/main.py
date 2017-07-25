import argparse
import sys

from dg.geocoder.iati.iati_codes import iati_publishers, iati_countries
from dg.geocoder.iati.iati_downloader import bulk_data_download






def main(args):
    try:
        parser = argparse.ArgumentParser(description="Utility to auto-geocode IATI projects")

        parser.add_argument("-m", "--command", type=str, default='geocode', choices=['geocode', 'download', 'generate'],
                            required=False,
                            dest='command',
                            help='use geocode to auto-geocode projects in file provided, or download to get raw '
                                 'data from IATI registry')

        parser.add_argument("-f", "--file", type=str, default=None, required=False, dest='file',
                            help='IATI XML activities')

        parser.add_argument("-p", "--path", type=str, default='docs', required=False, dest='path',
                            help='lookup path for of private documents ')

        parser.add_argument("-d", "--download_path", type=str, default='download', required=False, dest='download_path',
                            help='Downloaded data storage folder, default will be download folder')

        parser.add_argument("-o", "--org", type=str, default=None, required=False, dest='organisation',
                            help='Reporting organisation of the data to be download')

        parser.add_argument("-c", "--countries", type=str, default=None, required=False, dest='countries',
                            help='Countries codes')

        parser.add_argument("-l", "--limit", type=str, default=100, required=False, dest='limit',
                            help='Number of activities to download')

        args = parser.parse_args(args)

        if args.command == 'geocode':
            file = args.file
            doc_path = args.path
            if file is None:
                print('Please provide an input file using -f')

        elif args.command == 'download':
            if args.organisation is None or args.organisation not in iati_publishers:
                print('Please provide a valid reporting organisation code please look at '
                      'http://iatistandard.org/202/codelists/OrganisationIdentifier/')
                return
            if args.countries is None or args.countries != 'ALL':
                print('Provide a recipient country code or set it to ALL, please '
                      'look at http://iatistandard.org/202/codelists/Country/')
                return
            if args.countries == 'ALL':
                countries = iati_countries
            else:
                countries = args.countries
            bulk_data_download(args.organisation, countries, download_path=args.download_path,
                               activities_limit=args.limit)
        elif args.command == 'generate':
            print('generate corpora')

    except (KeyboardInterrupt, SystemExit):
        print('By!')


# report error and proceed


if __name__ == '__main__':
    main(sys.argv[1:])
