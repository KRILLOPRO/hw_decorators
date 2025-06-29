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


# Очищаем общий лог файл
if os.path.exists('all_tests.log'):
    os.remove('all_tests.log')


@logger('all_tests.log')
def run_all_tests():
    """Запускает все тесты итераторов с логированием"""
    
    print("Запуск всех тестов итераторов...")
    
    # Импортируем и запускаем test_1
    from test_1 import test_1
    print("Выполнение test_1...")
    test_1()
    
    # Импортируем и запускаем test_2  
    from test_2 import test_2
    print("Выполнение test_2...")
    test_2()
    
    # Импортируем и запускаем test_3
    from test_3 import test_3
    print("Выполнение test_3...")
    test_3()
    
    # Импортируем и запускаем test_4
    from test_4 import test_4
    print("Выполнение test_4...")
    test_4()
    
    print("Все тесты успешно выполнены!")
    return "Все тесты пройдены"


if __name__ == '__main__':
    result = run_all_tests()
    print(f"\nРезультат: {result}")
    print("Проверьте файл all_tests.log для просмотра логов выполнения") 