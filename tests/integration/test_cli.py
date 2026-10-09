import json
from proteus.interface.cli import main

def test_cli_commands(tmp_path,capsys):
    home=str(tmp_path/"home")
    assert main(["--home",home,"init"])==0
    assert main(["--home",home,"train","--episodes","30","--size","5"])==0
    assert main(["--home",home,"status"])==0
    status=json.loads(capsys.readouterr().out.split("}\n")[-2]+"}") if False else None
    assert main(["--home",home,"tool","arithmetic","1+2*3"])==0
    assert "7.0" in capsys.readouterr().out
