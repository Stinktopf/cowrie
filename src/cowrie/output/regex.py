# Copyright (c) 2015 Michel Oosterhof <michel@oosterhof.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The names of the author(s) may not be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHORS ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

# Notice of modification
#
# This code is a modified version of the textlog.py code by Michel Oosterhof.
# The modification was created by Lucas Immanuel Nickel and uses CommonRegex
# to anonymize log files.

from __future__ import annotations

import cowrie.core.cef
import cowrie.core.output
from cowrie.core.config import CowrieConfig

from commonregex import CommonRegex
import re


class Output(cowrie.core.output.Output):
    """
    regex output
    """
    def regex(self, text_to_anonymize):
        parsed_text = CommonRegex(text_to_anonymize)
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.emails, "<EMAIL_ADDRESS>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.links, "<URL>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.ips, "<IP_ADDRESS>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.ipv6s, "<IP_ADDRESS>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.dates, "<DATE_TIME>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.times, "<DATE_TIME>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.phones, "<PHONE_NUMBER>")
        text_to_anonymize = self.sanitize(text_to_anonymize, parsed_text.credit_cards, "<CREDIT_CARD>")
        return text_to_anonymize

    def sanitize(self, text_to_anonymize, matches, replacement):
        for match in matches:
            text_to_anonymize = re.sub(match, replacement, text_to_anonymize)
        return text_to_anonymize

    def start(self):
        self.format = CowrieConfig.get("output_regex", "format")
        self.outfile = open(CowrieConfig.get("output_regex", "logfile"), "a")

    def stop(self):
        pass

    def write(self, logentry):
        if self.format == "cef":
            self.outfile.write("{} ".format(logentry["timestamp"]))
            self.outfile.write(f"{cowrie.core.cef.formatCef(logentry)}\n")
        else:
            self.outfile.write("{} ".format(logentry["timestamp"]))
            self.outfile.write("{} ".format(logentry["session"]))
            self.outfile.write(self.regex(("{}".format(logentry["message"]))) + "\n")
        self.outfile.flush()
