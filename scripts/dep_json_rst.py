# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import argparse, json, os, os.path as osp, re, logging
import spdx_lookup
from collections import defaultdict


class FakeLicense(object):
    def __init__(self, name, template, url = None):
        self.name = name
        self.template = template
        if url is not None:
            self.url = url

def enriched_spdx_lookup(spdx_license_id):
    if spdx_license_id == "EDL-1.0":
        return FakeLicense("Eclipse Distribution License - v 1.0", u"""All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
    Neither the name of the Eclipse Foundation, Inc. nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
""")
    elif spdx_license_id == "INSEE license":
        return FakeLicense("INSEE License",
         u"""Source: INSEE - Résumé  statistique des territoires. La rediffusion des données du produit, y compris à  des fins commerciales,est autorisée sans licence et sans versement de redevance.
""")
    elif spdx_license_id =="W3C-20150513":
        return FakeLicense("W3C Software and Document Notice and License",
u"""
By obtaining and/or copying this work, you (the licensee) agree that you have read, understood, and will comply with the following terms and conditions.

Permission to copy, modify, and distribute this work, with or without modification, for any purpose and without fee or royalty is hereby granted, provided that you include the following on ALL copies of the work or portions thereof, including modifications:

    The full text of this NOTICE in a location viewable to users of the redistributed or derivative work.
    Any pre-existing intellectual property disclaimers, notices, or terms and conditions. If none exist, the W3C Software and Document Short Notice should be included.
    Notice of any changes or modifications, through a copyright statement on the new code or document such as "This software or document includes material copied from or derived from [title and URI of the W3C document]. Copyright © [YEAR] W3C® (MIT, ERCIM, Keio, Beihang)."

Disclaimers

THIS WORK IS PROVIDED "AS IS," AND COPYRIGHT HOLDERS MAKE NO REPRESENTATIONS OR WARRANTIES, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO, WARRANTIES OF MERCHANTABILITY OR FITNESS FOR ANY PARTICULAR PURPOSE OR THAT THE USE OF THE SOFTWARE OR DOCUMENT WILL NOT INFRINGE ANY THIRD PARTY PATENTS, COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS.

COPYRIGHT HOLDERS WILL NOT BE LIABLE FOR ANY DIRECT, INDIRECT, SPECIAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF ANY USE OF THE SOFTWARE OR DOCUMENT.

The name and trademarks of copyright holders may NOT be used in advertising or publicity pertaining to the work without specific, written prior permission. Title to copyright in this work will at all times remain with copyright holders.
""", "https://www.w3.org/Consortium/Legal/2015/copyright-software-and-document")
    elif spdx_license_id =="Oracle Free Use Terms and Conditions":
        return FakeLicense("Oracle Free Use Terms and Conditions", None, url="https://www.oracle.com/downloads/licenses/oracle-free-license.html")
    else:
        return spdx_lookup.by_id(spdx_license_id)


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--versions", action="store_true")
    parser.add_argument("-f", "--format", help="format (rst - default or cnf - crazy notice file)", default="rst")

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--input', help='Input JSON file name', action='append', required=True)
    requiredNamed.add_argument('-d', '--directory', help='License text directory', required=False)
    requiredNamed.add_argument('-o', '--output', help='Output RST file name', required=True)
    return parser.parse_args()


