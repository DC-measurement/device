def print_hand(hand, name='ゲスト'):
    print(name + 'は' + hand + 'を出しました')

print('じゃんけんをはじめます')

# inputを用いて入力を受け取り、変数player_nameに代入してください
player_name = input('名前を入力してください：')

# 変数player_nameの値によって関数print_handの呼び出し方を変更してください
if player_name == '':
    print_hand('グー')
else:
    print_hand('グー',player_name)