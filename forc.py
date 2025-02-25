#!/usr/bin/env python3

import getopt
import os
import sys
from io import StringIO

import log
from start import start



VERSION = '0.1.0'

DEF_INPUT_PATH = 'in'
DEF_OUTPUT_PATH = 'out'
DEF_MANIFEST = 'manifest.json'
DEF_ALIASES = None
DEF_DELIM_CODEPOINT = "-"

DEF_OUTPUT_FORMATS = ['SVGinOT']
DEF_COMPILER = 'ttx'



DEF_NO_VS16 = False
DEF_NO_LIG = False

DEF_NUSC = False
DEF_AFSC = False

DEF_NO_TEST = False

DEF_TTX_OUTPUT = False
DEF_DEV_TTX = False


HELP = f'''forc {VERSION}
by Mutant Standard
(mutant.tech)

USAGE: forc.py [options...]



HELP:
----------------------------------------------------
-h      Prints this help message.

Also look at /docs for full documentation.



WHAT TO BUILD FROM:
----------------------------------------------------
-i      Image glyphs directory (default: {DEF_INPUT_PATH})
-a      Alias glyphs file (optional)
-m      Manifest file (default: {DEF_MANIFEST})
-o      Output directory (default: {DEF_OUTPUT_PATH})

-d      Delimiter between ligatured codepoints
        (default: '{DEF_DELIM_CODEPOINT}')



HOW TO BUILD IT:
----------------------------------------------------
-F      Format (default: {DEF_OUTPUT_FORMATS[0]})
        comma separated with no spaces (ie. 'SVGinOT,CBx,sbixOT')

        Formats that require SVG images:
        - SVGinOT       (Many platforms)

        Formats that require PNG images:
        - sbixOT
        - sbixOTiOS     (DEVELOPMENT/TESTING)
        - CBx           (Google/Android)

-C      Compiler (default: {DEF_COMPILER})
        - ttx
        - forc (*will* give broken results atm)



OPTIONAL EXTRA FLAGS:
----------------------------------------------------

FOR CODEPOINTS

--no-vs16   Strips any presence of VS16 (U+fe0f) from the output.
--no-lig    (DEVELOPMENT OPTION) Strips ligatures from the output.


FOR SVGs

--nusc      No Unenforced SVG Contents Checking.
            Makes SVG checking less strict by allowing SVG contents
            that are not guaranteed to work in SVG checks.

--afsc      Affinity SVG Correction.
            Corrects quirks in SVGs images exported by Serif's
            Affinity software. Always use this if you are making
            a font with SVGs that come from Affinity software.



FOR ALL COMPILERS

--no-test   (DEVELOPMENT OPTION) Disables the font validation phase of
            font compilation.



FOR TTX COMPILER
Will be ignored if you are using a different compiler.

--ttx       Exports a matching ttx (.ttx) file for each format.

--dev-ttx   (DEVELOPMENT OPTION) Keeps the initial ttx that forc
            compiles before passing it to fonttools. This is
            different to the above, which is a full representation
            of the font file.



'''



def main():
    input_path = DEF_INPUT_PATH
    output_path = DEF_OUTPUT_PATH
    manifest_path = DEF_MANIFEST
    aliases_path = DEF_ALIASES
    delim_codepoint = DEF_DELIM_CODEPOINT

    output_formats = DEF_OUTPUT_FORMATS
    compiler = DEF_COMPILER

    no_vs16 = DEF_NO_VS16
    no_lig = DEF_NO_LIG

    nusc = DEF_NUSC
    afsc = DEF_AFSC

    no_test = DEF_NO_TEST

    ttx_output = DEF_TTX_OUTPUT
    dev_ttx_output = DEF_DEV_TTX


    try:
        opts, _ = getopt.getopt(sys.argv[1:],
                                'hi:o:m:a:d:F:C:',
                                ['help', 'no-vs16', 'no-lig', 'nusc', 'afsc', 'no-test', 'ttx', 'dev-ttx'])
        for opt, arg in opts:
            if opt in ['-h', '--help']:
                print(HELP)
                sys.exit()

            elif opt == '-i':
                input_path = arg
            elif opt == '-o':
                output_path = arg
            elif opt == '-m':
                manifest_path = arg
            elif opt == '-a':
                aliases_path = arg
            elif opt =='-d':
                delim_codepoint = arg

            elif opt == '-F':
                output_formats = arg.split(',')
            elif opt == '-C':
                compiler = arg


            elif opt =='--no-vs16':
                no_vs16 = True
            elif opt =='--no-lig':
                no_lig = True


            elif opt =='--nusc':
                nusc = True
            elif opt =='--afsc':
                afsc = True


            elif opt =='--no-test':
                no_test = True


            elif opt =='--ttx':
                ttx_output = True
            elif opt =='--dev-ttx':
                dev_ttx_output = True

    except Exception:
        print(HELP)
        sys.exit(2)
    try:
        flags = { "no_vs16": no_vs16
                , "no_lig": no_lig

                , "nusc": nusc
                , "afsc": afsc

                , "no_test": no_test

                , "ttx_output": ttx_output
                , "dev_ttx_output": dev_ttx_output
                }

        start( input_path
              , output_path
              , manifest_path
              , aliases_path
              , delim_codepoint

              , output_formats
              , compiler
              , flags
              )

    except Exception as e:
        log.out(f'\n!!! {e}', 31)
        raise e  ######################## TEMP
        sys.exit(1)
    log.out('All done!', 35)

if __name__ == '__main__':
    main()
