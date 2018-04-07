import random

def draw(n):
    if type(n) is not int:
        return None
    prob = random.random()
    cards = []
    shape = ['Spade ','Club ','Heart ','Diamond ']
    number = ['A','1','2','3','4','5','6','7','8','9','10','J','Q','K']
    cards = cards+ ['Joker']
    for i in shape:
        for j in number:
            cards.append(i+j)
    cards = cards*9
    cards = cards + ['2차원의 함정 속으로','함정 속으로','나락의 함정 속으로', '황산의 함정 속으로', '큰 함정 속으로', '교활한 함정 속으로', '절망의 함정 속으로','똥 묻은 칼','용암 광전사','얼음 광전사','암용 광전사','어둠 광전사']
    random.shuffle(cards)
    string = ''
    for i in range(n):
        string=string+' '+cards[i]
    return string
