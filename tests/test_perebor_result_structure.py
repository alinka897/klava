"""
Тест для функции perebor: структура возвращаемых данных.
"""

from structs import Layout

def test_perebor_result_structure():
    layout = Layout(name="test")
    
    result = layout.perebor("барашек")
    
    if result is not None:
        convs, chl_count, chr_count = result
        
        # convs: список из 3 чисел [bad, ok, good]
        assert isinstance(convs, list), f"convs должен быть list, получил {type(convs)}"
        assert len(convs) == 3, f"convs должен иметь длину 3, получил {len(convs)}"
        assert all(isinstance(x, int) for x in convs), "Все элементы convs должны быть int"
        
        # chl_count: словарь для левой руки
        assert isinstance(chl_count, dict), f"chl_count должен быть dict, получил {type(chl_count)}"
        assert set(chl_count.keys()) == {'ch2', 'ch3', 'ch4', 'ch5'}
        
        # chr_count: словарь для правой руки
        assert isinstance(chr_count, dict), f"chr_count должен быть dict, получил {type(chr_count)}"
        assert set(chr_count.keys()) == {'ch2', 'ch3', 'ch4', 'ch5'}
        
        print("✅ Структура результата правильная")
