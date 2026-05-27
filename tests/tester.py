import subprocess

def run_child_script(module_name, extra_args=None):
    command = ["python", "-m", module_name]
    if extra_args:
        command.extend(extra_args)
        
    result = subprocess.run(
        command, 
        capture_output=True, 
        text=True,
        check=True  
    )
    
    return result.stdout

def extract_returned(string):
    extracted = string[string.find("Assembled successfully.") + len("Assembled successfully."):string.find("Program executed successfully.")]
    extracted = extracted.replace(" ", "").replace("\n","")
    return extracted

def run(args = None):
    try:
        
        captured_output = run_child_script("tests.parser_runner", extra_args=args)    
        return extract_returned(captured_output)
        
    except subprocess.CalledProcessError as e:
        print(f"The script failed with error  {e.returncode}")
        print(f"Error output:\n{e.stderr}")    



#TEsts__________________________________________________________________

def test_func1():
    ret = run("tests/scripts/test_func1")
    assert ret == "300"
    


def test_func2():
    ret = run("tests/scripts/test_func2")
    assert ret == "0"


def test_func3():
    ret = run("tests/scripts/test_func3")
    assert ret == "4"

def test_func4():
    ret = run("tests/scripts/test_func4")
    assert ret == "5"

def test_func5():
    ret = run("tests/scripts/test_func5")
    
    assert ret == "55"

def test_func6():
    #This test tests that parameters in functions can have the same name as global vars without interference
    ret = run("tests/scripts/test_func6")
    assert ret == "10100"
    
def test_func7():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_func7")
    assert ret == "100"


def test_func8():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_func8")
    assert ret == "Hello"
    
if __name__ == "__main__":
    all_tests = [
        test_func1,
        test_func2,
        test_func3,
        test_func4,
        test_func5,
        test_func6,
        test_func7,
        test_func8
    ]
    t = 1
    for test in all_tests:
        try:
            test()
            print(f"Success at test func {t}")
        except:
            print(f"error in test func {t}")
        t += 1

