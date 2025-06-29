import os
import datetime


def logger(log_file_path):
    """
    Параметризованный декоратор для логирования вызовов функций.
    
    Записывает в указанный файл:
    - Дату и время вызова функции
    - Имя функции
    - Аргументы (позиционные и именованные)
    - Возвращаемое значение
    
    Args:
        log_file_path (str): Путь к файлу для записи логов
    """
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


# Очищаем демонстрационный лог файл
if os.path.exists('demo.log'):
    os.remove('demo.log')


@logger('demo.log')
def математические_операции(a, b, операция='сложение'):
    """Демонстрирует логирование функции с различными типами аргументов"""
    if операция == 'сложение':
        return a + b
    elif операция == 'умножение':
        return a * b
    elif операция == 'деление':
        return a / b if b != 0 else "Деление на ноль!"
    else:
        return "Неизвестная операция"


@logger('demo.log')
def работа_со_списками(список, индекс=0):
    """Демонстрирует логирование с сложными структурами данных"""
    if индекс < len(список):
        return список[индекс]
    else:
        return "Индекс вне диапазона"


@logger('demo.log')
def генератор_чисел(до_числа):
    """Демонстрирует логирование функции-генератора"""
    for i in range(до_числа):
        yield i * 2


@logger('demo.log')
def обработка_ошибок(значение):
    """Демонстрирует логирование функции с обработкой ошибок"""
    try:
        return 100 / значение
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except Exception as e:
        return f"Неожиданная ошибка: {e}"


@logger('demo.log')
def демонстрация_логгера():
    """Главная функция демонстрации возможностей логгера"""
    
    print("🔍 ДЕМОНСТРАЦИЯ РАБОТЫ ЛОГГЕРА")
    print("=" * 50)
    
    print("\n1. Математические операции:")
    print(f"   5 + 3 = {математические_операции(5, 3)}")
    print(f"   4 * 7 = {математические_операции(4, 7, операция='умножение')}")
    print(f"   15 / 3 = {математические_операции(15, 3, операция='деление')}")
    
    print("\n2. Работа со списками:")
    тестовый_список = ['python', 'javascript', 'go', 'rust']
    print(f"   Элемент по индексу 0: {работа_со_списками(тестовый_список)}")
    print(f"   Элемент по индексу 2: {работа_со_списками(тестовый_список, индекс=2)}")
    print(f"   Элемент по индексу 10: {работа_со_списками(тестовый_список, индекс=10)}")
    
    print("\n3. Генераторы:")
    gen = генератор_чисел(5)
    print(f"   Генератор создан: {gen}")
    print(f"   Список из генератора: {list(генератор_чисел(3))}")
    
    print("\n4. Обработка ошибок:")
    print(f"   100 / 5 = {обработка_ошибок(5)}")
    print(f"   100 / 0 = {обработка_ошибок(0)}")
    
    print("\n✅ Демонстрация завершена!")
    return "Демонстрация успешно выполнена"


if __name__ == '__main__':
    результат = демонстрация_логгера()
    
    print(f"\n📄 РЕЗУЛЬТАТ: {результат}")
    print("\n📋 СОДЕРЖИМОЕ ЛОГА:")
    print("=" * 50)
    
    # Читаем и выводим содержимое лога
    with open('demo.log', 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            print(f"{line_num:2d}. {line.strip()}")
    
    print("\n" + "=" * 50)
    print("🎉 Логгер успешно применён к коду из папки hw_iterators!") 