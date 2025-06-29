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
        self.outer_index = 0  # индекс текущего внешнего списка
        self.inner_index = 0  # индекс текущего элемента во внутреннем списке

    def __iter__(self):
        return self

    def __next__(self):
        # Пропускаем пустые списки
        while self.outer_index < len(self.list_of_list):
            current_list = self.list_of_list[self.outer_index]
            
            # Если текущий внутренний список не пустой и есть элементы для возврата
            if self.inner_index < len(current_list):
                item = current_list[self.inner_index]
                self.inner_index += 1
                return item
            else:
                # Переходим к следующему списку
                self.outer_index += 1
                self.inner_index = 0
        
        # Все списки пройдены
        raise StopIteration


@logger('test_1.log')
def test_1():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_1()
    print("test_1 выполнен успешно! Проверьте файл test_1.log")