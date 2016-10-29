import argparse
import logging
import logging.handlers

'''
Author: Ankit Kumar
Commandline Parser for the Bot
This file is run by the user
It initializes the Logger and Parses and the Commandline Arguments
It Calls the corresponding function for the command requested
'''

def mkArgs():
    '''
    Parses Commnand Line
    Returns Parser and Arguments
    '''

    # define parser
    parser = argparse.ArgumentParser(description=__doc__)

    # define parser's options
    parser.add_argument('-D', '--debug', action="count",
                        help='set debug level')
    parser.add_argument('-v', '--verbose', action="count",
                        help='set verbose level')
    parser.add_argument('-l', '--logfile', type=str, default='-',
                        help='set log file (default stdin "-")')
    parser.add_argument('-L', '--loglevel', type=str, default='i',
                        help='set log level (default stdin "i")')

    # define subparser
    subparsers = parser.add_subparsers()

    # tweet fetch subparser
    fetch_parser = subparsers.add_parser('fetch', 
                                          help='fetch new tweets (stream)')
    fetch_parser.set_defaults(func=fetch_tweets)

    # tweet generate subparser
    generator_parser = subparsers.add_parser('generator', 
                                          help='generate new tweets')
    generator_parser.set_defaults(func=gen_tweets)

    args = parser.parse_args()

    logger = logging.getLogger()
    if args.loglevel:
        level = args.loglevel.lower()
        assert level in 'dwc', 'invalid log level'
        if level == 'd':
            logger.setLevel(logging.DEBUG)
        elif level == 'w':
            logger.setLevel(logging.WARNING)
        elif level == 'c':
            logger.setLevel(logging.CRITICAL)

    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.logfile == '-':
        hdlr = logging.StreamHandler()
    else:
        hdlr = logging.handlers.\
                RotatingFileHandler(args.logfile,
                                    maxBytes=2**24, backupCount=5)

    formatter = logging.Formatter('%(asctime)s' +
                                  '%(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)

    # add logger to args
    setattr(args, 'logger', logger)

    args.logger.debug(str(args))

    return parser, args


def main():
    parser, args = mkArgs()

    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.error("Please select a command!")

if "__name__" == "__main__":
    main()