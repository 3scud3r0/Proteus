import pytest
from proteus.safety.sandbox import Workspace
from proteus.safety.approval import Approval
from proteus.safety.policy import Policy
from proteus.tools.python_runner import arithmetic
from proteus.tools.shell_runner import execute
from proteus.tools.browser import retrieve
from proteus.tools.code_editor import save_python
from proteus.tools.test_runner import syntax_check
from proteus.tools.registry import ToolRegistry
from proteus.tools.permissions import ToolPermissions
from proteus.tools.executor import ToolExecutor
from proteus.evolution.promotion import promote

def test_workspace_confines_files(tmp_path):
    w=Workspace(tmp_path/"workspace",max_bytes=1000)
    w.write("ok/hello.txt","teste")
    assert w.read("ok/hello.txt")=="teste"
    with pytest.raises(PermissionError):w.write("../escape.txt","bad")
    with pytest.raises(PermissionError):w.write("/tmp/escape.txt","bad")
    outside=tmp_path/"outside";outside.mkdir()
    (w.root/"link").symlink_to(outside,target_is_directory=True)
    with pytest.raises(PermissionError):w.write("link/oops.txt","bad")
    with pytest.raises(ValueError):w.write("big.txt","x"*1001)

def test_arithmetic_ast_limits():
    assert arithmetic("(4+2)*3")==18.
    for expr in ('__import__("os").system("echo bad")','2**1000000','[1,2]','1 if 1 else 2'):
        with pytest.raises((PermissionError,ValueError)):arithmetic(expr)
    with pytest.raises(PermissionError):execute("echo hi")
    with pytest.raises(PermissionError):retrieve("https://example.com")

def test_tools_are_opt_in(tmp_path):
    r=ToolRegistry();r.register("sum",lambda a,b:a+b)
    executor=ToolExecutor(r,ToolPermissions({"sum"}))
    assert executor.execute("sum",a=1,b=2)==3
    with pytest.raises(PermissionError):ToolExecutor(r,ToolPermissions()).execute("sum",a=1,b=2)
    workspace=Workspace(tmp_path/"safe")
    save_python(workspace,"sample.py","print(1)\n")
    assert syntax_check(workspace,"sample.py")["valid"]

def test_promotion_requires_approval(tmp_path):
    with pytest.raises(PermissionError):promote("a",{"alpha":0.3},Approval("a","reviewer",False),tmp_path/"p.json")
    promote("a",{"alpha":0.3},Approval("a","reviewer",True),tmp_path/"p.json")
    assert (tmp_path/"p.json").exists()
    assert not Policy().permit("shell")
