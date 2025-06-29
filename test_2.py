import types
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


@logger('test_2_generator.log')
def flat_generator(list_of_lists):
    for inner_list in list_of_lists:
        for item in inner_list:
            yield item


@logger('test_2.log')
def test_2():

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):

        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)


if __name__ == '__main__':
    test_2()
    print("test_2 выполнен успешно! Проверьте файлы test_2.log и test_2_generator.log")
    