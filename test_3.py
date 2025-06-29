import os
import datetime


def logger(log_file_path):
    def decorator(old_function):
        def new_function(*args, **kwargs):
            # Вызываем оригинальную функцию и получаем результат
            result = old_function(*args, **kwargs)
            
            # Получаем текущее время
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Формируем строку с аргументами
            args_str = ', '.join([str(arg) for arg in args])
            kwargs_str = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
            
            # Объединяем аргументы
            all_args = []
            if args_str:
                all_args.append(args_str)
            if kwargs_str:
                all_args.append(kwargs_str)
            arguments = ', '.join(all_args) if all_args else ''
            
            # Формируем лог запись
            log_entry = f"{timestamp} - Function: {old_function.__name__}, Args: ({arguments}), Result: {result}\n"
            
            # Записываем в файл с переданным путем
            with open(log_file_path, 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry)
            
            return result

        return new_function
    return decorator


class FlatIterator:

    def __init__(self, list_of_list):
        self.list_of_list = list_of_list

    def __iter__(self):
        # Инициализируем стек с элементами в обратном порядке
        # чтобы сохранить правильный порядок обхода
        self.stack = list(reversed(self.list_of_list))
        return self
    
    def __next__(self):
        while self.stack:
            # Извлекаем элемент из стека
            current = self.stack.pop()
            
            # Если элемент является списком, добавляем его содержимое в стек
            if isinstance(current, list):
                # Добавляем элементы в обратном порядке для сохранения порядка обхода
                self.stack.extend(reversed(current))
            else:
                # Если элемент не список, возвращаем его
                return current
        
        # Стек пуст, все элементы обработаны
        raise StopIteration


@logger('test_3.log')
def test_3():

    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']


if __name__ == '__main__':
    test_3()
    print("test_3 выполнен успешно! Проверьте файл test_3.log")