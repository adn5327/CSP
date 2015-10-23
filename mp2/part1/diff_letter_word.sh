echo "This script checks if the Word and Letter implementations return the same values"

echo "Puzzle 1"
python main.py puzzles/puzzle1.txt word notrace > word.txt
python main.py puzzles/puzzle1.txt letter notrace > letter.txt
echo "Word"
cat word.txt 
echo "Letter"
cat letter.txt

echo "Puzzle 2"
python main.py puzzles/puzzle2.txt word notrace > word.txt
python main.py puzzles/puzzle2.txt letter notrace > letter.txt
echo "Word"
cat word.txt 
echo "Letter"
cat letter.txt

echo "Puzzle 3"
python main.py puzzles/puzzle3.txt word notrace > word.txt
python main.py puzzles/puzzle3.txt letter notrace > letter.txt
echo "Word"
cat word.txt 
echo "Letter"
cat letter.txt

echo "Puzzle 4"
python main.py puzzles/puzzle4.txt word notrace > word.txt
python main.py puzzles/puzzle4.txt letter notrace > letter.txt
echo "Word"
cat word.txt 
echo "Letter"
cat letter.txt

echo "Puzzle 5"
python main.py puzzles/puzzle5.txt word notrace > word.txt
python main.py puzzles/puzzle5.txt letter notrace > letter.txt
echo "Word"
cat word.txt 
echo "Letter"
cat letter.txt

rm word.txt
rm letter.txt