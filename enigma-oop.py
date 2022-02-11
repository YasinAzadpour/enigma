from random import shuffle
DIGITS = '0123456789'
CHARS = 'abcdefghijklmnopqrstuvwxyz'


class Enigma:
    HEADER = '''
            @@@@@@@@  @@@  @@@  @@@   @@@@@@@@  @@@@@@@@@@    @@@@@@
            @@@@@@@@  @@@@ @@@  @@@  @@@@@@@@@  @@@@@@@@@@@  @@@@@@@@
            @@!       @@!@!@@@  @@!  !@@        @@! @@! @@!  @@!  @@@
            !@!       !@!!@!@!  !@!  !@!        !@! !@! !@!  !@!  @!@
            @!!!:!    @!@ !!@!  !!@  !@! @!@!@  @!! !!@ @!@  @!@!@!@!
            !!!!!:    !@!  !!!  !!!  !!! !!@!!  !@!   ! !@!  !!!@!!!!
            !!:       !!:  !!!  !!:  :!!   !!:  !!:     !!:  !!:  !!!
            :!:       :!:  !:!  :!:  :!:   !::  :!:     :!:  :!:  !:!
            :: ::::   ::   ::   ::   ::: ::::  :::     ::   ::   :::
            : :: ::   ::    :   :     :: :: :    :      :     :   : :
      '''

    def __init__(self):
        self.initial_data = [None, None]
        self.arotors = []
        self.drotors = []
        self.cypher = ''
        self.state = 0
    
    def flash(self):
        self.arotors = self.initial_data[0]
        self.drotors = self.initial_data[1]
        self.state = 0


    def set_rotors(self, new_rotors):
        self.arotors = self._validate(new_rotors[0],CHARS)
        self.drotors = self._validate(new_rotors[1], DIGITS)
        self.initial_data = [self.arotors.copy(), self.drotors.copy()] 


    def randomly(self):
        self.arotors.clear()
        self.drotors.clear()
        for _ in range(3):
            new_drotor = list(DIGITS)
            shuffle(new_drotor)
            self.drotors.append("".join(new_drotor))

            new_arotor = list(CHARS)
            shuffle(new_arotor)
            self.arotors.append("".join(new_arotor))

        self.initial_data = [self.arotors.copy(), self.drotors.copy()] 

    def _validate(self, rotors, refrence):
        my_list = []
        for i in range(3):
            assert set(rotors[i]) == set(refrence)
            my_list.append(rotors[i])

        assert len(rotors) == 3
        return my_list

    def __str__(self):
        header = f'{"1":26} {"2":26} {"3":26}'
        ascii_str = f'{self.arotors[0]} {self.arotors[1]} {self.arotors[2]}'
        digits_str = f'{self.drotors[0]:26} {self.drotors[1]:26} {self.drotors[2]:26}'
        return f'{header}\n{ascii_str}\n{digits_str}'

    def _reflector(self, refrence, char):
        return refrence[len(refrence)-(refrence.find(char)+1)]

    def _rotate_one_router(self,rotor):
        return rotor[1:] + rotor[0]

    def _rotate_routers(self, rotors):
        rotors[0] = self._rotate_one_router(rotors[0])
        
        if self.state % 26:
            rotors[1] = self._rotate_one_router(rotors[1])
            
        if self.state % (26*26):
            rotors[2] = self._rotate_one_router(rotors[2])

    def _rotor_one_char(self, c):
        try:    
            self.state += 1
            if c in DIGITS:
                rotors = self.drotors
                refrence = DIGITS

            elif c in CHARS:
                rotors = self.arotors
                refrence = CHARS

            else:
                return ''

            char = rotors[0][refrence.find(c)]
            char = rotors[1][refrence.find(char)]
            char = rotors[2][refrence.find(char)]
            char = self._reflector(refrence, char)
            char = refrence[rotors[2].find(char)]
            char = refrence[rotors[1].find(char)]
            char = refrence[rotors[0].find(char)]
            self._rotate_routers(rotors)

            return char
        except:
            raise AssertionError("Please set rotors")

    def encrypt_text(self, message):
        
        text = ''
        for c in message.lower():
            text += self._rotor_one_char(c)

        return text


if __name__ == "__main__":
    import sys
    m = Enigma()
    m.randomly()
    print(m.encrypt_text(sys.argv[1]))
