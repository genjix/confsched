#!/bin/sh
python confsched.py sat-sat &
python confsched.py sat-alp &
python confsched.py sat-lib &
python confsched.py sun-sat &
python confsched.py sun-alp &
python confsched.py sun-lib &

