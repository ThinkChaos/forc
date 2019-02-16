#!/usr/bin/env python3

import getopt
import os
import sys
import json
from io import StringIO

import log
from export import export



VERSION = '0.0.1'
DEF_MANIFEST = 'manifest.json'
DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_OUTPUT_FORMATS = ['SVGinOT']
DEF_TTX_OUTPUT = False
DEF_DEV_TTX = False
DEF_DELIM = "-"

DEF_NO_LIG = False
DEF_NO_VS16 = False
DEF_NFCC = False

HELP = f'''forc {VERSION}
by Mutant Standard
(mutant.tech)

USAGE: forc.py [options...]

OPTIONS:
-h      prints this help message

-m      input JSON manifest (default: {DEF_MANIFEST})

-i      input directory path (default: {DEF_INPUT_PATH})
        Should have 'png' and/or 'svg' subfolders for PNG and SVG
        images respectively.

-o      output (default: {DEF_OUTPUT_PATH})

-F      format (default: {DEF_OUTPUT_FORMATS})

        formats that require SVG images:
        - SVGinOT       SVG with OpenType ligatures.

        formats that require PNG images:
        - sbixTT        (macOS) sbix with TrueType ligatures.
        - sbixOT        sbix with OpenType ligatures.
        - sbixTTiOS     (iOS) sbix with TrueType ligatures,
                        packaged in an iOS Configuration Profile.
        - sbixOTiOS     (DEVELOPMENT/TESTING) sbix with OpenType ligatures,
                        packaged in an iOS Configuration Profile.
        - CBx           (Google/Android) CBDT/CBLC with OpenType
                        ligatures.


-d      delimiter between ligatured codepoints
        (default: '{DEF_DELIM}')



--ttx       export an additional ttx (.ttx) file for each format.

--dev-ttx   keep the initial ttx that forc compiles before
            passing it to fonttools.

--no-lig    (DEVELOPMENT OPTION) strip ligatures from the output.

--no-vs16   (DEVELOPMENT OPTION) strip any presence of VS16 (U+fe0f)
            from the output.

--nfcc      No File Consistency Checking. Stops forc from checking
            if the images in the format subfolders are all the same.
            Only use if you are inputting data where that guarantee
            has already been made and you want to save time.

'''



def main():
    manifest_path = DEF_MANIFEST
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    output_formats = DEF_OUTPUT_FORMATS
    ttx_output = DEF_TTX_OUTPUT
    dev_ttx_output = DEF_DEV_TTX
    delim = DEF_DELIM

    no_lig = DEF_NO_LIG
    no_vs16 = DEF_NO_VS16
    nfcc = DEF_NFCC

    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hm:i:o:F:d:',
                                ['help', 'ttx', 'dev-ttx', 'no-lig', 'no-vs16', 'nfcc'])
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg
            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt =='-d':
                delim = arg
            elif opt =='--ttx':
                ttx_output = True
            elif opt =='--dev-ttx':
                dev_ttx_output = True
            elif opt =='--no-lig':
                no_lig = True
            elif opt =='--no-vs16':
                no_vs16 = True
            elif opt =='--nfcc':
                nfcc = True

    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        with open(manifest_path, "r") as read_file:
            m = json.load(read_file)

        export(m, input_path, output_path, output_formats, delim, ttx_output, dev_ttx_output, no_lig, no_vs16, nfcc)

    except Exception as e:
        log.out(f'!!! {e}', 31)
        raise e  ######################## TEMP
        sys.exit(1)
    log.out('All done', 35)

if __name__ == '__main__':
    main()
