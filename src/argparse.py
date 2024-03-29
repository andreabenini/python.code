# Version 1: argparse
# Really basic argparse example usage
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument( '-f', '--filename', type=str, default='myfile.conf', help='Some useful help message')
    # Mutually exclusive group
    mutex = parser.add_mutually_exclusive_group()
    mutex.add_argument('--arg1', action='store_true', help='Help on arg1')
    mutex.add_argument('--arg2', action='store_true', help='Help on arg2')
    #
    subparser = parser.add_subparsers(dest='command', help='MyFavorite Command')
    connectionList = subparser.add_parser('list')
    connectionList.set_defaults(type=str, help='<list> command help here')
    connectionAdd = subparser.add_parser('add')
    connectionAdd.add_argument('url', type=str, help='<add> <url> help message here')
    connectionDel = subparser.add_parser('del')
    connectionDel.add_argument('url', type=str, help='<del> <url> help message here')
    args = parser.parse_args()
    # Now you have:
    # - args.filename   [optional] default to myfile.conf
    # - args.command    [mandatory] it might be one of: [list,add,del]
    # - args.url        [mandatory when args.command is <add> or <del>, not available when args.command is <list> ]
    # - args.arg1, args.arg2 [mutually exclusive]


# Version 2: optparse
# Input parameters
import optparse
if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option('-H', '--hostname', dest='hostname', default='my.own.host.name', help='can provide some hostname here')
    parser.add_option('-u', '--username', dest='username', default='ben', help='default username')
    parser.add_option('-p', '--password', dest='password', default='',    help='default password')
    (options, _) = parser.parse_args()
    if not options.hostname or not options.username:
        parser.print_help()
        sys.exit(1)
