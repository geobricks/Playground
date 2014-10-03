import time



def pattern_count(text, pattern):
    count = 0
    for i in range(0, len(text)-len(pattern)):
        if text[i:i+len(pattern)] == pattern:
            count += 1
            # print str(i+1) + ' ' + text[i:i+len(pattern)] + ' VS ' + pattern + ' ' + str(text[i:i+len(pattern)] == pattern)
    return count


def frequent_patterns(text, k):
    fps = []
    count = []
    for i in range(0, len(text) - k):
        pattern = text[i:i+k]
        count.append(pattern_count(text, pattern))
        maxCount = max(count)

    for i in range(0, len(text) - k):
        if count[i] == maxCount:
            if text[i:i+k] not in fps:
                fps.append(text[i:i+k])
    return sorted(fps, reverse=False)


def pattern_to_number(pattern):
    if len(pattern) < 1:
        return 0
    symbol = pattern[len(pattern)-1:]
    pattern_minus_last = pattern[:-1]
    return (4 * pattern_to_number(pattern_minus_last)) + symbol_to_number(symbol)


def symbol_to_number(symbol):
    mapping = {
        'A': 0,
        'C': 1,
        'G': 2,
        'T': 3
    }
    return mapping[symbol.upper()]


def number_to_symbol(number):
    mapping = {
        0: 'A',
        1: 'C',
        2: 'G',
        3: 'T'
    }
    return mapping[number]


def number_to_pattern(index, k):
    if k == 1:
        return number_to_symbol(index)
    prefix_index = index / 4
    reminder = index % 4
    prefix_pattern = number_to_pattern(prefix_index, k-1)
    symbol = number_to_symbol(reminder)
    return prefix_pattern + symbol


def computing_frequencies(text, k):
    freq_array = []
    for i in range(0, (pow(4, k))):
        freq_array.append(0)

    for i in range(0, (len(text) - k) + 1):
        pattern = text[i:i+k]
        j = pattern_to_number(pattern)
        freq_array[j] = freq_array[j] + 1
    return freq_array


def faster_frequent_words(text, k):
    fps = []
    fa = computing_frequencies(text, k)
    maxCount = max(fa)
    for i in range(0, (pow(4, k))):
        if fa[i] == maxCount:
            pattern = number_to_pattern(i, k)
            if pattern not in fps:
                fps.append(pattern)
    return fps


def reverse_complemnt_problem(pattern):
    map = {
        "A": "T",
        "C": "G",
        "G": "C",
        "T": "A"
    }
    output = ""
    for p in reversed(pattern):
        output += map[p]
    return output


def pattern_matching_problem(pattern, genome):
    positions = []
    for i in range(0, (len(genome) - len(pattern) +1)):
        if genome[i:i+len(pattern)] == pattern:
            positions.append(str(i))
    return " ".join(positions)



pattern = 'CTTGATCAT'
genome = open('/home/vortex/Downloads/Thermotoga-petrophila.txt', 'r').read()
#genome = 'CGGACTCGACAGATGTGAAGAACGACAATGTGAAGACTCGACACGACAGAGTGAAGAGAAGAGGAAACATTGTAA'
# print pattern_count(text, pattern)

# print int(round(time.time() * 1000))
# print frequent_patterns(text, 7)
# print int(round(time.time() * 1000))
# # print pattern_to_number('ATGCAA')
# # print number_to_pattern(5437, 8)
# print faster_frequent_words(text, 7)
# print int(round(time.time() * 1000))

#print reverse_complemnt_problem(text)
print "here"
print faster_frequent_words(genome, 9)
print "end"
#print pattern_matching_problem(pattern, genome)



















