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
    if  ret != "300" :
        print( f"Wrong value  {ret}" )
        
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
    # !!! This test is no longer supposed to work
    ret = run("tests/scripts/test_func7")
    if  ret != "100" :
        print( f"Wrong value  {ret}" )
        raise ValueError(f"Wrong value  {ret}")

def test_func8():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_func8")
    if  ret != "4and10" :
        print( f"Wrong value  {ret}" )
        raise ValueError(f"Wrong value  {ret}")

def test_basique0():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_basique.c")
    assert ret == "6"

def test_pt0():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_pt0")
    assert ret == "4"

def test_pt_func0():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_pt_func0")
    assert ret == "4"

def test_pt_func1():
    #This test tests that global vars can be used in functions
    ret = run("tests/scripts/test_pt_func1")
    assert ret == "0,10,20,30,40,"


def test_leftexpr_pt0():
    ret = run("tests/scripts/test_leftexpr_pt0")
    assert ret == "5"

def test_leftexpr_pt1():
    ret = run("tests/scripts/test_leftexpr_pt1")
    assert ret == "6"


def test_leftexpr_func0():
    ret = run("tests/scripts/test_leftexpr_func0")
    assert ret == "5"


def test_leftexpr_func1():
    ret = run("tests/scripts/test_leftexpr_func1")
    assert ret == "6"

def test_malloc0():
    ret = run("tests/scripts/test_malloc0")
    assert ret == "5"

def test_tab0():
    ret = run("tests/scripts/test_tab0")
    assert ret == "18"

def test_tab1():
    ret = run("tests/scripts/test_tab1")
    assert ret == "50"

def test_tab2():
    ret = run("tests/scripts/test_tab2")
    assert ret == "5"

def test_tab3():
    ret = run("tests/scripts/test_tab3")
    assert ret == "20"

def test_tab4():
    ret = run("tests/scripts/test_tab4")
    assert ret == "012"

def test_malloc_func():
    ret = run("tests/scripts/test_malloc_func")
    assert ret == "5"

def test_merge_sort():
    ret = run("tests/scripts/test_merge_sort")
    assert ret == "0 , 36 , 48 , 42 , 24 , 0 , -24 , -42 , -48 , -36 , Final  -48 , -42 , -36 , -24 , 0 , 0 , 24 , 36 , 42 , 48 , ".replace(" ","")

def test_merge_sort_tab():
    ret = run("tests/scripts/test_merge_sort_tab")
    assert ret == "0 , 36 , 48 , 42 , 24 , 0 , -24 , -42 , -48 , -36 , Final  -48 , -42 , -36 , -24 , 0 , 0 , 24 , 36 , 42 , 48 , ".replace(" ","")
        
def test_func_8args():
    ret = run("tests/scripts/test_func_8args")
    assert ret == "-33 and 0 , 36 , 48 , 42 , 24 , 0 , -24 , -42 , -48 , -36 , -103".replace(" ", "")

def test_for():
    ret = run("tests/scripts/test_for")
    assert ret == "012345678910"


if __name__ == "__main__":
    all_tests = [
        test_basique0,
        test_func1,
        test_func2,
        test_func3,
        test_func4,
        test_func5,
        test_func6,
        test_func8,
        test_func_8args,
        test_pt0,
        test_pt_func0,
        test_pt_func1,
        test_leftexpr_pt0,
        test_leftexpr_func0,
        test_malloc0,
        test_malloc_func,
        test_leftexpr_pt1,
        test_leftexpr_func1,
        test_merge_sort,
        test_merge_sort_tab,
        test_tab0,
        test_tab1,
        test_tab2,
        test_tab3,
        test_tab4,
        test_for
]
    t = 1
    for test in all_tests:
        try:
            test()
            print(f"Success at test  {test.__name__}")
        except:
            print(f"error in test  {test.__name__} ")
            break
            
        t += 1

