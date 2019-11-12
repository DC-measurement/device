import utils

print('じゃんけんをはじめます')
player_name = input('名前を入力してください：')
print('何を出しますか？（0: グー, 1: チョキ, 2: パー）')
player_hand = int(input('数字で入力してください：'))

# utilsモジュール内の関数validateを呼び出してください
if utils.validate(player_hand):
    computer_hand = 1

    if player_name == '':
        # utilsモジュール内の関数print_handを呼び出してください
        utils.print_hand(player_hand)
    else:
        # utilsモジュール内の関数print_handを呼び出してください
        utils.print_hand(player_hand, player_name)

    # utilsモジュール内の関数print_handを呼び出してください
    utils.print_hand(computer_hand, 'コンピュータ')
    
    # utilsモジュール内の関数judgeを呼び出してください
    utils.result = utils.judge(player_hand, computer_hand)
    print('結果は' + utils.result + 'でした')
else:
    print('正しい数値を入力してください')
