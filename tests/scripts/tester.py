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


def test_func2():
    ret = run("tests/scripts/test_func3")
    assert ret == "0"


if __name__ == "__main__":
    all_tests = [
        test_func1,
        test_func2,
        
    ]
    t = 1
    for test in all_tests:
        try:
            test()
            print(f"Success at test func {t}")
        except:
            print("error in test func 1")
        t += 1

