import argparse
import logging
import sys

from dg.geocoder.iati.iati_codes import iati_countries
from dg.geocoder.processor.file_processor import FileProcessor

logger = logging.getLogger()


def main(args):
    try:
        parser = argparse.ArgumentParser(description="Auto-geocode activity projects")

        parser.add_argument("-c", "--command", type=str, default='geocode', choices=['geocode', 'download', 'generate',
                                                                                     'train'],
                            required=False,
                            dest='command',
                            help='Use geocode to auto-geocode file. '
                                 'Use download to get raw  data from IATI registry. '
                                 'Use generate to generate a corpora. '
                                 'Use train to train a new classifier ')

        parser.add_argument("-f", "--file", type=str, default=None, nargs='+',

                            help='Use together with -c geocode to pass a file to process, The file can be a IATI '
                                 'activities file, pdf document, odt document or txt file')

        parser.add_argument("-p", "--publisher", type=str, default=None, required=False, dest='organisation',
                            help='Use together with -c download  to download data of specific IATI Publisher ')

        parser.add_argument("-t", "--countries", type=str, default=None, required=False, dest='countries',
                            help='Use together with -c geocode to filter geonames search \n '
                                 'Use together with -c download to download data of specific countries')

        parser.add_argument("-l", "--limit", type=str, default=50, required=False, dest='limit',
                            help='Use together with -c download to limit the Number of activities to download '
                                 'for each publisher/country')

        parser.add_argument("-n", "--name", type=str, required=False, dest='name',
                            help='set the new classifier name')

        parser.add_argument("-o", "--output", type=str, required=False,  dest='outputFormat',
                            help='Set output format, default json', choices=['xml', 'tsv', 'json'])

        args = parser.parse_args(args)

        if args.command == 'geocode':
            file = args.file[0] if args.file else None
            format = args.outputFormat

            print('{} will be geocoded'.format(file))
            if file is None:
                print('Please provide an input file using -f')
            else:
                cty_codes = args.countries.split(',') if args.countries else None

                out = FileProcessor(file, cty_codes=cty_codes).process().write_output(format, '')
                print('Results were saved in {}'.format(out))

        elif args.command == 'download':
            if args.organisation is None:
                print('Please provide a publisher code using -p parameter,  please look at '
                      'https://www.iatiregistry.org/publisher')
                return
            if args.countries is None or args.countries != 'ALL':
                print('Provide a recipient country code or set it to ALL by using -t parameter, '
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
                from dg.geocoder.data.corpora_generator import generate
                generate()
                print('done!')

    except (KeyboardInterrupt, SystemExit):
        logger.info('Chau!')
    except Exception as e:
        logger.error('Unexpected error {}'.format(e))


# report error and proceed
if __name__ == '__main__':
    main(sys.argv[1:])
