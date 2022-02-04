from itertools import count
from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
import datetime

app = Flask(__name__)

column_names = ['date', 'player','score']
df = pd.read_csv('./csv/players.csv')
players = df.to_numpy().tolist()


def saveCSV(array):
    # 配列からDataframeへ
    players_df = pd.DataFrame(array, columns=column_names)
    players_df.to_csv('./csv/players.csv', index=False)

# todo一覧画面

@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('main.html', players=players)
    else:
        if request.form.get('reset') != None:  # reset
            i=0
            for _ in players:
                players[i][2] = 0
                i+=1
            saveCSV(players)
            return redirect(url_for('main'))
        # 完了ボタンを押した時の動作
        elif request.form.get('done') != None:  # done
            done_index = int(request.form.get('done'))  # done
            del players[done_index]
            saveCSV(players)
            return redirect(url_for('main'))
            # return render_template('main.html', players=players) # 課題に載っていた内容
        elif request.form.get('count') != None:  # count
            count_index = int(request.form.get('count'))  # count
            players[count_index][2] += 1
            saveCSV(players)
            return redirect(url_for('main'))
        elif request.form.get('sub') != None:  # sub
            count_index = int(request.form.get('sub'))  # sub
            players[count_index][2] -= 1
            saveCSV(players)
            return redirect(url_for('main'))
        # 編集画面でタスクを編集した時の動作
        elif request.form.get('updated_player') != None:  # updated_player
            updated_player = request.form.get('updated_player')  # updated_player
            updated_index = request.form.get('updated_index')  # updated_index
            score_based = players[int(updated_index)][2]
            date_added = datetime.datetime.now().date()
            player = [date_added, updated_player,score_based]
            players[int(updated_index)] = player
            saveCSV(players)
            return render_template('main.html', players=players)


# Playerの新規作成
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        # HTMLのテキストボックスの情報
        added_player = request.form.get('new_player')  # new_player
        date_added = datetime.datetime.now().date()
        score_initialized = 0
        player = [date_added, added_player, score_initialized]
        # 配列に追加
        players.append(player)
        saveCSV(players)
        return render_template('add.html')


# Playerを更新
@app.route('/update', methods=['POST'])
def update_init():
    update_index = int(request.form.get('update'))  # update
    return render_template('update.html', player_title=players[update_index][1], player_index=update_index)


if __name__ == '__main__':
    app.run(debug=True)
