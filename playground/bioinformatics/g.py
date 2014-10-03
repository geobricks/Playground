def pattern_count(genome, pattern):
    count = 0
    for i in range(0, len(genome)-len(pattern)):
        if genome[i:i+len(pattern)] == pattern:
            count += 1
    return count


def frequent_words(genome, k):
    frequent_patterns = []
    count = {}
    maximum = 0
    for i in range(0, len(genome) - k):
        count[i] = pattern_count(genome, genome[i:i+k])
        if count[i] > maximum:
            maximum = count[i]
    for i in range(0, len(genome) - k):
        if count[i] == maximum and genome[i:i+k] not in frequent_patterns:
            frequent_patterns.append(genome[i:i+k])
    return frequent_patterns


def reverse_complement(genome):
    out = ''
    mappings = {
        'A': 'T',
        'T': 'A',
        'C': 'G',
        'G': 'C'
    }
    for i in reversed(genome):
        out += mappings[i]
    return out


def pattern_matching(pattern, genome):
    indices = []
    for i in range(0, len(genome)-len(pattern)):
        if genome[i:i+len(pattern)] == pattern:
            indices.append(str(i))
    return indices


def find_clump(genome, k, l, t):
    clumps = []
    words_buffer = []
    for i in range(0, len(genome)-l):
        sub_genome = genome[i:i+l]
        words = frequent_words(sub_genome, k)
        # if words not in words_buffer:
        #     words_buffer.append(words)
        for word in words:
            p_count = pattern_count(sub_genome, word)
            if p_count == t and word not in clumps:
                clumps.append(word)
                print 'Added: ' + word
    print 'OUTPUT?'
    print len(clumps)
    return ' '.join(clumps)

pattern = 'CTTGATCAT'
genome = open('/home/kalimaha/Desktop/colera.txt', 'r').read()
# genome = open('/home/kalimaha/Desktop/petrophila.txt', 'r').read()
# genome = 'gatcagcataagggtccctgcaatgcatgacaagcctgcagttgttttac'
# print pattern_count(genome, pattern)
# print frequent_words(genome, 9)
# print reverse_complement(genome)
# indices = pattern_matching(pattern, genome)
# print ' '.join(indices)
print find_clump(genome, 9, 500, 3)