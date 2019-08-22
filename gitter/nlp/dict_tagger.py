from ruamel.yaml import YAML


class DictionaryTagger(object):
    def __init__(self, dictionary_paths):
        yaml = YAML()
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries_list = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionaries = {}
        self.max_key_size = 0
        for curr_dict in dictionaries_list:
            for key in curr_dict:
                if key in self.dictionaries:
                    self.dictionaries[key].extend(curr_dict[key])
                else:
                    self.dictionaries[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, pos_tagged_sentences):
        return (
            [self.tag_sentence(sentence) for sentence in pos_tagged_sentences])

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentences = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N)  # avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join(
                    [word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join(
                    [word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionaries:
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionaries[literal]]
                    tagged_expression = (
                        expression_form, expression_lemma, taggings)
                    # if the tagged literal is a single token,
                    # conserve its previous taggings:
                    if is_single_token:
                        original_token_taggings = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_taggings)
                    tag_sentences.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentences.append(sentence[i])
                i += 1
        return tag_sentences
