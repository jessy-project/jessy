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
from jessy.modules.lib import get_definition

try:
    import wikipedia
    from wikipedia import DisambiguationError
except ImportError as ex:
    wikipedia = None


class DefineWord(JessyModule):
    '''
    Plugin for word definition.
    '''
    NUMBERS = {0: 'no',
        1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
    }

    ORDERS = {0: 'no',
        1: 'first', 2: 'second', 3: 'third', 4: 'fourth', 5: 'fifth',
        6: 'sixth', 7: 'seventh', 8: 'eighth', 9: 'nineth', 10: 'last',
    }

    def __init__(self, *args, **kwargs):
        JessyModule.__init__(self, *args, **kwargs)

    def join_for_more(self, data, limit=3):
        '''
        Join for more. This joins many options into one sentence with the limitation.
        '''
        _data = []
        for term in (limit and data[:limit] or data):
            if not term.lower().startswith('all pages beginning with') and not term.lower().startswith('all pages with titles containing'):
                _data.append(term.split('(')[0].strip())
        return ', '.join(_data[:-1]) + (limit and ' or {0} and even more'.format(_data[-1]) or ' and {0}'.format(_data[-1]))

    def ask_wikipedia(self, definition):
        '''
        Ask Wikipedia for the definition.

        :param definition:
        :return:
        '''
        # TODO: this method should run in a separate process, asynchronously

        is_exact = False
        out = []
        if not wikipedia:
            return is_exact, out

        page_titles = wikipedia.search(definition)
        page = None
        if page_titles:
            for page_title in page_titles:
                if page_title.lower() == definition:
                    try:
                        page = wikipedia.page(page_title)
                        is_exact = True
                    except DisambiguationError as ex:
                        out.append(Phrase().text('This can refer to a many things, such as {0}'.format(self.join_for_more(ex.options, limit=None))))
                        return is_exact, out

            if not page and 'disambiguation' not in page_titles[0]:
                try:
                    page = wikipedia.page(page_titles[0])
                except Exception as ex:
                    out.append(Phrase().text(str(ex)))

        if page and not out:
            out.append(Phrase().text(page.content.split('==')[0]
                                     .split('\n')[0]
                                     .encode('utf-8', 'ignore')).pause(1))
        return is_exact, out

    def ask_duck(self, definition):
        '''
        Ask duckduckgo for the definition

        :param definition:
        :return:
        '''
        answer = []
        result = duck.query(definition)
        if result.type == 'disambiguation' and  result.related:
            related = [res for res in result.related if hasattr(res, 'text') and not res.text.endswith('...')][:5]
            answer.append(
                Phrase().text('There {0} {1} definition{2} for this {3}'.format(
                    (len(related) - 1) and 'are' or 'is',
                    self.NUMBERS[len(related)],
                    (len(related) - 1) and 's' or '',
                    result.type
                ))
            )

            for r_num, r_data in enumerate(related):
                answer.append(Phrase().text("{}.".format(self.ORDERS[r_num + 1])).pause(1))
                answer.append(Phrase().text(r_data.text.encode('UTF-8', 'ignore')).pause(1))
        return answer

    def _get_answer(self, definition):
        '''
        Get answer.

        :param definition:
        :return: A series of sentences that needs to be said.
        '''
        is_exact, answer = self.ask_wikipedia(definition)

        if not is_exact and not answer:
            answer = self.ask_duck(definition) or answer
            if answer:
                answer.append(Phrase().text('I hope this helps'))

        if not answer:
            answer.append(Phrase().text('Unfortunately, I do not know what means {}'.format(definition)))

        return answer

    def _handle(self, text):
        '''
        Main handler.

        :param text:
        :return:
        '''
        definition = get_definition(text.lower())
        if definition:
            self.say('Let me look...')
            answer = self._get_answer(definition)  # Should go background before saying 'please wait'
            for phrase in answer:
                self.say(phrase)

    def handle(self, transcription):
        if self.matches(transcription):
            self._handle(transcription)
            return True

    @classmethod
    def keywords(cls):
        return ['define', 'means', 'meaning', 'definition', 'what']


plugin = DefineWord
