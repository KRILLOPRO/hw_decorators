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


def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger('main.log')
    def hello_world():
        return 'Hello World'

    @logger('main.log')
    def summator(a, b=0):
        return a + b

    @logger('main.log')
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    
    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


def test_2():
    # Тестируем параметризованный декоратор с разными файлами
    
    # Очищаем файлы логов если они существуют
    for log_file in ['log1.log', 'log2.log', 'log3.log']:
        if os.path.exists(log_file):
            os.remove(log_file)

    @logger('log1.log')
    def func_a(x):
        return x * 2

    @logger('log2.log') 
    def func_b(a, b=1):
        return a + b

    @logger('log3.log')
    def func_c():
        return 'test'

    # Вызываем функции
    result_a = func_a(5)
    result_b = func_b(10, b=3)
    result_c = func_c()

    # Проверяем результаты
    assert result_a == 10, 'func_a должна вернуть 10'
    assert result_b == 13, 'func_b должна вернуть 13'
    assert result_c == 'test', 'func_c должна вернуть test'

    # Проверяем, что файлы созданы
    assert os.path.exists('log1.log'), 'log1.log должен существовать'
    assert os.path.exists('log2.log'), 'log2.log должен существовать'
    assert os.path.exists('log3.log'), 'log3.log должен существовать'

    # Проверяем содержимое файлов
    with open('log1.log') as f:
        content1 = f.read()
        assert 'func_a' in content1, 'В log1.log должно быть имя функции func_a'
        assert '5' in content1, 'В log1.log должен быть аргумент 5'
        assert '10' in content1, 'В log1.log должен быть результат 10'

    with open('log2.log') as f:
        content2 = f.read()
        assert 'func_b' in content2, 'В log2.log должно быть имя функции func_b'
        assert '10' in content2, 'В log2.log должен быть аргумент 10'
        assert 'b=3' in content2, 'В log2.log должен быть именованный аргумент b=3'
        assert '13' in content2, 'В log2.log должен быть результат 13'

    with open('log3.log') as f:
        content3 = f.read()
        assert 'func_c' in content3, 'В log3.log должно быть имя функции func_c'
        assert 'test' in content3, 'В log3.log должен быть результат test'

    # Дополнительные вызовы для проверки append режима
    func_a(7)
    func_b(a=2, b=8)

    # Проверяем, что записи добавляются, а не перезаписываются
    with open('log1.log') as f:
        content1_updated = f.read()
        assert content1_updated.count('func_a') == 2, 'В log1.log должно быть 2 записи func_a'

    with open('log2.log') as f:
        content2_updated = f.read()
        assert content2_updated.count('func_b') == 2, 'В log2.log должно быть 2 записи func_b'

    # Очищаем тестовые файлы
    for log_file in ['log1.log', 'log2.log', 'log3.log']:
        if os.path.exists(log_file):
            os.remove(log_file)


if __name__ == '__main__':
    test_1()
    test_2()
    print("Все тесты прошли успешно!")
