# -*- coding: utf-8-*-
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Bogdan Maryniuk <bo@suse.de>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from jessy.modules import JessyModule, Phrase
from jessy.modules import _ddg as duck

try:
    import wikipedia
except ImportError as ex:
    wikipedia = None


class DefineWord(JessyModule):
    '''
    Plugin for word definition.
    '''
    NUMBERS = {
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    }

    ORDERS = {
        1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
        6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'nineth', 10: 'last',
    }

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def _extract_definition(self, text):
        '''
        Extracts definition from the given text

        :param text:
        :return:
        '''
        text = text.lower()
        definition = ''
        for kwd in self.keywords():
            if kwd in text:
                definition = text.split(kwd)[-1].split(' ')[-1]
                if definition:
                    break

        return definition

    def _get_answer(self, definition):
        '''
        Get answer.

        :param definition:
        :return: A series of sentences that needs to be said.
        :return:
        '''
        # Wikipedia
        if wikipedia:
            page_titles = wikipedia.search(definition)
            page = None
            if page_titles:
                for page_title in page_titles:
                    if page_title.lower() == definition:
                        page = wikipedia.page(page_title)
                        break
                if not page and 'disambiguation' not in page_titles[0]:
                    page = wikipedia.page(page_titles[0])

            if page:
                answer.append(Phrase().text(page.content.split('==')[0]
                                            .split('\n')[0]
                                            .encode('utf-8', 'ignore')).pause(1))

        result = duck.query(definition)
        if result.type == 'disambiguation' and  result.related:
            related = [res for res in result.related if hasattr(res, 'text') and not res.text.endswith('...')][:5]
            self.say('There {0} {1} definition{2} for this {3}'.format(
                (len(related) - 1) and 'are' or 'is',
                self.NUMBERS[len(related)],
                (len(related) - 1) and 's' or '',
                result.type))

            for r_num, r_data in enumerate(related):
                self.say("{}.".format(self.ORDERS[r_num + 1]))
                time.sleep(1)
                self.say(r_data.text.encode('UTF-8', 'ignore'))
                time.sleep(1)

        self.say('I hope this helps')

    def _handle(self, text):
        '''
        Main handler.

        :param text:
        :return:
        '''
        definition = self._extract_definition(text)
        if definition:
            self._mic.say('Let me look...')
            answer = self._get_answer(definition)  # Should go background before saying 'please wait'

    def handle(self, transcription):
        if self.matches(transcription):
            self._handle(transcription)
            return True

    @classmethod
    def keywords(cls):
        return ['define', 'means', 'meaning', 'definition']


plugin = DefineWord
