"""
тест для writef создает файл
"""
import os

def test_writef_creates_file():
    from structs import Layout
    
    layout = Layout(name="Тест")
    
    if os.path.exists("result.txt"):
        os.remove("result.txt")
    
    layout.writef("txt", ["первая строка\n", "вторая строка\n"])
    
    assert os.path.exists("result.txt"), "writef не создал файл result.txt!"
    print("✅ writef создал файл result.txt")
    
    with open("result.txt", "r") as f:
        content = f.read()
        print(f"📄 В файле: {repr(content[:50])}...")
    
    os.remove("result.txt")
    print("✅ Файл удалён (тест чистый)")
