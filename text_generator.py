from nltk.tokenize import regexp_tokenize as rt
from collections import defaultdict
from collections import Counter
import random


def get_file_content(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        return file.read()


# returns a list of n-grams where the tail is always a single word and head is everything else that precedes it
def get_n_grams(tokens, n):
    n_grams_list = []
    for i, word in enumerate(tokens[:-n+1]):
        head = word
        for j in range(1, n - 1):
            head += ' ' + tokens[i + j]
        # IDE suggestion: list(head) is not correct in this case
        n_gram = [head]
        n_gram.append(tokens[i + n - 1])
        n_grams_list.append(n_gram)
    return n_grams_list


# returns a dictionary with the n-gram heads as keys and the values are all possible tails from n-grams-list
def all_occurring_tails(n_grams_list):
    all_occurring_tails_dict = defaultdict(list)
    for n_gram in n_grams_list:
        all_occurring_tails_dict[n_gram[0]].append(n_gram[1])

    return all_occurring_tails_dict


# returns a modified dictionary of all_occurring_tails function where tails for each head are stored as a Counter object
def all_occurring_tails_counted(all_tails_dict):
    for head in all_tails_dict:
        counter_object = Counter(all_tails_dict[head])
        all_tails_dict[head] = counter_object

    return all_tails_dict


# returns a head that starts with a capital letter to be used after a punctuation mark. No matter how long the head is,
# it will not return a head whose first word ends in a punctuation mark
# Uses Counter objects criteria (from all_occurring_tails_counted) as weight for tail picking
def random_capital_letter_head(all_tails_dict, weight=None):
    while True:
        head = random.choices(list(all_tails_dict), weight)

        # random.choices() returns a list which is why head[0] is needed to give us a string to work with
        if head[0][0].isupper() and head[0].split()[0][-1] not in '.!?':
            return head
        # if there is no tail that fits based on the weight criteria, it will pick one with no regard for the weight
        if len(list(all_tails_dict)) == 1:
            head = random.choices(list(all_tails_dict))
            return head


# Generates a pseudo sentence of at least 5 words
# Works for trigams
def pseudo_sentence_generator(all_tails_dict):
    pseudo_sentence = ""

    head = random_capital_letter_head(all_tails_dict)[0]

    while True:
        pseudo_sentence += ' ' + head

        # takes the last 2 words as the trigram head that it uses to search for the next word
        head = ' '.join(pseudo_sentence.split()[-2:])
        if head[-1] in '.!?':
            # in case of a punctuation mark before 5 words are reached it will start a new sentence with a capital word
            if len(pseudo_sentence.split()) >= 5:
                break
            head = random_capital_letter_head(all_tails_dict[head], all_tails_dict[head].values())[0]
        else:
            head = random.choices(list(all_tails_dict[head]), all_tails_dict[head].values())[0]

    return pseudo_sentence


def main():
    file_name = input()
    corpus = get_file_content(file_name)

    tokens = rt(corpus, r"[^\s]+")
    trigrams = get_n_grams(tokens, 3)

    all_tails_counted = all_occurring_tails_counted(all_occurring_tails(trigrams))

    for _ in range(10):
        print(pseudo_sentence_generator(all_tails_counted))

    """
    # Check all possible tails that occur for a head in an n_gram list
    
    while True:
        head = input()
        if head == 'exit':
            break
        try:
            tails = all_tails_counted[head]
            print("Head:", head)
            if not tails:
                raise KeyError

        except ValueError:
            print("Type Error. Please input an integer.")
        except IndexError:
            print("Index Error. Please input an integer that is in the range of the corpus.")
        except KeyError:
            print("Key Error. The requested word is not in the model. Please input another word.")
        else:
            for tail in tails:
                print("Tail:", tail, " " * (9 - len(tail)), "Count:", tails[tail])
        finally:
            print()
        """


if __name__ == '__main__':
    main()
