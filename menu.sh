
pkill python
echo "Waiting for running program to exit.."
while kill -0 $(pgrep python)
do
	echo "Waiting.."
done

python Main.py menu
wait
nohup python -u main.py &



