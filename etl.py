from datetime import datetime
from typing import List
import os
import conf


def transform_data(users, todos):
    for i in users:
        d = {}
        try:
            if checking_the_file(i['username']) is True:
                continue
            else:
                d['first_line'] = f"Отчет для {i['company']['name']}."
                d['second_line'] = f"{i['name']} <{i['email']}> {datetime.now()}"
                d['third_line'] = f"Всего задач: {transform_line_three(todos, i['id'])} \n"
                line_five = transform_line_five(todos, i['id'])
                d['fifth_line'] = f"Завершённые задачи ({line_five[0]}): \n{line_five[1]}\n" \
                                  f"Оставшиеся задачи ({line_five[2]}): \n{line_five[3]}"
                with open(f"tasks/{i['username']}.txt", 'w') as f:
                    for j in d:
                        print(f"Writing to file...")
                        f.write(d.get(j) + '\n')
        except:
            print("Error in data transform")


def checking_the_file(file) -> bool:
    cur_time = datetime.now()
    if os.path.isfile(f"tasks/{file}.txt"):
        os.rename(f"tasks/{file}.txt", f"tasks/old_{file}_{cur_time.date()}T{cur_time.hour}:"
                                       f"{cur_time.minute}.txt")
        return True
    return False


def transform_line_three(todos, users_id) -> int:
    counter = 0
    for i in todos:
        try:
            if i['userId'] and i['userId'] == users_id and i['title']:
                counter = 1
            if i['userId'] > users_id:
                break
        except:
            print("Not found userId")
    print(f"Total tasks {counter}")
    return counter


def transform_line_five(todos, users_id) -> List:
    counter_t, counter_f = 0, 0
    completed, not_completed = '', ''
    for i in todos:
        try:
            if i['userId'] and i['userId'] == users_id and i['title']:
                if i['completed'] == True:
                    counter_t += 1
                    if len(i['title']) > 48:
                        completed += i['title'][:48] + '...' + '\n'
                    completed += i['title'] + '\n'
                else:
                    counter_f += 1
                    if len(i['title']) > 48:
                        not_completed += i['title'][:48] + '...' + '\n'
                    not_completed += i['title'] + '\n'
            if i['userId'] > users_id:
                break
        except:
            print("Not found userId or title")
    print(f"The amount of tasks solved {counter_t}" '\n'
          f"The amount of tasks unsolved {counter_f}")

    return [counter_t, completed, counter_f, not_completed]


if __name__ == '__main__':
    if not os.path.exists('tasks'):
        os.mkdir('tasks')

    print("Transform data...")
    transform_data(conf.users_data, conf.todo_data)

# one = f"Отчет для 'название компании из api user'."
# two = f"'name из api users' '<email из api users>' 'время составления отчета(datetime.now)'"
# three = f"Всего задач: 'int'"  # проверка кол-во title и completed, общее количество задач
# four = 'пустая строка'
# five = f"Завершённые задачи (N): + '\n' список завершенных задач"  # completed true
#        f"Оставшиеся задачи (M): + '\n' список оставшихся задач"  # completed false (max(48 items...)
