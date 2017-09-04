class CodingResults(object):
    def __init__(self, tagged):
        self.tagged = tagged

    @staticmethod
    def gap_length(word1, word2, text):
        """Returns the number of characters after the end of word1 and
        before the start of word2 in text. Also returns the "trimmed"
        text with whitespace through word1's position and the
        merged words expression.
        """
        pos1, pos2 = text.index(word1), text.index(word2)
        pos1_e, pos2_e = pos1 + len(word1), pos2 + len(word2)
        gap = pos2 - pos1_e

        # Substitute characters already looked at with whitespace
        edited_text = chr(0) * pos1_e + text[pos1_e:]
        inter_text = text[pos1_e:pos2_e]
        return gap, edited_text, inter_text

    def get_results(self, cut_off=0):
        ret = {}
        for i in range(len(self.tagged)):
            val = self.tagged[i]
            text = val[0]
            locs = val[1]

            merged = self.__merge(locs, text)
            for location in merged:
                if location[0] in ret:
                    ret[location[0]]['texts'].append(text)
                    ret[location[0]]['rels'].append(location[1])
                    ret[location[0]]['count'] += 1
                else:
                    ret[location[0]] = {'texts': [text], 'count': 1, 'rels': [location[1]]}

        return [(k, ret[k]) for k in ret if ret[k]['count'] > cut_off]

    def __merge(self, locs, text, distance=1):
        """Merges all words in locs list that are spaced at most two characters
        apart in text. (i.e. ", "). Assumes locs are in order in text.
        """
        idx = 0
        last_idx = len(locs) - 1
        merged = []
        while idx <= last_idx:
            # loc is a tuple of (location name , relations[])
            loc = locs[idx][0]
            while idx is not last_idx:
                # "Trims" the text after looking at each location to prevent
                # indexing the wrong occurence of the location word if it
                # occurs multiple times in the text.
                gap, text, merge = self.gap_length(locs[idx][0], locs[idx + 1][0], text)
                if gap <= distance:
                    loc += merge
                    idx += 1
                else:
                    break
            merged.append((loc, locs[idx][1]))
            idx += 1
        return merged

    def filter(self):
        pass

    def merge(self):
        pass

    def top(self, ut_off=2):
        pass
