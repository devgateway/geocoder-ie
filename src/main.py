import argparse
import sys

from dg.geocoder.iati.iati_codes import iati_publishers, iati_countries
from dg.geocoder.processor import process


def main(args):
    try:
        parser = argparse.ArgumentParser(description="Utility to auto-geocode IATI projects")

        parser.add_argument("-c", "--command", type=str, default='geocode', choices=['geocode', 'download', 'generate',
                                                                                     'train'],
                            required=False,
                            dest='command',
                            help='use geocode to auto-geocode projects in file provided, or download to get raw '
                                 'data from IATI registry')

        parser.add_argument("file", type=str, default=None, nargs='+', help='IATI XML activities')

        parser.add_argument("-p", "--publisher", type=str, default=None, required=False, dest='organisation',
                            help='Reporting organisation of the data to be download')

        parser.add_argument("-co", "--countries", type=str, default=None, required=False, dest='countries',
                            help='Countries codes')

        parser.add_argument("-l", "--limit", type=str, default=50, required=False, dest='limit',
                            help='Number of activities to download')

        parser.add_argument("-n", "--name", type=str, required=False, dest='name',
                            help='classifier name')

        args = parser.parse_args(args)

        if args.command == 'geocode':

            file = args.file[0]
            print('GEOCODE {}'.format(file))
            if file is None:
                print('Please provide an input file using -f')
            else:
                process(file)

        elif args.command == 'download':
            if args.organisation is None or args.organisation not in iati_publishers:
                print('Please provide a valid reporting organisation code please look at '
                      'https://www.iatiregistry.org/publisher')
                return
            if args.countries is None or args.countries != 'ALL':
                print('Provide a recipient country code or set it to ALL, please '
                      'look at http://iatistandard.org/202/codelists/Country/')
                return
            if args.countries == 'ALL':
                countries = iati_countries
            else:
                countries = args.countries

            from dg.geocoder.iati.iati_downloader import bulk_data_download
            bulk_data_download(args.organisation, countries, activities_limit=args.limit)
        elif args.command == 'train':
            name = args.name
            if name is None:
                print('Please provide a name for the new classifier using -n')
            else:
                print('we will train and save a new classifier from database corpora')
                from dg.geocoder.classification.trainer import train_classifier
                cls = train_classifier(plot_results=True)
                cls.save(name)

        elif args.command == 'generate':
            print('Corpora database will be erased, Are you sure to continue?')
            if input('[y/n]').lower() == 'y':
                from corpora_generator import generate
                generate()
                print('done!')

    except (KeyboardInterrupt, SystemExit):
        print('adios!')


# report error and proceed
if __name__ == '__main__':
    main(sys.argv[1:])