def main():
    args = get_args()

    # Combine input files
    combined_json = []
    for cur_input in args.input:
        with open(cur_input, 'r', encoding="utf-8") as cur_file:
            cur_json = json.load(cur_file)
            if not isinstance(cur_json, list):
                raise Exception('File {} does not contain a JSON array'.format(cur_input))
            combined_json.extend(cur_json)

    # Enrich licenses with label and URL
    aggregate_json = defaultdict(list)
    for cur_dep in combined_json:
        license_id = cur_dep['license_type']
        spdx_license = enriched_spdx_lookup(license_id)
        cur_dep["licenseLabel"] = spdx_license.name if spdx_license else license_id
        if hasattr(spdx_license, "url"):
            cur_dep["genericLicenseUrl"] = spdx_license.url
        elif isinstance(spdx_license, spdx_lookup.License):
            cur_dep["genericLicenseUrl"] = "https://spdx.org/licenses/{}".format(license_id)
        else:
            cur_dep["genericLicenseUrl"] = license_id
        aggregate_json[cur_dep["printedName"].lower()].append(cur_dep)

    # Output
    if args.format == "rst":
        os.makedirs(os.path.dirname(args.output), exist_ok=True)

        with open(args.output, 'w+', encoding="utf-8") as output_file:
            output_file.write(".. This file was autogenerated, do not update\n\n")
            for _, cur_deps in sorted(aggregate_json.items()):
                cur_dep = cur_deps[0]
                output_file.write('* {}\n\n'.format(cur_dep['printedName']))
                if cur_dep.get('homepage', None):
                    output_file.write(' * Project: {}\n'.format(cur_dep['homepage'].replace("\n", ", ")))

                if args.versions:
                    if len(cur_deps) == 1:
                        output_file.write('Version: %s\n' % cur_dep['version'])
                    else:
                        output_file.write('Versions: %s\n' % ",".join(c['version'] for c in cur_deps))

                added_licenses = set()
                for c in cur_deps:
                    if c["licenseLabel"] not in added_licenses:
                        added_licenses.add(c["licenseLabel"])
                        license_url = c.get("genericLicenseUrl", "")
                        if license_url.startswith("http"):
                            output_file.write(' * License: `{} <{}>`_\n'.format(c["licenseLabel"], c["genericLicenseUrl"]))
                        else:
                            output_file.write(' * License: {}\n'.format(c["licenseLabel"]))


                added_copyrights = set()
                for c in cur_deps:
                    copyright = c.get('copyright_line', '')
                    if copyright and copyright not in added_copyrights:
                        added_copyrights.add(copyright)
                        output_file.write(' * {}\n'.format(re.sub(r'\r?\n', ' |br| ', copyright, 0, flags=re.MULTILINE)))
                output_file.write('\n')

    elif args.format == "cnf":
        os.makedirs(args.output)

        with open(osp.join(args.output, "NOTICE.txt"), "w", encoding="utf-8") as output_file:
            output_file.write("""Dataiku DSS third party dependencies notice file
    ################################################

    Preamble
    ========

    This file and the associated license files list the third-party components that
    Dataiku DSS uses and that are distributed as part of the Dataiku DSS software.

    For each third-party component, this file details the information about the component,
    the copyright statement or authors, and the license under which Dataiku distributes
    this third-party component as part of Dataiku DSS.

    Provision of source code
    ========================

    As part of the obligations with regards to some of the licenses listed in this document,
    Dataiku makes the source code of the third-party component available to you.

    The information for each such component lists the homepage and or repository URL for said
    component, from which you can obtain the source code.

    Alternatively, Dataiku offers to provide source code of software licensed under any of
    such licenses to you by electronic transmission, without charge, upon written request to:

    Dataiku - Open Source Software Operations
    203 rue de Bercy
    75009 Paris
    France

    This offer is valid for a period of three (3) years from the date of the distribution
    of this product by Dataiku.

    This offer is only valid for components distributed under one of the following licenses:

    * The GNU Lesser General Public License versions 2 or 3
    * The Mozilla Public License versions 1 or 2
    * The Eclipse Public License versions 1 or 1.1
    * The Open Database License version 1

    """)
            license_missing = []

            for cur_dep in sorted(combined_json, key = lambda x : (x["printedName"].lower(), x["lic"] or 0)):
                slug_name = re.compile("[^A-Za-z0-9]").sub("-", cur_dep['printedName'])

                output_file.write("\n\n\n%s\n========================================\n" % cur_dep["printedName"])
                output_file.write("%s\n\n" % cur_dep['copyright_line'])
                output_file.write('License: {}\n'.format(cur_dep["licenseLabel"]))
                license_id = cur_dep['license_type']

                if "license_txt" in cur_dep:
                    with open(os.path.join(args.directory, cur_dep["license_txt"]), encoding="utf-8") as f:
                        license_text = f.read()
            else:
                license_missing.append(cur_dep)

                if license_text is not None:
                    with open(osp.join(args.output, "license-%s.txt" % slug_name), "w", encoding="utf-8") as f:
                        f.write(license_text)
                    output_file.write("Full license text: license-%s.txt\n" % slug_name)

                output_file.write("\n")
                if 'homepage' in cur_dep:
                    output_file.write('Homepage: {}\n'.format(cur_dep['homepage']))
                if 'repository' in cur_dep:
                    output_file.write('Repository: {}\n'.format(cur_dep['repository']))

                if args.versions and len(cur_dep.get('version', '')):
                    output_file.write('Version: %s\n' % cur_dep['version'])

                output_file.write('\n')

        logging.info("########################################")
        logging.info("# Errors and warnings summary")
        logging.info("########################################")
        for dep in license_missing:
            logging.error("Missing license text for dep: %s" % dep)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
