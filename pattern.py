
class GoBangPattern(object):
    def __init__(self):
        self.pattern_score = {
            'FIVE': 100000,
            'FOUR': 10000,
            'B_FOUR': 1000,
            'THREE': 100,
            'B_THREE': 10,
            'TWO': 10}
        self.pattern = {}
        self.pattern['FIVE'] = {
            (+1, +1, +1, +1, +1, +1): '',
            (+1, +1, +1, +1, +1, +0): '',
            (+1, +1, +1, +1, +1, -1): ''}
        self.pattern['FOUR'] = {
            (+0, +1, +1, +1, +1, +0): ''}
        self.pattern['B_FOUR'] = {
            (-1, +1, +1, +1, +1, +0): '',
            (+1, +1, +1, +0, +1, +0): '',
            (+1, +1, +1, +0, +1, +1): '',
            (+1, +1, +1, +0, +1, -1): '',
            (+1, +1, +0, +1, +1, +1): '',
            (+1, +1, +0, +1, +1, -1): '',
            (+1, +1, +0, +1, +1, +0): ''}
        self.gen_pattern()
        self.build_inverted()

    def __getitem__(self, key):
        return self.pattern[key]

    def match_pattern(self, pat, tar=+1):
        pat = tuple([x * tar for x in pat])
        if pat in self.inv_pat:
            return self.inv_pat[pat]
        rev_pat = self.reverse(pat)
        if rev_pat in self.inv_pat:
            return self.inv_pat[rev_pat]

    def undo(self, pat):
        for i in range(len(pat)):
            if pat[i] == +1:
                t = list(pat)
                t[i] = 0
                yield tuple(t)

    def reverse(self, pat):
        return tuple(list(pat)[::-1])

    def gen_pattern(self):
        self.pattern['THREE'] = {}
        self.pattern['B_THREE'] = {}
        self.pattern['TWO'] = {}

        for pat in self['FOUR']:
            for new_pat in self.undo(pat):
                if self.reverse(new_pat) not in self.pattern['THREE']:
                    self.pattern['THREE'][new_pat] = ''
        for pat in self['B_FOUR']:
            for new_pat in self.undo(pat):
                if self.reverse(new_pat) not in self.pattern['B_THREE']:
                    self.pattern['B_THREE'][new_pat] = ''
        for pat in self['THREE']:
            for new_pat in self.undo(pat):
                if self.reverse(new_pat) not in self.pattern['TWO']:
                    self.pattern['TWO'][new_pat] = ''
        for pat in self['B_THREE']:
            for new_pat in self.undo(pat):
                if self.reverse(new_pat) not in self.pattern['TWO']:
                    self.pattern['TWO'][new_pat] = ''

    def build_inverted(self):
        self.inv_pat = {}
        for cat in self.pattern:
            for pat in self.pattern[cat]:
                rev_pat = self.reverse(pat)
                reg_pat = rev_pat if rev_pat in self.inv_pat else pat
                if reg_pat not in self.inv_pat or self.pattern_score[cat] > self.inv_pat[reg_pat]:
                    self.inv_pat[reg_pat] = self.pattern_score[cat]
        print self.inv_pat


p = GoBangPattern()
