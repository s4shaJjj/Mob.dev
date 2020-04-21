class Encoder:

    def __init__(self, filename, newfilename, word_to_code):
        self.key = [['с', 'р'], ['c', 'p']]
        self.rusalph = [chr(i) for i in range(ord('а'), ord('я')+1)] + \
                                      [chr(i) for i in range(ord('А'), ord('Я') + 1)]

        self.filename = filename
        self.newfilename = newfilename
        self.word_to_code = word_to_code

        f = open(filename, 'r', encoding='utf-8')
        self.text = f.readlines()

    def check_ru(self, word):
        for c in word:
            if c in self.rusalph or c in ['\n']:
                continue
            else:
                return False
        return True

    def check_ru_en(self,word):
        k = 0
        for c in word:
            if c in self.rusalph or c in ['\n']:
                continue
            else:
                if c in self.key[1]:
                    k += 1
                else:
                    return False
        if k == 1:
            return True
        return False

    # return word in binary
    def str_to_bin(word):
        s = []
        for letter in word:
            s.append((bin(ord(letter))[2:]))

        ret = ""
        for code in s:
            ret += str(code)
        return ret

    # return char by bin code
    def bin_to_str(code):
        return chr(int(code, 2))

    # Let c(ru) -> c(en) it's 0b
    # Let p(ru) -> p(en) it's 1b
    def EncodeByReplace(self):
        codes = Encoder.str_to_bin(self.word_to_code)
        i = 0
        with open(self.newfilename,'w', encoding='utf-8') as file:
            for line in self.text:
                if (i == len(codes)):
                    file.write(line)
                    continue
                new_line = ''
                if i != len(codes):
                    words = line.split(' ')
                    for word in words:
                        if (i == len(codes)):
                            if new_line == '':
                                new_line += word
                            else:
                                new_line += ' ' + word
                            continue
                        new_word = ''
                        for j in range(0, 2):
                            if word.find(self.key[0][j]) >= 0 and \
                                    str(j) == codes[i] and \
                                    self.check_ru(word):
                                new_word = word.replace(self.key[0][j], self.key[1][j], 1)
                                i += 1
                                break


                        if new_line == '' :
                            if new_word == '':
                                new_line += word
                            else:
                                new_line += new_word
                        else:
                            if new_word == '':
                                new_line += ' ' + word
                            else:
                                new_line += ' ' + new_word

                if (new_line[len(new_line) - 1] != '\n'):
                    new_line += '\n'
                file.write(new_line)

    def DecodeByReplace(self):
        self.text = open(self.newfilename, 'r', encoding='utf-8').readlines()
        bits = ""

        for line in self.text:
            words = line.split(' ')
            for word in words:
                if ((word.find(self.key[1][0]) >= 0 or word.find(self.key[1][1]) >= 0)
                        and self.check_ru_en(word)):
                    if word.find(self.key[1][0]) >= 0:
                        #log
                        #print('find 0 in ' + word)
                        bits += '0'
                    else:
                        bits += '1'
                        # log
                        #print('find 1 in ' + word)
        str =""
        if len(bits) == 11:
            return Encoder.bin_to_str(bits)

        for i in range(len(bits) // 11):
            str += Encoder.bin_to_str(bits[i * 11 : i * 11 +11])
        return str

    ##################################

    def letter_exist(self,line):
        for i in line:
            if i in self.rusalph:
                return True
        return False


    def format_text(self):
        for i in range(len(self.text)):
            if (not self.letter_exist(self.text[i])):
                continue
            c = len(self.text[i]) - 1
            while self.text[i][c] in [' ', '\n', '\t']:
                c -= 1
            self.text[i] = self.text[i][0:c + 1] + '\n'

    def EncodeBySpaces(self):
        codes = Encoder.str_to_bin(self.word_to_code)
        self.format_text()

        i = 0
        c = 0
        while c < len(codes):
            if self.letter_exist(self.text[i]):
                if codes[c] == '0':
                    self.text[i] = self.text[i][0: len(self.text[i]) - 1] + ' ' + '\n'
                    #log
                    print('bit 0 on the ' + str(i) + 'th line')
                else:
                    self.text[i] = self.text[i][0: len(self.text[i]) - 1] + '  ' + '\n'
                    print('bit 1 on the ' + str(i) + 'th line')
                c += 1
            i += 1

        with open(self.newfilename,'w', encoding='utf-8') as file:
            for line in self.text:
                file.write(line)

    def DecodebySapce(self):
        f = open(self.newfilename, 'r', encoding='utf-8')
        self.text = f.readlines()

        #log
        s = 0

        bits = ""
        for line in self.text:
            if self.letter_exist(line):
                spaces = line[len(line) - 3:]
                if line.find('  ') >= 0:
                    bits += '1'
                    print('found 1 on the ' + str(s) + 'th line')
                elif line.find(' ') >= 0:
                    bits += '0'
                    print('found 0 on the ' + str(s) + 'th line')
            #log
            s += 1
        string =""
        if len(bits) == 11:
            return Encoder.bin_to_str(bits)

        for i in range(len(bits) // 11):
            string += Encoder.bin_to_str(bits[i * 11 : i * 11 + 11])
        return string

    #################

    #let \0   :  0
    #let \2   :  1
    def EncodeByNonPrintble(self):
        codes = Encoder.str_to_bin(self.word_to_code)

        c = 0

        for line in range(len(self.text)):
            if c == len(codes):
                break
            lenght = len(self.text[line])
            char = 0
            while char < lenght:
                if self.text[line][char] == ' ':
                    if codes[c] == '0':
                        self.text[line] = self.text[line][0:char] + '\0' + self.text[line][char + 1:]
                    else:
                        self.text[line] = self.text[line][0:char] + '\2' + self.text[line][char + 1:]
                    c += 1
                    lenght = len(self.text[line])
                    if c == len(codes):
                        break
                char += 1

        with open(self.newfilename,'w', encoding='utf-8') as file:
            for i in range(len(self.text)):
                file.write(self.text[i])

    def DecodeByNonPrintble(self):
        f = open(self.newfilename, 'r', encoding='utf-8')
        self.text = f.readlines()

        bits = ''
        for line in range(len(self.text)):
            for char in range(len(self.text[line])):
                if self.text[line][char] == '\0':
                    bits += '0'
                if self.text[line][char] == '\2':
                    bits += '1'

        string = ''
        if len(bits) == 11:
            return Encoder.bin_to_str(bits)

        for i in range(len(bits) // 11):
            string += Encoder.bin_to_str(bits[i * 11 : i * 11 + 11])
        return string


coder = Encoder('book.txt', 'book_e.txt', 'ТекстТЕкст')
coder.EncodeByReplace()
print(coder.DecodeByReplace())


