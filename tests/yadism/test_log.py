# -*- coding: utf-8 -*-
from yadism import log


def test_setup(caplog, capsys):
    log.setup()
    log.logger.info("Try not. Do or do not. There is no try.")

    assert "There is no try" in caplog.text
    assert "There is no try" in capsys.readouterr().out

    log.setup(log_to_stdout=False)
    log.logger.info("The ability to speak does not make you intelligent.")

    assert "intelligent" in caplog.text
    assert "intelligent" not in capsys.readouterr().out
